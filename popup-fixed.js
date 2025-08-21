console.log('Popup script starting...');

// Global error handler
window.addEventListener('error', (e) => {
  console.error('Global error:', e.error);
});

document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM Content Loaded - Initializing RCP Popup');
  
  try {
    // Get all DOM elements with error handling
    const elements = {
      folderList: document.getElementById('folderList'),
      addFolderBtn: document.getElementById('addFolderBtn'),
      addPromptBtn: document.getElementById('addPromptBtn'),
      saveSelectionBtn: document.getElementById('saveSelectionBtn'),
      discoverBtn: document.getElementById('discoverBtn'),
      resetBtn: document.getElementById('resetBtn'),
      openFullBtn: document.getElementById('openFullBtn'),
      importFileBtn: document.getElementById('importFileBtn'),
      manageCategoriesBtn: document.getElementById('manageCategoriesBtn'),
      fileInput: document.getElementById('fileInput'),
      searchInput: document.getElementById('search-input'),
      statsText: document.getElementById('stats-text'),
      compactToggle: document.getElementById('compact-toggle')
    };
    
    // Debug: Check if all elements are found
    console.log('Element check results:');
    Object.keys(elements).forEach(key => {
      console.log(`${key}:`, elements[key]);
      if (!elements[key] && !['folderList', 'statsText'].includes(key)) {
        console.warn(`Warning: ${key} not found`);
      }
    });
    
    // Check if critical elements are missing
    const criticalElements = ['addFolderBtn', 'addPromptBtn', 'saveSelectionBtn', 'importFileBtn'];
    const missingCritical = criticalElements.filter(key => !elements[key]);
    
    if (missingCritical.length > 0) {
      console.error('Critical elements not found:', missingCritical);
      // Try to add fallback buttons
      addFallbackButtons();
      return;
    }
    
    // Global variables
    let folders = [];
    let isCompactMode = true;
    let searchTerm = '';
    let expandedFolders = new Set();

    // Initialize the application
    initializeApp(elements);
    
  } catch (error) {
    console.error('Error during DOMContentLoaded:', error);
    addFallbackButtons();
  }
});

// Add fallback buttons if main ones don't work
function addFallbackButtons() {
  console.log('Adding fallback buttons');
  
  const fallbackContainer = document.createElement('div');
  fallbackContainer.style.cssText = 'margin: 10px 0; padding: 10px; border: 1px solid #ffd700; border-radius: 4px;';
  fallbackContainer.innerHTML = '<h3 style="color: #ffd700; margin: 0 0 10px 0;">Fallback Buttons</h3>';
  
  const buttons = [
    { id: 'fallback-add-folder', text: '+ Add Folder', action: () => alert('Add Folder clicked') },
    { id: 'fallback-add-prompt', text: '+ Add Prompt', action: () => alert('Add Prompt clicked') },
    { id: 'fallback-import', text: '📁 Import File', action: () => alert('Import File clicked') },
    { id: 'fallback-save', text: '💾 Save Selection', action: () => alert('Save Selection clicked') }
  ];
  
  buttons.forEach(btn => {
    const button = document.createElement('button');
    button.id = btn.id;
    button.textContent = btn.text;
    button.style.cssText = `
      background: linear-gradient(135deg, #8b0000 0%, #dc143c 100%);
      color: #ffd700;
      border: 1px solid #ffd700;
      padding: 8px 12px;
      margin: 2px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 12px;
    `;
    button.addEventListener('click', btn.action);
    fallbackContainer.appendChild(button);
  });
  
  document.body.insertBefore(fallbackContainer, document.body.firstChild);
}

// Initialize the application
function initializeApp(elements) {
  console.log('Initializing application with elements:', elements);
  
  // Load compact mode preference
  loadCompactMode(elements.compactToggle);
  
  // Load folders and prompts
  loadFolders(elements);
  
  // Add event listeners to all buttons
  setupEventListeners(elements);
}

// Setup all event listeners
function setupEventListeners(elements) {
  console.log('Setting up event listeners');
  
  // Add folder button functionality
  if (elements.addFolderBtn) {
    elements.addFolderBtn.addEventListener('click', () => {
      console.log('Add Folder button clicked');
      const folderName = prompt('Enter folder name:');
      if (folderName && folderName.trim()) {
        createFolder(folderName.trim(), elements);
      }
    });
  }
  
  // Add prompt button functionality
  if (elements.addPromptBtn) {
    elements.addPromptBtn.addEventListener('click', () => {
      console.log('Add Prompt button clicked');
      const promptText = prompt('Enter prompt text:');
      if (promptText && promptText.trim()) {
        const promptTitle = prompt('Enter prompt title (optional):') || 'Untitled Prompt';
        createPrompt(promptTitle.trim(), promptText.trim(), elements);
      }
    });
  }
  
  // Save selection button functionality
  if (elements.saveSelectionBtn) {
    elements.saveSelectionBtn.addEventListener('click', async () => {
      console.log('Save Selection button clicked');
      await handleSaveSelection(elements);
    });
  }
  
  // Discover prompts button functionality
  if (elements.discoverBtn) {
    elements.discoverBtn.addEventListener('click', () => {
      console.log('Discover button clicked');
      showDiscoveryOptions(elements);
    });
  }
  
  // Reset library button functionality
  if (elements.resetBtn) {
    elements.resetBtn.addEventListener('click', () => {
      console.log('Reset button clicked');
      if (confirm('Are you sure you want to reset the preloaded prompt library?')) {
        resetPreloadedPrompts(elements);
      }
    });
  }

  // Open full UI button functionality
  if (elements.openFullBtn) {
    elements.openFullBtn.addEventListener('click', () => {
      console.log('Open Full UI button clicked');
      browser.tabs.create({ url: browser.runtime.getURL('full-ui.html') });
      window.close();
    });
  }
  
  // Import file button functionality
  if (elements.importFileBtn) {
    elements.importFileBtn.addEventListener('click', () => {
      console.log('Import File button clicked');
      showImportFileModal(elements);
    });
  }
  
  // Manage categories button functionality
  if (elements.manageCategoriesBtn) {
    elements.manageCategoriesBtn.addEventListener('click', () => {
      console.log('Manage Categories button clicked');
      showCategoryManagementModal(elements);
    });
  }
  
  // File input change handler
  if (elements.fileInput) {
    elements.fileInput.addEventListener('change', (e) => {
      console.log('File input changed');
      handleFileImport(e.target.files, elements);
    });
  }
  
  // Search functionality
  if (elements.searchInput) {
    elements.searchInput.addEventListener('input', (e) => {
      console.log('Search input changed');
      searchTerm = e.target.value.toLowerCase();
      renderFolders(elements);
    });
  }

  // Compact mode toggle
  if (elements.compactToggle) {
    elements.compactToggle.addEventListener('click', () => {
      console.log('Compact toggle clicked');
      isCompactMode = !isCompactMode;
      elements.compactToggle.classList.toggle('active', isCompactMode);
      browser.storage.local.set({ compactMode: isCompactMode });
      renderFolders(elements);
    });
  }
  
  console.log('All event listeners set up');
}

// Function to load compact mode preference
async function loadCompactMode(compactToggle) {
  try {
    const result = await browser.storage.local.get(['compactMode']);
    isCompactMode = result.compactMode !== false; // Default to true
    if (compactToggle) {
      compactToggle.classList.toggle('active', isCompactMode);
    }
  } catch (error) {
    console.error('Error loading compact mode preference:', error);
  }
}

// Function to load folders and prompts
async function loadFolders(elements) {
  try {
    console.log('Loading folders...');
    const response = await browser.runtime.sendMessage({ action: 'getFolders' });
    folders = response.folders || [];
    console.log('Folders loaded:', folders);
    
    updateStats(elements);
    renderFolders(elements);
  } catch (error) {
    console.error('Error loading folders:', error);
    if (elements.folderList) {
      elements.folderList.innerHTML = '<div style="color: #ffcc00; padding: 20px; text-align: center;">Error loading folders</div>';
    }
  }
}

// Function to update statistics
function updateStats(elements) {
  if (elements.statsText) {
    const totalPrompts = folders.reduce((sum, folder) => sum + (folder.prompts ? folder.prompts.length : 0), 0);
    elements.statsText.textContent = `${folders.length} folders, ${totalPrompts} prompts`;
  }
}

// Function to render folders
function renderFolders(elements) {
  if (!elements.folderList) return;
  
  console.log('Rendering folders...');
  
  if (folders.length === 0) {
    elements.folderList.innerHTML = `
      <div style="text-align: center; color: #ffcc00; padding: 30px 15px;">
        <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.5;">📁</div>
        <h3 style="margin: 0 0 8px 0; color: #ffd700;">No folders yet</h3>
        <p style="margin: 0; font-size: 12px;">Create your first folder to get started</p>
      </div>
    `;
    return;
  }
  
  // Simple folder rendering for testing
  elements.folderList.innerHTML = folders.map(folder => `
    <div style="margin-bottom: 8px; border: 1px solid #ffd700; border-radius: 6px; padding: 8px; cursor: pointer;">
      <div style="color: #ffd700; font-weight: bold;">${folder.name}</div>
      <div style="color: #ffcc00; font-size: 10px;">${folder.prompts ? folder.prompts.length : 0} prompts</div>
    </div>
  `).join('');
}

// Function to create folder
async function createFolder(folderName, elements) {
  try {
    console.log('Creating folder:', folderName);
    const response = await browser.runtime.sendMessage({
      action: 'createFolder',
      name: folderName
    });
    
    if (response.success) {
      console.log('Folder created successfully');
      showNotification('Folder created successfully!', 'success');
      loadFolders(elements);
    } else {
      console.error('Failed to create folder:', response.error);
      showNotification('Failed to create folder: ' + (response.error || 'Unknown error'), 'error');
    }
  } catch (error) {
    console.error('Error creating folder:', error);
    showNotification('Error creating folder. Please try again.', 'error');
  }
}

// Function to create prompt
async function createPrompt(title, text, elements) {
  try {
    console.log('Creating prompt:', title);
    // For now, just show a notification
    showNotification('Prompt creation would be implemented here', 'info');
  } catch (error) {
    console.error('Error creating prompt:', error);
    showNotification('Error creating prompt. Please try again.', 'error');
  }
}

// Function to handle save selection
async function handleSaveSelection(elements) {
  try {
    showNotification('Save selection functionality would be implemented here', 'info');
  } catch (error) {
    console.error('Error handling save selection:', error);
    showNotification('Failed to save selection. Please try again.', 'error');
  }
}

// Function to show import file modal
function showImportFileModal(elements) {
  console.log('Showing import file modal');
  showNotification('Import functionality would be implemented here', 'info');
}

// Function to show notification
function showNotification(message, type = 'info') {
  console.log(`Showing notification: ${message} (${type})`);
  
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 16px;
    border-radius: 6px;
    color: white;
    font-weight: 500;
    z-index: 10001;
    max-width: 280px;
    word-wrap: break-word;
    font-size: 12px;
    border: 1px solid #ffd700;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  `;
  
  // Set background color based on type
  switch (type) {
    case 'success':
      notification.style.background = 'linear-gradient(135deg, #ffd700 0%, #ffcc00 100%)';
      notification.style.color = '#660000';
      break;
    case 'error':
      notification.style.background = 'linear-gradient(135deg, #ff6b6b 0%, #dc143c 100%)';
      notification.style.color = '#ffd700';
      break;
    default:
      notification.style.background = 'linear-gradient(135deg, #4dabf7 0%, #1a237e 100%)';
      notification.style.color = '#ffd700';
  }
  
  notification.textContent = message;
  document.body.appendChild(notification);
  
  // Remove notification after 3 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 3000);
}

// Placeholder functions for other features
function showDiscoveryOptions(elements) {
  showNotification('Discovery options would be implemented here', 'info');
}

function resetPreloadedPrompts(elements) {
  showNotification('Reset functionality would be implemented here', 'info');
}

function showCategoryManagementModal(elements) {
  showNotification('Category management would be implemented here', 'info');
}

function handleFileImport(files, elements) {
  showNotification('File import handling would be implemented here', 'info');
}

console.log('Popup script loaded successfully');