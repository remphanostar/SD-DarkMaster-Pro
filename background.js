// RCP - Right Click Prompt Firefox Extension
// Simplified version without preloaded prompts

// Storage Manager for handling folders and prompts
const storageManager = {
  getFolders: async function() {
    return new Promise((resolve, reject) => {
      browser.storage.local.get(['rcpFolders'], (result) => {
        if (browser.runtime.lastError) {
          reject(new Error(browser.runtime.lastError.message));
        } else {
          resolve(result.rcpFolders || []);
        }
      });
    });
  },
  
  saveFolders: async function(folders) {
    return new Promise((resolve, reject) => {
      browser.storage.local.set({ rcpFolders: folders }, () => {
        if (browser.runtime.lastError) {
          reject(new Error(browser.runtime.lastError.message));
        } else {
          resolve();
        }
      });
    });
  }
};

// Function to rebuild context menu
async function rebuildContextMenu() {
  try {
    // Clear existing context menu items
    await browser.contextMenus.removeAll();
    
    // Get folders
    const folders = await storageManager.getFolders();
    
    // Create main context menu item
    browser.contextMenus.create({
      id: 'rcp-main',
      title: 'RCP - Right Click Prompt',
      contexts: ['selection']
    });
    
    // Create folder submenu items
    folders.forEach(folder => {
      browser.contextMenus.create({
        id: `rcp-folder-${folder.id}`,
        title: folder.name,
        parentId: 'rcp-main',
        contexts: ['selection']
      });
      
      // Create prompt items for each folder
      if (folder.prompts && folder.prompts.length > 0) {
        folder.prompts.forEach(prompt => {
          browser.contextMenus.create({
            id: `rcp-prompt-${prompt.id}`,
            title: prompt.title,
            parentId: `rcp-folder-${folder.id}`,
            contexts: ['selection']
          });
        });
      }
    });
    
    // Add separator
    browser.contextMenus.create({
      id: 'rcp-separator',
      type: 'separator',
      parentId: 'rcp-main',
      contexts: ['selection']
    });
    
    // Add "Save Selection" option
    browser.contextMenus.create({
      id: 'rcp-save-selection',
      title: '💾 Save Selection as Prompt...',
      parentId: 'rcp-main',
      contexts: ['selection']
    });
    
  } catch (error) {
    console.error('Error rebuilding context menu:', error);
  }
}

// Function to show toast notification on active tab
async function showToastOnActiveTab(message) {
  try {
    const [activeTab] = await browser.tabs.query({ active: true, currentWindow: true });
    if (activeTab && activeTab.id) {
      await browser.tabs.sendMessage(activeTab.id, {
        action: 'showToast',
        message: message
      });
    }
  } catch (error) {
    console.error('Error showing toast:', error);
  }
}

// Initialize extension
browser.runtime.onInstalled.addListener(async (details) => {
  console.log('RCP Extension installed/updated');
  
  // Initialize with empty folders (no preloaded prompts)
  try {
    const existingFolders = await storageManager.getFolders();
    if (existingFolders.length === 0) {
      // Start with empty folders array
      await storageManager.saveFolders([]);
    }
  } catch (error) {
    console.error('Error initializing storage:', error);
  }
  
  // Rebuild context menu
  await rebuildContextMenu();
});

// Handle context menu clicks
browser.contextMenus.onClicked.addListener(async (info, tab) => {
  try {
    const menuItemId = info.menuItemId;
    
    if (menuItemId === 'rcp-save-selection') {
      // Save selection as prompt
      const selectedText = info.selectionText;
      if (selectedText) {
        // Store the selected text and open the popup
        await browser.storage.local.set({
          pendingPromptText: selectedText,
          pendingPromptSource: 'context-menu'
        });
        
        // Open the extension popup
        browser.browserAction.openPopup();
      }
    } else if (menuItemId.startsWith('rcp-prompt-')) {
      // Handle prompt click
      const promptId = menuItemId.replace('rcp-prompt-', '');
      
      // Find the prompt in storage
      const folders = await storageManager.getFolders();
      let promptText = '';
      
      for (const folder of folders) {
        if (folder.prompts) {
          const prompt = folder.prompts.find(p => p.id === promptId);
          if (prompt) {
            promptText = prompt.text;
            break;
          }
        }
      }
      
      if (promptText) {
        // Copy to clipboard
        await navigator.clipboard.writeText(promptText);
        await showToastOnActiveTab('Prompt copied to clipboard!');
      }
    }
  } catch (error) {
    console.error('Error handling context menu click:', error);
  }
});

// Listen for messages from popup and content scripts
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Background script received message:', message);
  
  if (message.action === 'ping') {
    sendResponse({ success: true, message: 'pong', timestamp: Date.now() });
    return true;
  }
  
  if (message.action === 'getFolders') {
    storageManager.getFolders().then(folders => {
      sendResponse({ success: true, folders: folders });
    }).catch(error => {
      console.error('Error getting folders:', error);
      sendResponse({ success: false, error: 'Failed to get folders' });
    });
    return true;
  }
  
  if (message.action === 'createFolder') {
    (async () => {
      const folderName = message.name;
      
      if (!folderName) {
        sendResponse({ success: false, error: 'Folder name is required' });
        return;
      }
      
      try {
        const folders = await storageManager.getFolders();
        
        // Check if folder already exists
        if (folders.some(folder => folder.name === folderName)) {
          sendResponse({ success: false, error: 'Folder already exists' });
          return;
        }
        
        const newFolder = {
          id: 'folder_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
          name: folderName,
          prompts: []
        };
        
        folders.push(newFolder);
        await storageManager.saveFolders(folders);
        await rebuildContextMenu();
        
        sendResponse({ success: true, folderId: newFolder.id });
      } catch (error) {
        console.error('Error creating folder:', error);
        sendResponse({ success: false, error: 'Failed to create folder' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'createPrompt') {
    (async () => {
      const { folderName, prompt } = message;
      
      if (!folderName || !prompt || !prompt.text) {
        sendResponse({ success: false, error: 'Folder name and prompt text are required' });
        return;
      }
      
      try {
        const folders = await storageManager.getFolders();
        const folder = folders.find(f => f.name === folderName);
        
        if (!folder) {
          sendResponse({ success: false, error: 'Folder not found' });
          return;
        }
        
        const newPrompt = {
          id: 'prompt_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
          title: prompt.title || 'Untitled Prompt',
          text: prompt.text,
          source: prompt.source || 'custom',
          timestamp: prompt.timestamp || new Date().toISOString()
        };
        
        folder.prompts.push(newPrompt);
        await storageManager.saveFolders(folders);
        await rebuildContextMenu();
        
        sendResponse({ success: true, promptId: newPrompt.id });
      } catch (error) {
        console.error('Error creating prompt:', error);
        sendResponse({ success: false, error: 'Failed to create prompt' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'deleteFolder') {
    (async () => {
      const folderName = message.name;
      
      if (!folderName) {
        sendResponse({ success: false, error: 'Folder name is required' });
        return;
      }
      
      try {
        const folders = await storageManager.getFolders();
        const updatedFolders = folders.filter(folder => folder.name !== folderName);
        
        await storageManager.saveFolders(updatedFolders);
        await rebuildContextMenu();
        
        sendResponse({ success: true });
      } catch (error) {
        console.error('Error deleting folder:', error);
        sendResponse({ success: false, error: 'Failed to delete folder' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'deletePrompt') {
    (async () => {
      const { folderName, promptId } = message;
      
      if (!folderName || !promptId) {
        sendResponse({ success: false, error: 'Folder name and prompt ID are required' });
        return;
      }
      
      try {
        const folders = await storageManager.getFolders();
        const folder = folders.find(f => f.name === folderName);
        
        if (!folder) {
          sendResponse({ success: false, error: 'Folder not found' });
          return;
        }
        
        folder.prompts = folder.prompts.filter(p => p.id !== promptId);
        await storageManager.saveFolders(folders);
        await rebuildContextMenu();
        
        sendResponse({ success: true });
      } catch (error) {
        console.error('Error deleting prompt:', error);
        sendResponse({ success: false, error: 'Failed to delete prompt' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'updatePrompt') {
    (async () => {
      const { folderName, promptId, prompt } = message;
      
      if (!folderName || !promptId || !prompt) {
        sendResponse({ success: false, error: 'Folder name, prompt ID, and prompt data are required' });
        return;
      }
      
      try {
        const folders = await storageManager.getFolders();
        const folder = folders.find(f => f.name === folderName);
        
        if (!folder) {
          sendResponse({ success: false, error: 'Folder not found' });
          return;
        }
        
        const promptIndex = folder.prompts.findIndex(p => p.id === promptId);
        if (promptIndex === -1) {
          sendResponse({ success: false, error: 'Prompt not found' });
          return;
        }
        
        folder.prompts[promptIndex] = { ...folder.prompts[promptIndex], ...prompt };
        await storageManager.saveFolders(folders);
        await rebuildContextMenu();
        
        sendResponse({ success: true });
      } catch (error) {
        console.error('Error updating prompt:', error);
        sendResponse({ success: false, error: 'Failed to update prompt' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'renameFolder') {
    (async () => {
      const { oldName, newName } = message;
      
      if (!oldName || !newName) {
        sendResponse({ success: false, error: 'Old name and new name are required' });
        return;
      }
      
      try {
        const folders = await storageManager.getFolders();
        const folder = folders.find(f => f.name === oldName);
        
        if (!folder) {
          sendResponse({ success: false, error: 'Folder not found' });
          return;
        }
        
        // Check if new name already exists
        if (folders.some(f => f.name === newName && f.name !== oldName)) {
          sendResponse({ success: false, error: 'Folder with this name already exists' });
          return;
        }
        
        folder.name = newName;
        await storageManager.saveFolders(folders);
        await rebuildContextMenu();
        
        sendResponse({ success: true });
      } catch (error) {
        console.error('Error renaming folder:', error);
        sendResponse({ success: false, error: 'Failed to rename folder' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'resetLibrary') {
    (async () => {
      try {
        await storageManager.saveFolders([]);
        await rebuildContextMenu();
        sendResponse({ success: true });
      } catch (error) {
        console.error('Error resetting library:', error);
        sendResponse({ success: false, error: 'Failed to reset library' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'clearAllData') {
    (async () => {
      try {
        await storageManager.saveFolders([]);
        await rebuildContextMenu();
        sendResponse({ success: true });
      } catch (error) {
        console.error('Error clearing data:', error);
        sendResponse({ success: false, error: 'Failed to clear data' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'discoverPrompts') {
    // Mock discover functionality - returns empty result since we removed preloaded prompts
    setTimeout(() => {
      sendResponse({ success: false, error: 'Discover functionality disabled - no preloaded prompts available' });
    }, 500);
    return true;
  }
  
  if (message.action === 'saveSelectionAsPrompt') {
    (async () => {
      try {
        const { text, folderId, title } = message;
        
        if (!text || !folderId) {
          sendResponse({ success: false, error: 'Text and folder ID are required' });
          return;
        }
        
        const folders = await storageManager.getFolders();
        const folder = folders.find(f => f.id === folderId);
        
        if (!folder) {
          sendResponse({ success: false, error: 'Folder not found' });
          return;
        }
        
        const newPrompt = {
          id: 'prompt_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
          title: title || 'Selection Prompt',
          text: text,
          timestamp: Date.now(),
          source: 'selection'
        };
        
        folder.prompts.push(newPrompt);
        await storageManager.saveFolders(folders);
        await rebuildContextMenu();
        
        // Clear the pending prompt data
        await browser.storage.local.remove(['pendingPromptText', 'pendingPromptSource']);
        
        sendResponse({ success: true, promptId: newPrompt.id });
      } catch (error) {
        console.error('Error saving selection as prompt:', error);
        sendResponse({ success: false, error: 'Failed to save selection as prompt' });
      }
    })();
    
    return true;
  }
  
  if (message.action === 'getPendingPrompt') {
    (async () => {
      try {
        const result = await browser.storage.local.get(['pendingPromptText', 'pendingPromptSource']);
        sendResponse({ 
          success: true, 
          text: result.pendingPromptText || '',
          source: result.pendingPromptSource || 'selection'
        });
      } catch (error) {
        console.error('Error getting pending prompt:', error);
        sendResponse({ success: false, error: 'Failed to get pending prompt' });
      }
    })();
    
    return true;
  }
  
  return true;
});

// Initialize context menu when extension starts
rebuildContextMenu().catch(error => {
  console.error('Error initializing context menu:', error);
});