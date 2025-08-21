/**
 * RCP Firefox Extension - Robust Popup Implementation
 * 
 * This implementation fixes all the issues from the previous version:
 * - No global event listeners that interfere with file inputs
 * - Clean event handling with proper cleanup
 * - Simplified file input management
 * - Robust modal system
 * - Proper error handling
 */

console.log('RCP Popup script starting...');

// Main application class for better organization
class RCPopup {
  constructor() {
    this.folders = [];
    this.isCompactMode = true;
    this.searchTerm = '';
    this.expandedFolders = new Set();
    this.isManageMode = false;
    this.currentModal = null;
    
    // Cache DOM elements
    this.elements = {};
    this.initializeElements();
  }

  // Initialize and cache all DOM elements
  initializeElements() {
    const elementIds = [
      'folderList', 'addFolderBtn', 'addPromptBtn', 'saveSelectionBtn',
      'discoverBtn', 'resetBtn', 'openFullBtn', 'importFileBtn',
      'manageCategoriesBtn', 'debugToggleBtn', 'fileInput',
      'debugFileInput', 'debugOutput', 'debug-file-input',
      'search-input', 'stats-text', 'compact-toggle'
    ];

    elementIds.forEach(id => {
      this.elements[id] = document.getElementById(id);
    });

    console.log('Element initialization complete:', 
      Object.keys(this.elements).filter(key => this.elements[key]).length, 
      'elements found');
  }

  // Initialize the application
  async init() {
    try {
      console.log('Initializing RCP Popup...');
      
      // Validate critical elements
      if (!this.validateCriticalElements()) {
        throw new Error('Critical elements missing');
      }

      // Load preferences and data
      await this.loadPreferences();
      await this.loadData();

      // Setup event listeners
      this.setupEventListeners();

      // Render initial UI
      this.updateStats();
      this.renderFolders();

      console.log('RCP Popup initialized successfully');
    } catch (error) {
      console.error('Failed to initialize RCP Popup:', error);
      this.showNotification('Failed to initialize extension. Please reload.', 'error');
      this.showFallbackUI();
    }
  }

  // Validate that critical elements exist
  validateCriticalElements() {
    const critical = ['addFolderBtn', 'addPromptBtn', 'saveSelectionBtn', 'importFileBtn'];
    const missing = critical.filter(id => !this.elements[id]);
    
    if (missing.length > 0) {
      console.error('Missing critical elements:', missing);
      return false;
    }
    return true;
  }

  // Load user preferences
  async loadPreferences() {
    try {
      const result = await browser.storage.local.get(['compactMode']);
      this.isCompactMode = result.compactMode !== false; // Default to true
      
      if (this.elements['compact-toggle']) {
        this.elements['compact-toggle'].classList.toggle('active', this.isCompactMode);
      }
    } catch (error) {
      console.error('Error loading preferences:', error);
    }
  }

  // Load folders and prompts from storage
  async loadData() {
    try {
      console.log('Loading folders and prompts...');
      const response = await browser.runtime.sendMessage({ action: 'getFolders' });
      this.folders = response.folders || [];
      console.log('Loaded', this.folders.length, 'folders');
    } catch (error) {
      console.error('Error loading data:', error);
      this.folders = [];
    }
  }

  // Setup all event listeners with proper error handling
  setupEventListeners() {
    console.log('Setting up event listeners...');

    // Button event listeners
    this.addButtonListener('addFolderBtn', () => this.handleAddFolder());
    this.addButtonListener('addPromptBtn', () => this.handleAddPrompt());
    this.addButtonListener('saveSelectionBtn', () => this.handleSaveSelection());
    this.addButtonListener('discoverBtn', () => this.showDiscoveryOptions());
    this.addButtonListener('resetBtn', () => this.handleReset());
    this.addButtonListener('openFullBtn', () => this.handleOpenFullUI());
    this.addButtonListener('importFileBtn', () => this.showImportFileModal());
    this.addButtonListener('manageCategoriesBtn', () => this.toggleManageMode());

    // Debug functionality
    if (this.elements['debugToggleBtn']) {
      this.addButtonListener('debugToggleBtn', () => this.toggleDebugMode());
    }

    // File input handling - NO GLOBAL LISTENERS
    if (this.elements['fileInput']) {
      this.elements['fileInput'].addEventListener('change', (e) => {
        this.handleFileSelection(e.target.files);
      });
    }

    // Debug file input
    if (this.elements['debugFileInput']) {
      this.elements['debugFileInput'].addEventListener('change', (e) => {
        this.handleDebugFileSelection(e.target.files);
      });
    }

    // Search functionality
    if (this.elements['search-input']) {
      this.elements['search-input'].addEventListener('input', (e) => {
        this.searchTerm = e.target.value.toLowerCase();
        this.renderFolders();
      });
    }

    // Compact mode toggle
    if (this.elements['compact-toggle']) {
      this.addButtonListener('compact-toggle', () => this.toggleCompactMode());
    }

    console.log('Event listeners setup complete');
  }

  // Helper method to add button listeners with error handling
  addButtonListener(elementId, handler) {
    const element = this.elements[elementId];
    if (element) {
      element.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        try {
          handler();
        } catch (error) {
          console.error(`Error in ${elementId} handler:`, error);
          this.showNotification('An error occurred. Please try again.', 'error');
        }
      });
    }
  }

  // Handle folder creation
  async handleAddFolder() {
    const folderName = prompt('Enter folder name:');
    if (folderName && folderName.trim()) {
      try {
        const response = await browser.runtime.sendMessage({
          action: 'createFolder',
          name: folderName.trim()
        });

        if (response.success) {
          this.showNotification('Folder created successfully!', 'success');
          await this.loadData();
          this.updateStats();
          this.renderFolders();
        } else {
          this.showNotification('Failed to create folder: ' + (response.error || 'Unknown error'), 'error');
        }
      } catch (error) {
        console.error('Error creating folder:', error);
        this.showNotification('Error creating folder. Please try again.', 'error');
      }
    }
  }

  // Handle prompt creation
  async handleAddPrompt() {
    const promptText = prompt('Enter prompt text:');
    if (promptText && promptText.trim()) {
      const promptTitle = prompt('Enter prompt title (optional):') || 'Untitled Prompt';
      
      try {
        // For now, show a notification - would need folder selection logic
        this.showNotification('Prompt creation would be implemented here', 'info');
      } catch (error) {
        console.error('Error creating prompt:', error);
        this.showNotification('Error creating prompt. Please try again.', 'error');
      }
    }
  }

  // Handle save selection
  async handleSaveSelection() {
    try {
      const [activeTab] = await browser.tabs.query({ active: true, currentWindow: true });
      
      if (!activeTab || !activeTab.id) {
        this.showNotification('No active tab found.', 'error');
        return;
      }

      const results = await browser.scripting.executeScript({
        target: { tabId: activeTab.id },
        func: () => {
          const selection = window.getSelection();
          return selection ? selection.toString().trim() : '';
        }
      });

      const selectedText = results && results[0] ? results[0].result : '';
      
      if (!selectedText) {
        this.showNotification('Please highlight some text on the page first, then click this button.', 'info');
        return;
      }

      await browser.storage.local.set({ 
        pendingPromptText: selectedText,
        pendingPromptSource: 'popup'
      });

      await browser.scripting.executeScript({
        target: { tabId: activeTab.id },
        files: ['category-selector.js']
      });

      window.close();
      
    } catch (error) {
      console.error('Error handling save selection:', error);
      this.showNotification('Failed to save selection. Please try again.', 'error');
    }
  }

  // Handle reset
  handleReset() {
    if (confirm('Are you sure you want to reset the prompt library? This will remove all prompts and folders.')) {
      // Reset functionality would be implemented here
      this.showNotification('Reset functionality would be implemented here', 'info');
    }
  }

  // Handle opening full UI
  handleOpenFullUI() {
    browser.tabs.create({ url: browser.runtime.getURL('full-ui.html') });
    window.close();
  }

  // Toggle compact mode
  toggleCompactMode() {
    this.isCompactMode = !this.isCompactMode;
    this.elements['compact-toggle'].classList.toggle('active', this.isCompactMode);
    browser.storage.local.set({ compactMode: this.isCompactMode });
    this.renderFolders();
  }

  // Toggle manage mode
  toggleManageMode() {
    this.isManageMode = !this.isManageMode;
    this.elements['manageCategoriesBtn'].textContent = 
      this.isManageMode ? '📋 View Mode' : '⚙️ Manage';
    this.renderFolders();
  }

  // Toggle debug mode
  toggleDebugMode() {
    const debugDiv = this.elements['debug-file-input'];
    const debugBtn = this.elements['debugToggleBtn'];
    
    if (debugDiv && debugBtn) {
      const isVisible = debugDiv.style.display !== 'none';
      debugDiv.style.display = isVisible ? 'none' : 'block';
      debugBtn.textContent = isVisible ? '🐛 Debug' : '🔍 Hide Debug';
    }
  }

  // Handle file selection - CLEAN IMPLEMENTATION
  handleFileSelection(files) {
    console.log('File selection handled:', files);
    if (files && files.length > 0) {
      // Store files in a controlled manner
      this.selectedFiles = files;
      this.updateSelectedFilesDisplay();
    }
  }

  // Handle debug file selection
  handleDebugFileSelection(files) {
    console.log('Debug file selection:', files);
    const debugOutput = this.elements['debugOutput'];
    if (debugOutput) {
      if (files && files.length > 0) {
        const fileNames = Array.from(files).map(file => file.name).join(', ');
        debugOutput.textContent = `Selected: ${fileNames}`;
      } else {
        debugOutput.textContent = '';
      }
    }
  }

  // Update selected files display - SIMPLIFIED
  updateSelectedFilesDisplay() {
    const selectedFilesDiv = document.getElementById('selected-files');
    if (!selectedFilesDiv) return;

    if (this.selectedFiles && this.selectedFiles.length > 0) {
      const fileNames = Array.from(this.selectedFiles).map(file => file.name).join(', ');
      selectedFilesDiv.textContent = `Selected: ${fileNames}`;
    } else {
      selectedFilesDiv.textContent = '';
    }
  }

  // Show discovery options modal
  showDiscoveryOptions() {
    const modal = this.createModal('discovery-modal', this.getDiscoveryOptionsHTML());
    this.setupDiscoveryModalListeners(modal);
  }

  // Get discovery options HTML
  getDiscoveryOptionsHTML() {
    return `
      <div style="padding: 20px; background: #f9fafb; border-radius: 8px; margin: 10px 0;">
        <h3 style="margin: 0 0 15px 0; color: #374151;">🔍 Discover New Prompts</h3>
        <p style="margin: 0 0 15px 0; color: #6b7280; font-size: 12px;">
          Get fresh prompts from legitimate sources. Choose a category:
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
          <button class="discovery-btn" data-category="writing" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">✍️ Writing</button>
          <button class="discovery-btn" data-category="coding" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">💻 Coding</button>
          <button class="discovery-btn" data-category="analysis" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">📊 Analysis</button>
          <button class="discovery-btn" data-category="business" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">💼 Business</button>
          <button class="discovery-btn" data-category="education" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">🎓 Education</button>
          <button class="discovery-btn" data-category="creative" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">🎨 Creative</button>
          <button class="discovery-btn" data-category="communication" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">💬 Communication</button>
          <button class="discovery-btn" data-category="problems" style="padding: 6px; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-size: 11px;">🧩 Problem Solving</button>
        </div>
        <div style="margin-top: 12px;">
          <button class="discovery-btn" data-category="all" style="width: 100%; padding: 8px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 500; font-size: 11px;">🎯 Discover All Categories</button>
        </div>
        <div style="margin-top: 8px;">
          <button id="close-discovery-btn" style="width: 100%; padding: 6px; background: #6b7280; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 10px;">Cancel</button>
        </div>
      </div>
    `;
  }

  // Setup discovery modal listeners
  setupDiscoveryModalListeners(modal) {
    // Discovery buttons
    const discoveryBtns = modal.querySelectorAll('.discovery-btn');
    discoveryBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const category = btn.getAttribute('data-category');
        this.closeModal('discovery-modal');
        this.discoverPrompts(category);
      });
    });

    // Close button
    const closeBtn = modal.querySelector('#close-discovery-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.closeModal('discovery-modal');
      });
    }

    // Close on outside click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        e.preventDefault();
        e.stopPropagation();
        this.closeModal('discovery-modal');
      }
    });
  }

  // Show import file modal - ROBUST IMPLEMENTATION
  showImportFileModal() {
    console.log('Showing import file modal');
    
    // Close any existing modal
    this.closeCurrentModal();

    const modal = this.createModal('import-file-modal', this.getImportModalHTML());
    this.setupImportModalListeners(modal);
  }

  // Get import modal HTML
  getImportModalHTML() {
    return `
      <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000; display: flex; align-items: center; justify-content: center;">
        <div style="background: linear-gradient(135deg, #1a0000 0%, #330000 100%); border: 2px solid #ffd700; border-radius: 12px; padding: 24px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto; box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #ffd700; font-size: 18px; font-weight: 600; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">Import Files</h3>
            <button id="close-import-modal" style="background: none; border: none; color: #ffd700; font-size: 24px; cursor: pointer; padding: 4px; border-radius: 4px;">×</button>
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
              <input type="file" id="modal-file-input" accept=".md,.txt,.json" multiple style="width: 100%; padding: 8px; background: linear-gradient(135deg, rgba(26,0,0,0.8) 0%, rgba(51,0,0,0.9) 100%); color: #ffd700; border: 1px solid #ffd700; border-radius: 4px; margin-bottom: 8px;">
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
  }

  // Setup import modal listeners - CLEAN IMPLEMENTATION
  setupImportModalListeners(modal) {
    // Close button
    const closeBtn = modal.querySelector('#close-import-modal');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.closeModal('import-file-modal');
      });
    }

    // Cancel button
    const cancelBtn = modal.querySelector('#cancel-import-btn');
    if (cancelBtn) {
      cancelBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.closeModal('import-file-modal');
      });
    }

    // Process button
    const processBtn = modal.querySelector('#process-import-btn');
    if (processBtn) {
      processBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.processImportFiles();
      });
    }

    // Modal file input - SIMPLE DIRECT HANDLING
    const modalFileInput = modal.querySelector('#modal-file-input');
    if (modalFileInput) {
      modalFileInput.addEventListener('change', (e) => {
        console.log('Modal file input changed');
        this.selectedFiles = e.target.files;
        this.updateSelectedFilesDisplay();
      });
    }

    // Close on outside click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        e.preventDefault();
        e.stopPropagation();
        this.closeModal('import-file-modal');
      }
    });

    // Load categories
    this.loadCategoriesIntoSelect();
  }

  // Load categories into select dropdown
  loadCategoriesIntoSelect() {
    const select = document.getElementById('import-category-select');
    if (!select) return;

    // Clear existing options
    select.innerHTML = '<option value="">Choose a category...</option>';

    // Add folder options
    this.folders.forEach(folder => {
      const option = document.createElement('option');
      option.value = folder.name;
      option.textContent = folder.name;
      select.appendChild(option);
    });
  }

  // Process import files - SIMPLIFIED
  async processImportFiles() {
    const categorySelect = document.getElementById('import-category-select');
    const newCategoryInput = document.getElementById('import-new-category');

    if (!this.selectedFiles || this.selectedFiles.length === 0) {
      this.showNotification('Please select files to import.', 'error');
      return;
    }

    let targetCategory = categorySelect.value;
    const newCategory = newCategoryInput.value.trim();

    if (!targetCategory && !newCategory) {
      this.showNotification('Please select a category or create a new one.', 'error');
      return;
    }

    if (newCategory) {
      targetCategory = newCategory;
    }

    // For now, show a notification
    this.showNotification(`Would import ${this.selectedFiles.length} files into "${targetCategory}"`, 'info');
    
    // Clear and close
    this.selectedFiles = null;
    this.closeModal('import-file-modal');
  }

  // Discover prompts
  async discoverPrompts(category) {
    this.showNotification(`Discovering ${category} prompts...`, 'info');
    
    try {
      const response = await browser.runtime.sendMessage({ 
        action: 'discoverPrompts', 
        category: category 
      });
      
      if (response.success) {
        this.showNotification(`Discovered ${response.count} new ${category} prompts!`, 'success');
        await this.loadData();
        this.updateStats();
        this.renderFolders();
      } else {
        this.showNotification('Failed to discover prompts: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error discovering prompts:', error);
      this.showNotification('Error discovering prompts. Please try again.', 'error');
    }
  }

  // Modal management methods
  createModal(id, html) {
    // Close existing modal
    this.closeCurrentModal();

    const modal = document.createElement('div');
    modal.id = id;
    modal.innerHTML = html;
    document.body.appendChild(modal);
    
    this.currentModal = modal;
    return modal;
  }

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.remove();
      if (this.currentModal === modal) {
        this.currentModal = null;
      }
    }
  }

  closeCurrentModal() {
    if (this.currentModal) {
      this.currentModal.remove();
      this.currentModal = null;
    }
  }

  // Update statistics display
  updateStats() {
    const statsText = this.elements['stats-text'];
    if (statsText) {
      const totalPrompts = this.folders.reduce((sum, folder) => 
        sum + (folder.prompts ? folder.prompts.length : 0), 0);
      statsText.textContent = `${this.folders.length} folders, ${totalPrompts} prompts`;
    }
  }

  // Render folders in the UI
  renderFolders() {
    const folderList = this.elements['folderList'];
    if (!folderList) return;

    if (this.folders.length === 0) {
      folderList.innerHTML = `
        <div style="text-align: center; color: #ffcc00; padding: 30px 15px;">
          <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.5;">📁</div>
          <h3 style="margin: 0 0 8px 0; color: #ffd700;">No folders yet</h3>
          <p style="margin: 0; font-size: 12px;">Create your first folder to get started</p>
        </div>
      `;
      return;
    }

    // Simple folder rendering
    folderList.innerHTML = this.folders.map(folder => `
      <div style="margin-bottom: 8px; border: 1px solid #ffd700; border-radius: 6px; padding: 8px; cursor: pointer;">
        <div style="color: #ffd700; font-weight: bold;">${folder.name}</div>
        <div style="color: #ffcc00; font-size: 10px;">${folder.prompts ? folder.prompts.length : 0} prompts</div>
      </div>
    `).join('');
  }

  // Show notification to user
  showNotification(message, type = 'info') {
    console.log(`Notification: ${message} (${type})`);
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
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

  // Show fallback UI if initialization fails
  showFallbackUI() {
    const fallbackContainer = document.createElement('div');
    fallbackContainer.style.cssText = 'margin: 10px 0; padding: 10px; border: 1px solid #ffd700; border-radius: 4px;';
    fallbackContainer.innerHTML = '<h3 style="color: #ffd700; margin: 0 0 10px 0;">Extension Error</h3><p style="color: #ffcc00; margin: 0;">Please reload the extension.</p>';
    
    document.body.insertBefore(fallbackContainer, document.body.firstChild);
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
  console.log('DOM Content Loaded - Starting RCP Popup');
  
  try {
    const popup = new RCPopup();
    await popup.init();
    console.log('RCP Popup started successfully');
  } catch (error) {
    console.error('Failed to start RCP Popup:', error);
  }
});

console.log('RCP Popup script loaded');