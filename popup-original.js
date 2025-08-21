document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM Content Loaded - Initializing RCP Popup');
  
  const folderList = document.getElementById('folderList');
  const addFolderBtn = document.getElementById('addFolderBtn');
  const addPromptBtn = document.getElementById('addPromptBtn');
  const saveSelectionBtn = document.getElementById('saveSelectionBtn');
  const discoverBtn = document.getElementById('discoverBtn');
  const resetBtn = document.getElementById('resetBtn');
  const openFullBtn = document.getElementById('openFullBtn');
  const importFileBtn = document.getElementById('importFileBtn');
  const manageCategoriesBtn = document.getElementById('manageCategoriesBtn');
  const fileInput = document.getElementById('fileInput');
  const searchInput = document.getElementById('search-input');
  const statsText = document.getElementById('stats-text');
  const compactToggle = document.getElementById('compact-toggle');
  
  // Debug: Check if all elements are found
  console.log('Element check results:');
  console.log('folderList:', folderList);
  console.log('addFolderBtn:', addFolderBtn);
  console.log('addPromptBtn:', addPromptBtn);
  console.log('saveSelectionBtn:', saveSelectionBtn);
  console.log('discoverBtn:', discoverBtn);
  console.log('resetBtn:', resetBtn);
  console.log('openFullBtn:', openFullBtn);
  console.log('importFileBtn:', importFileBtn);
  console.log('manageCategoriesBtn:', manageCategoriesBtn);
  console.log('fileInput:', fileInput);
  console.log('searchInput:', searchInput);
  console.log('statsText:', statsText);
  console.log('compactToggle:', compactToggle);
  
  // Check if critical elements are missing
  if (!addFolderBtn || !addPromptBtn || !saveSelectionBtn || !importFileBtn) {
    console.error('Critical elements not found!');
    return;
  }
  
  let folders = [];
  let isCompactMode = true;
  let searchTerm = '';
  let expandedFolders = new Set();

  // Load compact mode preference
  loadCompactMode();
  
  // Load folders and prompts
  loadFolders();
  
  // Add folder button functionality
  addFolderBtn.addEventListener('click', () => {
    console.log('Add Folder button clicked');
    const folderName = prompt('Enter folder name:');
    if (folderName && folderName.trim()) {
      createFolder(folderName.trim());
    }
  });
  
  // Add prompt button functionality
  addPromptBtn.addEventListener('click', () => {
    console.log('Add Prompt button clicked');
    const promptText = prompt('Enter prompt text:');
    if (promptText && promptText.trim()) {
      const promptTitle = prompt('Enter prompt title (optional):') || 'Untitled Prompt';
      createPrompt(promptTitle.trim(), promptText.trim());
    }
  });
  
  // Save selection button functionality
  saveSelectionBtn.addEventListener('click', async () => {
    try {
      // Get the active tab to check if there's any selected text
      const [activeTab] = await browser.tabs.query({ active: true, currentWindow: true });
      
      if (!activeTab || !activeTab.id) {
        showNotification('No active tab found.', 'error');
        return;
      }

      // Try to get selected text from the active tab
      const results = await browser.scripting.executeScript({
        target: { tabId: activeTab.id },
        func: () => {
          const selection = window.getSelection();
          return selection ? selection.toString().trim() : '';
        }
      });

      const selectedText = results && results[0] ? results[0].result : '';
      
      if (!selectedText) {
        showNotification('Please highlight some text on the page first, then click this button.', 'info');
        return;
      }

      // Store the selected text temporarily and open category selection
      await browser.storage.local.set({ 
        pendingPromptText: selectedText,
        pendingPromptSource: 'popup'
      });

      // Inject the category selector
      await browser.scripting.executeScript({
        target: { tabId: activeTab.id },
        files: ['category-selector.js']
      });

      // Close the popup
      window.close();
      
    } catch (error) {
      console.error('Error handling save selection:', error);
      showNotification('Failed to save selection. Please try again.', 'error');
    }
  });
  
  // Discover prompts button functionality
  discoverBtn.addEventListener('click', () => {
    showDiscoveryOptions();
  });
  
  // Reset library button functionality
  resetBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to reset the preloaded prompt library? This will remove all preloaded prompts and reload them. Your custom folders and prompts will be preserved.')) {
      resetPreloadedPrompts();
    }
  });

  // Open full UI button functionality
  openFullBtn.addEventListener('click', () => {
    browser.tabs.create({ url: browser.runtime.getURL('full-ui.html') });
    window.close();
  });
  
  // Import file button functionality
  importFileBtn.addEventListener('click', () => {
    console.log('Import File button clicked');
    showImportFileModal();
  });
  
  // File input change handler
  fileInput.addEventListener('change', (e) => {
    handleFileImport(e.target.files);
  });
  
  // Function to handle file input change
  function handleFileImport(files) {
    if (files && files.length > 0) {
      updateSelectedFilesDisplay();
    }
  }
  
  // Manage categories button functionality
  manageCategoriesBtn.addEventListener('click', () => {
    showCategoryManagementModal();
  });
  
  // Search functionality
  searchInput.addEventListener('input', (e) => {
    searchTerm = e.target.value.toLowerCase();
    renderFolders();
  });

  // Compact mode toggle
  compactToggle.addEventListener('click', () => {
    isCompactMode = !isCompactMode;
    compactToggle.classList.toggle('active', isCompactMode);
    browser.storage.local.set({ compactMode: isCompactMode });
    renderFolders();
  });
  
  // Function to load compact mode preference
  async function loadCompactMode() {
    try {
      const result = await browser.storage.local.get(['compactMode']);
      isCompactMode = result.compactMode !== false; // Default to true
      compactToggle.classList.toggle('active', isCompactMode);
    } catch (error) {
      console.error('Error loading compact mode preference:', error);
    }
  }
  
  // Function to show discovery options
  function showDiscoveryOptions() {
    const options = `
      <div style="padding: 20px; background: #f9fafb; border-radius: 8px; margin: 10px 0;">
        <h3 style="margin: 0 0 15px 0; color: #374151;">🔍 Discover New Prompts</h3>
        <p style="margin: 0 0 15px 0; color: #6b7280; font-size: 12px;">
          Get fresh prompts from legitimate sources. Choose a category:
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
          <button onclick="discoverPrompts('writing')" class="discovery-btn" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">✍️ Writing</button>
          <button onclick="discoverPrompts('coding')" class="discovery-btn" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">💻 Coding</button>
          <button onclick="discoverPrompts('analysis')" class="discovery-btn" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">📊 Analysis</button>
          <button onclick="discoverPrompts('business')" class="discovery-btn" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">💼 Business</button>
          <button onclick="discoverPrompts('education')" class="discovery-btn" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">🎓 Education</button>
          <button onclick="discoverPrompts('creative')" class="discovery-btn" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">🎨 Creative</button>
          <button onclick="discoverPrompts('communication')" class="discovery-btn" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">💬 Communication</button>
          <button onclick="discoverPrompts('problems')" class="discovery-btn" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">🧩 Problem Solving</button>
        </div>
        <div style="margin-top: 12px;">
          <button onclick="discoverPrompts('all')" class="discovery-btn" style="width: 100%; padding: 8px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 500; font-size: 11px;">🎯 Discover All Categories</button>
        </div>
        <div style="margin-top: 8px;">
          <button onclick="closeDiscoveryOptions()" style="width: 100%; padding: 6px; background: #6b7280; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 10px;">Cancel</button>
        </div>
      </div>
    `;
    
    // Create discovery modal
    const modal = document.createElement('div');
    modal.id = 'discovery-modal';
    modal.innerHTML = options;
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
    `;
    
    document.body.appendChild(modal);
  }
  
  // Function to close discovery options
  function closeDiscoveryOptions() {
    const modal = document.getElementById('discovery-modal');
    if (modal) {
      modal.remove();
    }
  }
  
  // Function to discover prompts (make it globally accessible)
  window.discoverPrompts = async function(category) {
    closeDiscoveryOptions();
    showNotification(`Discovering ${category} prompts...`, 'info');
    
    try {
      const response = await browser.runtime.sendMessage({ 
        action: 'discoverPrompts', 
        category: category 
      });
      
      if (response.success) {
        showNotification(`Discovered ${response.count} new ${category} prompts!`, 'success');
        loadFolders(); // Refresh the list
      } else {
        showNotification('Failed to discover prompts: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error discovering prompts:', error);
      showNotification('Error discovering prompts. Please try again.', 'error');
    }
  };
  
  // Function to close discovery options (make it globally accessible)
  window.closeDiscoveryOptions = function() {
    closeDiscoveryOptions();
  };
  
  // Function to show import file modal
  function showImportFileModal() {
    console.log('showImportFileModal called');
    // Remove any existing modal first
    const existingModal = document.getElementById('import-file-modal');
    if (existingModal) {
      existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'import-file-modal';
    modal.innerHTML = `
      <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000; display: flex; align-items: center; justify-content: center;">
        <div style="background: linear-gradient(135deg, #1a0000 0%, #330000 100%); border: 2px solid #ffd700; border-radius: 12px; padding: 24px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto; box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #ffd700; font-size: 18px; font-weight: 600; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">Import Files</h3>
            <button id="close-import-modal" style="background: none; border: none; color: #ffd700; font-size: 24px; cursor: pointer; padding: 4px; border-radius: 4px;">&times;</button>
          </div>
          <div style="margin-bottom: 20px;">
            <p style="color: #ffcc00; margin-bottom: 16px; font-size: 12px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">
              Import markdown (.md), text (.txt), or JSON files into your prompt library. Each file will be processed and added as a prompt to the selected category.
            </p>
            <div style="margin-bottom: 16px;">
              <label style="display: block; margin-bottom: 6px; font-weight: 500; color: #ffd700; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">Select Category</label>
              <select id="import-category-select" style="width: 100%; padding: 10px 12px; border: 1px solid #ffd700; border-radius: 6px; font-size: 14px; background: linear-gradient(135deg, rgba(26,0,0,0.8) 0%, rgba(51,0,0,0.9) 100%); color: #ffd700; box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);">
                <option value="">Choose a category...</option>
              </select>
            </div>
            <div style="margin-bottom: 16px;">
              <label style="display: block; margin-bottom: 6px; font-weight: 500; color: #ffd700; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">Or create new category</label>
              <input type="text" id="import-new-category" placeholder="Enter new category name" style="width: 100%; padding: 10px 12px; border: 1px solid #ffd700; border-radius: 6px; font-size: 14px; background: linear-gradient(135deg, rgba(26,0,0,0.8) 0%, rgba(51,0,0,0.9) 100%); color: #ffd700; box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);">
            </div>
            <div style="margin-bottom: 20px;">
              <label style="display: block; margin-bottom: 6px; font-weight: 500; color: #ffd700; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">Select Files</label>
              <button id="choose-files-btn" style="width: 100%; padding: 12px; background: linear-gradient(135deg, #8b0000 0%, #dc143c 100%); color: #ffd700; border: 1px solid #ffd700; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                📁 Choose Files (.md, .txt, .json)
              </button>
              <div id="selected-files" style="margin-top: 10px; color: #ffcc00; font-size: 12px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);"></div>
            </div>
          </div>
          <div style="display: flex; gap: 12px; justify-content: flex-end;">
            <button id="cancel-import-btn" style="padding: 10px 20px; background: linear-gradient(135deg, #4a4a4a 0%, #6d6d6d 100%); color: #ffd700; border: 1px solid #ffd700; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">Cancel</button>
            <button id="process-import-btn" style="padding: 10px 20px; background: linear-gradient(135deg, #8b0000 0%, #dc143c 100%); color: #ffd700; border: 1px solid #ffd700; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">Import Files</button>
          </div>
        </div>
      </div>
    `;
    
    console.log('Modal HTML created, appending to body');
    document.body.appendChild(modal);
    
    // Load categories into the select
    loadCategoriesIntoSelect();
    
    // Add event listeners using proper event handling
    console.log('Adding event listeners to modal buttons');
    const closeModalBtn = document.getElementById('close-import-modal');
    const cancelBtn = document.getElementById('cancel-import-btn');
    const processBtn = document.getElementById('process-import-btn');
    const chooseFilesBtn = document.getElementById('choose-files-btn');
    
    console.log('Modal buttons found:', { closeModalBtn, cancelBtn, processBtn, chooseFilesBtn });
    
    // Close modal handlers
    if (closeModalBtn) {
      closeModalBtn.addEventListener('click', () => {
        console.log('Close modal button clicked');
        closeImportModal();
      });
    }
    
    if (cancelBtn) {
      cancelBtn.addEventListener('click', () => {
        console.log('Cancel button clicked');
        closeImportModal();
      });
    }
    
    // Process import handler
    if (processBtn) {
      processBtn.addEventListener('click', () => {
        console.log('Process import button clicked');
        processFileImport();
      });
    }
    
    // Choose files handler
    if (chooseFilesBtn) {
      chooseFilesBtn.addEventListener('click', () => {
        console.log('Choose files button clicked');
        document.getElementById('fileInput').click();
      });
    }
    
    // Update selected files display when files are selected
    fileInput.addEventListener('change', updateSelectedFilesDisplay);
    
    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        console.log('Clicked outside modal, closing');
        closeImportModal();
      }
    });
    
    console.log('Modal setup complete');
  }
  
  // Function to close import modal
  function closeImportModal() {
    const modal = document.getElementById('import-file-modal');
    if (modal) {
      modal.remove();
    }
    // Reset file input
    fileInput.value = '';
  }
  
  // Function to load categories into select
  async function loadCategoriesIntoSelect() {
    try {
      const response = await browser.runtime.sendMessage({ action: 'getFolders' });
      const folders = response.folders || [];
      const select = document.getElementById('import-category-select');
      
      select.innerHTML = '<option value="">Choose a category...</option>';
      folders.forEach(folder => {
        const option = document.createElement('option');
        option.value = folder.id;
        option.textContent = folder.name;
        select.appendChild(option);
      });
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  }
  
  // Function to update selected files display
  function updateSelectedFilesDisplay() {
    const files = fileInput.files;
    const display = document.getElementById('selected-files');
    
    if (files.length > 0) {
      const fileNames = Array.from(files).map(file => file.name).join(', ');
      display.textContent = `Selected: ${fileNames}`;
    } else {
      display.textContent = '';
    }
  }
  
  // Function to process file import (made global for onclick)
  window.processFileImport = async function() {
    const categoryId = document.getElementById('import-category-select').value;
    const newCategory = document.getElementById('import-new-category').value.trim();
    const files = fileInput.files;
    
    if (!categoryId && !newCategory) {
      showNotification('Please select an existing category or create a new one!', 'error');
      return;
    }
    
    if (files.length === 0) {
      showNotification('Please select at least one file to import!', 'error');
      return;
    }
    
    let targetFolderId = categoryId;
    
    // Create new category if specified
    if (newCategory) {
      try {
        const createResponse = await browser.runtime.sendMessage({
          action: 'createFolder',
          name: newCategory
        });
        
        if (createResponse.success) {
          targetFolderId = createResponse.folderId;
          showNotification(`Created new category: ${newCategory}`, 'success');
        } else {
          showNotification('Failed to create new category!', 'error');
          return;
        }
      } catch (error) {
        console.error('Error creating category:', error);
        showNotification('Error creating new category!', 'error');
        return;
      }
    }
    
    // Process files
    let importedCount = 0;
    let errorCount = 0;
    
    for (const file of files) {
      try {
        const result = await processSingleFile(file, targetFolderId);
        if (result.success) {
          importedCount++;
        } else {
          errorCount++;
          console.error(`Failed to process ${file.name}:`, result.error);
        }
      } catch (error) {
        errorCount++;
        console.error(`Error processing ${file.name}:`, error);
      }
    }
    
    // Show results
    if (importedCount > 0) {
      showNotification(`Successfully imported ${importedCount} file${importedCount !== 1 ? 's' : ''}!`, 'success');
      if (errorCount > 0) {
        showNotification(`${errorCount} file${errorCount !== 1 ? 's' : ''} failed to import.`, 'error');
      }
      loadFolders(); // Refresh the list
    } else {
      showNotification('No files were imported successfully.', 'error');
    }
    
    // Close modal and reset
    closeImportModal();
  };
  
  // Function to process a single file
  async function processSingleFile(file, folderId) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      
      reader.onload = async (e) => {
        try {
          const content = e.target.result;
          let prompts = [];
          
          if (file.name.endsWith('.json')) {
            // Parse JSON file
            try {
              const jsonData = JSON.parse(content);
              prompts = parseJsonFile(jsonData);
            } catch (error) {
              resolve({ success: false, error: 'Invalid JSON format' });
              return;
            }
          } else {
            // Parse markdown or text file
            prompts = parseTextFile(content, file.name);
          }
          
          // Create prompts in the specified folder
          let createdCount = 0;
          for (const prompt of prompts) {
            try {
              const response = await browser.runtime.sendMessage({
                action: 'createPromptInFolder',
                folderId: folderId,
                title: prompt.title,
                text: prompt.text,
                source: 'imported'
              });
              
              if (response.success) {
                createdCount++;
              }
            } catch (error) {
              console.error('Error creating prompt:', error);
            }
          }
          
          resolve({ success: true, createdCount: createdCount });
        } catch (error) {
          resolve({ success: false, error: error.message });
        }
      };
      
      reader.onerror = () => {
        resolve({ success: false, error: 'Failed to read file' });
      };
      
      reader.readAsText(file);
    });
  }
  
  // Function to parse JSON file
  function parseJsonFile(jsonData) {
    const prompts = [];
    
    if (Array.isArray(jsonData)) {
      // Array of prompts
      jsonData.forEach((item, index) => {
        if (item.title && item.text) {
          prompts.push({
            title: item.title,
            text: item.text
          });
        } else if (item.text || item.content) {
          prompts.push({
            title: item.title || `Imported Prompt ${index + 1}`,
            text: item.text || item.content
          });
        }
      });
    } else if (jsonData.prompts && Array.isArray(jsonData.prompts)) {
      // Object with prompts array
      jsonData.prompts.forEach((item, index) => {
        prompts.push({
          title: item.title || `Imported Prompt ${index + 1}`,
          text: item.text || item.content
        });
      });
    } else if (jsonData.title && jsonData.text) {
      // Single prompt
      prompts.push({
        title: jsonData.title,
        text: jsonData.text
      });
    }
    
    return prompts;
  }
  
  // Function to parse text/markdown file
  function parseTextFile(content, fileName) {
    const prompts = [];
    
    // Split by double newlines to separate potential prompts
    const sections = content.split(/\n\s*\n/);
    
    sections.forEach((section, index) => {
      const trimmedSection = section.trim();
      if (trimmedSection) {
        // Try to extract title from the first line if it looks like a heading
        const lines = trimmedSection.split('\n');
        let title = '';
        let text = trimmedSection;
        
        if (lines.length > 1) {
          const firstLine = lines[0].trim();
          // Check if it's a markdown heading or just a title line
          if (firstLine.startsWith('#') || firstLine.length < 100) {
            title = firstLine.replace(/^#+\s*/, '').trim();
            text = lines.slice(1).join('\n').trim();
          }
        }
        
        // If no title found, create one from the filename and index
        if (!title) {
          const fileBaseName = fileName.replace(/\.[^/.]+$/, '');
          title = `${fileBaseName} - Prompt ${index + 1}`;
        }
        
        prompts.push({
          title: title,
          text: text
        });
      }
    });
    
    return prompts;
  }
  
  // Function to show category management modal
  function showCategoryManagementModal() {
    const modal = document.createElement('div');
    modal.id = 'category-management-modal';
    modal.innerHTML = `
      <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000; display: flex; align-items: center; justify-content: center;">
        <div style="background: linear-gradient(135deg, #1a0000 0%, #330000 100%); border: 2px solid #ffd700; border-radius: 12px; padding: 24px; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto; box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #ffd700; font-size: 18px; font-weight: 600; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">Manage Categories</h3>
            <button onclick="this.closest('#category-management-modal').remove()" style="background: none; border: none; color: #ffd700; font-size: 24px; cursor: pointer; padding: 4px; border-radius: 4px;">&times;</button>
          </div>
          <div style="margin-bottom: 20px;">
            <p style="color: #ffcc00; margin-bottom: 16px; font-size: 12px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">
              Drag and drop categories to reorder them. Toggle visibility to show/hide categories in the right-click menu.
            </p>
            <div id="category-sort-list" style="max-height: 300px; overflow-y: auto; margin-bottom: 16px;">
              <!-- Categories will be loaded here -->
            </div>
          </div>
          <div style="display: flex; gap: 12px; justify-content: flex-end;">
            <button onclick="this.closest('#category-management-modal').remove()" style="padding: 10px 20px; background: linear-gradient(135deg, #4a4a4a 0%, #6d6d6d 100%); color: #ffd700; border: 1px solid #ffd700; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">Close</button>
            <button onclick="saveCategoryOrder()" style="padding: 10px 20px; background: linear-gradient(135deg, #8b0000 0%, #dc143c 100%); color: #ffd700; border: 1px solid #ffd700; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">Save Order</button>
          </div>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    // Load categories into the sortable list
    loadCategoriesForManagement();
  }
  
  // Function to load categories for management
  async function loadCategoriesForManagement() {
    try {
      const response = await browser.runtime.sendMessage({ action: 'getFolders' });
      const folders = response.folders || [];
      const categoryList = document.getElementById('category-sort-list');
      
      // Get current category order and visibility settings
      const settingsResponse = await browser.runtime.sendMessage({ action: 'getCategorySettings' });
      const categoryOrder = settingsResponse.categoryOrder || [];
      const categoryVisibility = settingsResponse.categoryVisibility || {};
      
      // Sort categories according to saved order, or keep original order
      let sortedFolders = folders;
      if (categoryOrder.length > 0) {
        sortedFolders = folders.sort((a, b) => {
          const indexA = categoryOrder.indexOf(a.id);
          const indexB = categoryOrder.indexOf(b.id);
          if (indexA === -1) return 1; // Put new items at the end
          if (indexB === -1) return -1;
          return indexA - indexB;
        });
      }
      
      categoryList.innerHTML = sortedFolders.map(folder => {
        const isVisible = categoryVisibility[folder.id] !== false; // Default to visible
        return `
          <div class="category-sort-item" data-folder-id="${folder.id}" draggable="true" style="background: linear-gradient(135deg, rgba(51,0,0,0.8) 0%, rgba(26,0,0,0.9) 100%); border: 1px solid #ffd700; border-radius: 6px; padding: 12px; margin-bottom: 8px; cursor: move; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            <div style="display: flex; align-items: center; gap: 10px;">
              <span style="color: #ffd700; font-size: 16px;">⋮⋮</span>
              <span style="color: #ffd700; font-weight: 500; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">${escapeHtml(folder.name)}</span>
              <span style="color: #ffcc00; font-size: 11px; background: linear-gradient(135deg, #ffd700 0%, #ffcc00 100%); color: #660000; padding: 2px 6px; border-radius: 3px; font-weight: 600;">${folder.prompts ? folder.prompts.length : 0} prompts</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <label style="display: flex; align-items: center; gap: 4px; color: #ffcc00; font-size: 12px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">
                <input type="checkbox" class="category-visibility-toggle" data-folder-id="${folder.id}" ${isVisible ? 'checked' : ''} style="margin: 0;">
                Show in menu
              </label>
            </div>
          </div>
        `;
      }).join('');
      
      // Add drag and drop functionality
      addDragAndDropFunctionality();
      
    } catch (error) {
      console.error('Error loading categories for management:', error);
    }
  }
  
  // Function to add drag and drop functionality
  function addDragAndDropFunctionality() {
    const items = document.querySelectorAll('.category-sort-item');
    let draggedItem = null;
    
    items.forEach(item => {
      item.addEventListener('dragstart', (e) => {
        draggedItem = item;
        item.style.opacity = '0.5';
      });
      
      item.addEventListener('dragend', (e) => {
        item.style.opacity = '';
      });
      
      item.addEventListener('dragover', (e) => {
        e.preventDefault();
        const afterElement = getDragAfterElement(document.getElementById('category-sort-list'), e.clientY);
        if (afterElement == null) {
          document.getElementById('category-sort-list').appendChild(draggedItem);
        } else {
          document.getElementById('category-sort-list').insertBefore(draggedItem, afterElement);
        }
      });
    });
  }
  
  // Function to get the element after which to insert the dragged item
  function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.category-sort-item:not(.dragging)')];
    
    return draggableElements.reduce((closest, child) => {
      const box = child.getBoundingClientRect();
      const offset = y - box.top - box.height / 2;
      
      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child };
      } else {
        return closest;
      }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
  }
  
  // Function to save category order (made global for onclick)
  window.saveCategoryOrder = async function() {
    try {
      const categoryItems = document.querySelectorAll('.category-sort-item');
      const categoryOrder = Array.from(categoryItems).map(item => item.getAttribute('data-folder-id'));
      
      // Get visibility settings
      const visibilityToggles = document.querySelectorAll('.category-visibility-toggle');
      const categoryVisibility = {};
      visibilityToggles.forEach(toggle => {
        const folderId = toggle.getAttribute('data-folder-id');
        categoryVisibility[folderId] = toggle.checked;
      });
      
      // Save settings
      const response = await browser.runtime.sendMessage({
        action: 'saveCategorySettings',
        categoryOrder: categoryOrder,
        categoryVisibility: categoryVisibility
      });
      
      if (response.success) {
        showNotification('Category settings saved successfully!', 'success');
        // Rebuild context menu with new order
        await browser.runtime.sendMessage({ action: 'rebuildContextMenu' });
        loadFolders(); // Refresh the display
        document.getElementById('category-management-modal')?.remove();
      } else {
        showNotification('Failed to save category settings!', 'error');
      }
    } catch (error) {
      console.error('Error saving category settings:', error);
      showNotification('Error saving category settings!', 'error');
    }
  };
  
  // Function to load folders
  async function loadFolders() {
    try {
      const response = await browser.runtime.sendMessage({ action: 'getFolders' });
      folders = response.folders || [];
      
      updateStats();
      renderFolders();
      
    } catch (error) {
      console.error('Error loading folders:', error);
      folderList.innerHTML = '<p style="text-align: center; color: #EF4444; padding: 20px; font-size: 12px;">Error loading folders. Please try again.</p>';
    }
  }
  
  // Function to update stats
  function updateStats() {
    const totalFolders = folders.length;
    const totalPrompts = folders.reduce((sum, folder) => sum + (folder.prompts ? folder.prompts.length : 0), 0);
    statsText.textContent = `${totalFolders} folder${totalFolders !== 1 ? 's' : ''}, ${totalPrompts} prompt${totalPrompts !== 1 ? 's' : ''}`;
  }
  
  // Function to render folders
  function renderFolders() {
    folderList.innerHTML = '';
    
    if (folders.length === 0) {
      folderList.innerHTML = `
        <div class="empty-state">
          <h3>No folders yet</h3>
          <p>Create your first folder to get started organizing your prompts!</p>
        </div>
      `;
      return;
    }
    
    // Filter folders based on search term
    const filteredFolders = folders.filter(folder => {
      if (!searchTerm) return true;
      
      const folderMatches = folder.name.toLowerCase().includes(searchTerm);
      const promptsMatch = folder.prompts && folder.prompts.some(prompt => 
        prompt.title.toLowerCase().includes(searchTerm) || 
        prompt.text.toLowerCase().includes(searchTerm)
      );
      
      return folderMatches || promptsMatch;
    });
    
    if (filteredFolders.length === 0) {
      folderList.innerHTML = `
        <div class="empty-state">
          <h3>No results found</h3>
          <p>Try adjusting your search terms or create a new folder.</p>
        </div>
      `;
      return;
    }
    
    filteredFolders.forEach(folder => {
      const folderElement = createFolderElement(folder);
      folderList.appendChild(folderElement);
    });
  }
  
  // Function to create folder element
  function createFolderElement(folder) {
    const div = document.createElement('div');
    div.className = 'folder-item';
    
    const isExpanded = expandedFolders.has(folder.id);
    const folderPrompts = folder.prompts || [];
    
    // Filter prompts based on search term
    const filteredPrompts = searchTerm 
      ? folderPrompts.filter(prompt => 
          prompt.title.toLowerCase().includes(searchTerm) || 
          prompt.text.toLowerCase().includes(searchTerm)
        )
      : folderPrompts;
    
    div.innerHTML = `
      <div class="folder-header ${isExpanded ? '' : 'collapsed'}" data-folder-id="${folder.id}">
        <div class="folder-info">
          <button class="folder-toggle ${isExpanded ? 'expanded' : ''}" data-folder-id="${folder.id}">▶</button>
          <h3 class="folder-name">${escapeHtml(folder.name)}</h3>
          <span class="folder-count">${filteredPrompts.length}</span>
        </div>
        <div class="folder-actions">
          <button class="btn-add-prompt" data-folder-id="${folder.id}" title="Add prompt to this folder">+</button>
          <button class="btn-delete-folder" data-folder-id="${folder.id}" title="Delete folder">🗑️</button>
        </div>
      </div>
      <div class="prompt-container ${isExpanded ? 'expanded' : ''}" id="prompts-${folder.id}">
        ${filteredPrompts.length > 0 ? filteredPrompts.map(prompt => createPromptHTML(prompt)).join('') : '<p class="no-prompts">No prompts in this folder yet.</p>'}
      </div>
    `;
    
    // Add event listeners
    const folderHeader = div.querySelector('.folder-header');
    const folderToggle = div.querySelector('.folder-toggle');
    const addPromptBtn = div.querySelector('.btn-add-prompt');
    const deleteFolderBtn = div.querySelector('.btn-delete-folder');
    
    folderHeader.addEventListener('click', (e) => {
      if (!e.target.closest('.folder-actions')) {
        toggleFolder(folder.id);
      }
    });
    
    folderToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleFolder(folder.id);
    });
    
    addPromptBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const promptText = prompt('Enter prompt text:');
      if (promptText && promptText.trim()) {
        const promptTitle = prompt('Enter prompt title (optional):') || 'Untitled Prompt';
        createPromptInFolder(promptTitle.trim(), promptText.trim(), folder.id);
      }
    });
    
    deleteFolderBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (confirm(`Are you sure you want to delete the folder "${folder.name}" and all its prompts?`)) {
        deleteFolder(folder.id);
      }
    });
    
    return div;
  }
  
  // Function to toggle folder expansion
  function toggleFolder(folderId) {
    if (expandedFolders.has(folderId)) {
      expandedFolders.delete(folderId);
    } else {
      expandedFolders.add(folderId);
    }
    renderFolders();
  }
  
  // Function to create prompt HTML
  function createPromptHTML(prompt) {
    const sourceBadge = prompt.source ? `<span class="prompt-source">${prompt.source}</span>` : '';
    
    return `
      <div class="prompt-item" data-prompt-id="${prompt.id}">
        <div class="prompt-header">
          <h4 class="prompt-title">${escapeHtml(prompt.title)}</h4>
          ${sourceBadge}
        </div>
        <div class="prompt-content">${escapeHtml(prompt.text)}</div>
        <div class="prompt-actions">
          <button class="btn-copy" data-prompt-id="${prompt.id}" data-text="${escapeHtml(prompt.text)}" title="Copy to clipboard">📋 Copy</button>
          <button class="btn-edit-prompt" data-prompt-id="${prompt.id}" title="Edit prompt">✏️ Edit</button>
          <button class="btn-delete-prompt" data-prompt-id="${prompt.id}" title="Delete prompt">🗑️ Delete</button>
        </div>
        <div class="prompt-timestamp">Created: ${new Date(prompt.timestamp).toLocaleString()}</div>
      </div>
    `;
  }
  
  // Function to create a new folder
  async function createFolder(name) {
    try {
      const response = await browser.runtime.sendMessage({ 
        action: 'createFolder', 
        name: name 
      });
      
      if (response.success) {
        showNotification('Folder created successfully!', 'success');
        loadFolders(); // Refresh the list
      } else {
        showNotification('Failed to create folder: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error creating folder:', error);
      showNotification('Error creating folder. Please try again.', 'error');
    }
  }
  
  // Function to create a new prompt
  async function createPrompt(title, text) {
    try {
      // Get folders first
      const foldersResponse = await browser.runtime.sendMessage({ action: 'getFolders' });
      const availableFolders = foldersResponse.folders || [];
      
      if (availableFolders.length === 0) {
        showNotification('Please create a folder first.', 'error');
        return;
      }
      
      // Use the first folder or ask user to choose
      let folderId = availableFolders[0].id;
      if (availableFolders.length > 1) {
        const folderNames = availableFolders.map((f, i) => `${i + 1}. ${f.name}`).join('\n');
        const choice = prompt(`Which folder?\n${folderNames}\n\nEnter the number (1-${availableFolders.length}):`);
        const folderIndex = parseInt(choice) - 1;
        if (folderIndex >= 0 && folderIndex < availableFolders.length) {
          folderId = availableFolders[folderIndex].id;
        } else {
          showNotification('Invalid folder selection.', 'error');
          return;
        }
      }
      
      const response = await browser.runtime.sendMessage({ 
        action: 'savePrompt', 
        title: title, 
        text: text, 
        folderId: folderId 
      });
      
      if (response.success) {
        showNotification('Prompt created successfully!', 'success');
        loadFolders(); // Refresh the list
      } else {
        showNotification('Failed to create prompt: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error creating prompt:', error);
      showNotification('Error creating prompt. Please try again.', 'error');
    }
  }
  
  // Function to create a prompt in a specific folder
  async function createPromptInFolder(title, text, folderId) {
    try {
      const response = await browser.runtime.sendMessage({ 
        action: 'savePrompt', 
        title: title, 
        text: text, 
        folderId: folderId 
      });
      
      if (response.success) {
        showNotification('Prompt added successfully!', 'success');
        // Expand the folder to show the new prompt
        expandedFolders.add(folderId);
        loadFolders(); // Refresh the list
      } else {
        showNotification('Failed to add prompt: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error creating prompt:', error);
      showNotification('Error adding prompt. Please try again.', 'error');
    }
  }
  
  // Function to delete a folder
  async function deleteFolder(folderId) {
    try {
      // Send delete request to background script
      const response = await browser.runtime.sendMessage({ 
        action: 'deleteFolder', 
        folderId: folderId 
      });
      
      if (response.success) {
        showNotification('Folder deleted successfully!', 'success');
        expandedFolders.delete(folderId);
        loadFolders(); // Refresh the list
      } else {
        showNotification('Failed to delete folder: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error deleting folder:', error);
      showNotification('Error deleting folder. Please try again.', 'error');
    }
  }
  
  // Function to copy text to clipboard
  async function copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      showNotification('Prompt copied to clipboard!', 'success');
    } catch (error) {
      console.error('Error copying to clipboard:', error);
      showNotification('Failed to copy to clipboard.', 'error');
    }
  }
  
  // Function to delete a prompt
  async function deletePrompt(promptId) {
    try {
      // Send delete request to background script
      const response = await browser.runtime.sendMessage({ 
        action: 'deletePrompt', 
        promptId: promptId 
      });
      
      if (response.success) {
        showNotification('Prompt deleted successfully!', 'success');
        loadFolders(); // Refresh the list
      } else {
        showNotification('Failed to delete prompt: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error deleting prompt:', error);
      showNotification('Error deleting prompt. Please try again.', 'error');
    }
  }
  
  // Function to edit a prompt
  async function editPrompt(promptId) {
    try {
      // Get the current prompt data
      const response = await browser.runtime.sendMessage({ 
        action: 'getPrompt', 
        promptId: promptId 
      });
      
      if (response.success && response.prompt) {
        const prompt = response.prompt;
        
        // Create edit modal
        const modal = document.createElement('div');
        modal.id = 'edit-prompt-modal';
        modal.innerHTML = `
          <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000; display: flex; align-items: center; justify-content: center;">
            <div style="background: linear-gradient(135deg, #1a0000 0%, #330000 100%); border: 2px solid #ffd700; border-radius: 12px; padding: 24px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto; box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="margin: 0; color: #ffd700; font-size: 18px; font-weight: 600; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">Edit Prompt</h3>
                <button onclick="this.closest('#edit-prompt-modal').remove()" style="background: none; border: none; color: #ffd700; font-size: 24px; cursor: pointer; padding: 4px; border-radius: 4px;">&times;</button>
              </div>
              <form id="edit-prompt-form">
                <div style="margin-bottom: 16px;">
                  <label style="display: block; margin-bottom: 6px; font-weight: 500; color: #ffd700; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">Prompt Title</label>
                  <input type="text" id="edit-prompt-title" value="${escapeHtml(prompt.title)}" required style="width: 100%; padding: 10px 12px; border: 1px solid #ffd700; border-radius: 6px; font-size: 14px; background: linear-gradient(135deg, rgba(26,0,0,0.8) 0%, rgba(51,0,0,0.9) 100%); color: #ffd700; box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);">
                </div>
                <div style="margin-bottom: 20px;">
                  <label style="display: block; margin-bottom: 6px; font-weight: 500; color: #ffd700; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">Prompt Content</label>
                  <textarea id="edit-prompt-text" rows="8" required style="width: 100%; padding: 10px 12px; border: 1px solid #ffd700; border-radius: 6px; font-size: 14px; font-family: inherit; resize: vertical; background: linear-gradient(135deg, rgba(26,0,0,0.8) 0%, rgba(51,0,0,0.9) 100%); color: #ffd700; box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);">${escapeHtml(prompt.text)}</textarea>
                </div>
                <div style="display: flex; gap: 12px; justify-content: flex-end;">
                  <button type="button" onclick="this.closest('#edit-prompt-modal').remove()" style="padding: 10px 20px; background: linear-gradient(135deg, #4a4a4a 0%, #6d6d6d 100%); color: #ffd700; border: 1px solid #ffd700; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">Cancel</button>
                  <button type="submit" style="padding: 10px 20px; background: linear-gradient(135deg, #8b0000 0%, #dc143c 100%); color: #ffd700; border: 1px solid #ffd700; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">Save Changes</button>
                </div>
              </form>
            </div>
          </div>
        `;
        
        document.body.appendChild(modal);
        
        // Handle form submission
        const form = document.getElementById('edit-prompt-form');
        form.addEventListener('submit', async (e) => {
          e.preventDefault();
          
          const newTitle = document.getElementById('edit-prompt-title').value.trim();
          const newText = document.getElementById('edit-prompt-text').value.trim();
          
          if (!newTitle || !newText) {
            showNotification('Title and content are required!', 'error');
            return;
          }
          
          try {
            const updateResponse = await browser.runtime.sendMessage({
              action: 'updatePrompt',
              promptId: promptId,
              title: newTitle,
              text: newText
            });
            
            if (updateResponse.success) {
              showNotification('Prompt updated successfully!', 'success');
              modal.remove();
              loadFolders(); // Refresh the list
            } else {
              showNotification('Failed to update prompt: ' + (updateResponse.error || 'Unknown error'), 'error');
            }
          } catch (error) {
            console.error('Error updating prompt:', error);
            showNotification('Error updating prompt. Please try again.', 'error');
          }
        });
        
      } else {
        showNotification('Failed to load prompt data: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error editing prompt:', error);
      showNotification('Error editing prompt. Please try again.', 'error');
    }
  }
  
  // Function to reset preloaded prompts
  async function resetPreloadedPrompts() {
    try {
      showNotification('Resetting preloaded prompt library...', 'info');
      
      const response = await browser.runtime.sendMessage({ 
        action: 'resetPreloadedPrompts'
      });
      
      if (response.success) {
        showNotification('Preloaded prompt library reset successfully!', 'success');
        loadFolders(); // Refresh the list
      } else {
        showNotification('Failed to reset preloaded prompts: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error resetting preloaded prompts:', error);
      showNotification('Error resetting preloaded prompts. Please try again.', 'error');
    }
  }
  
  // Function to escape HTML to prevent XSS
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  // Function to show notifications
  function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add notification styles if not already added
    if (!document.querySelector('style[data-notification-styles]')) {
      const style = document.createElement('style');
      style.setAttribute('data-notification-styles', 'true');
      style.textContent = `
        .notification {
          position: fixed;
          top: 20px;
          right: 20px;
          padding: 10px 16px;
          border-radius: 6px;
          color: white;
          font-weight: 500;
          z-index: 10000;
          max-width: 280px;
          word-wrap: break-word;
          animation: slideIn 0.3s ease-out;
          font-size: 12px;
        }
        .notification-success {
          background-color: #10B981;
        }
        .notification-error {
          background-color: #EF4444;
        }
        .notification-info {
          background-color: #3B82F6;
        }
        @keyframes slideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
      `;
      document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => {
          if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
          }
        }, 300);
      }
    }, 3000);
  }
  
  // Event delegation for dynamic elements
  document.addEventListener('click', (event) => {
    // Handle copy button clicks
    if (event.target.classList.contains('btn-copy')) {
      const text = event.target.getAttribute('data-text');
      if (text) {
        copyToClipboard(text);
      }
    }
    
    // Handle delete prompt button clicks
    if (event.target.classList.contains('btn-delete-prompt')) {
      const promptId = event.target.getAttribute('data-prompt-id');
      if (promptId) {
        if (confirm('Are you sure you want to delete this prompt?')) {
          deletePrompt(promptId);
        }
      }
    }
    
    // Handle edit prompt button clicks
    if (event.target.classList.contains('btn-edit-prompt')) {
      const promptId = event.target.getAttribute('data-prompt-id');
      if (promptId) {
        editPrompt(promptId);
      }
    }
  });
  
  // Listen for storage changes to update the UI in real-time
  browser.storage.onChanged.addListener((changes, areaName) => {
    if (areaName === 'local' && changes.folders) {
      loadFolders();
    }
  });
});