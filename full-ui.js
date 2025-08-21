document.addEventListener('DOMContentLoaded', () => {
  // Global variables
  let folders = [];
  let prompts = [];
  let currentFolder = null;
  let currentView = 'grid';
  let searchTerm = '';
  let sortBy = 'newest';

  // DOM elements
  const elements = {
    totalFolders: document.getElementById('totalFolders'),
    totalPrompts: document.getElementById('totalPrompts'),
    totalSelections: document.getElementById('totalSelections'),
    searchInput: document.getElementById('searchInput'),
    folderList: document.getElementById('folderList'),
    promptGrid: document.getElementById('promptGrid'),
    contentTitle: document.getElementById('contentTitle'),
    sortSelect: document.getElementById('sortSelect'),
    addFolderBtn: document.getElementById('addFolderBtn'),
    addPromptBtn: document.getElementById('addPromptBtn'),
    saveSelectionBtn: document.getElementById('saveSelectionBtn'),
    discoverBtn: document.getElementById('discoverBtn'),
    importBtn: document.getElementById('importBtn'),
    exportBtn: document.getElementById('exportBtn'),
    resetBtn: document.getElementById('resetBtn'),
    addFolderModal: document.getElementById('addFolderModal'),
    addPromptModal: document.getElementById('addPromptModal'),
    addFolderForm: document.getElementById('addFolderForm'),
    addPromptForm: document.getElementById('addPromptForm'),
    promptFolderSelect: document.getElementById('promptFolderSelect')
  };

  // Initialize the application
  async function init() {
    await loadData();
    setupEventListeners();
    updateStats();
    renderFolders();
    renderPrompts();
  }

  // Load data from storage
  async function loadData() {
    try {
      const response = await browser.runtime.sendMessage({ action: 'getFolders' });
      folders = response.folders || [];
      
      // Flatten all prompts for easier manipulation
      prompts = [];
      folders.forEach(folder => {
        if (folder.prompts) {
          folder.prompts.forEach(prompt => {
            prompts.push({ ...prompt, folderId: folder.id, folderName: folder.name });
          });
        }
      });
    } catch (error) {
      console.error('Error loading data:', error);
      showNotification('Error loading data. Please refresh the page.', 'error');
    }
  }

  // Setup event listeners
  function setupEventListeners() {
    // Search functionality
    elements.searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.toLowerCase();
      renderPrompts();
    });

    // Sort functionality
    elements.sortSelect.addEventListener('change', (e) => {
      sortBy = e.target.value;
      renderPrompts();
    });

    // View toggle
    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentView = e.target.dataset.view;
        renderPrompts();
      });
    });

    // Action buttons
    elements.addFolderBtn.addEventListener('click', () => openModal('addFolderModal'));
    elements.addPromptBtn.addEventListener('click', () => openModal('addPromptModal'));
    elements.saveSelectionBtn.addEventListener('click', handleSaveSelection);
    elements.discoverBtn.addEventListener('click', handleDiscover);
    elements.importBtn.addEventListener('click', handleImport);
    elements.exportBtn.addEventListener('click', handleExport);
    elements.resetBtn.addEventListener('click', handleReset);

    // Form submissions
    elements.addFolderForm.addEventListener('submit', handleAddFolder);
    elements.addPromptForm.addEventListener('submit', handleAddPrompt);

    // Modal close buttons
    const closeAddFolderModal = document.getElementById('closeAddFolderModal');
    const cancelAddFolderModal = document.getElementById('cancelAddFolderModal');
    const closeAddPromptModal = document.getElementById('closeAddPromptModal');
    const cancelAddPromptModal = document.getElementById('cancelAddPromptModal');

    if (closeAddFolderModal) {
      closeAddFolderModal.addEventListener('click', () => closeModal('addFolderModal'));
    }
    if (cancelAddFolderModal) {
      cancelAddFolderModal.addEventListener('click', () => closeModal('addFolderModal'));
    }
    if (closeAddPromptModal) {
      closeAddPromptModal.addEventListener('click', () => closeModal('addPromptModal'));
    }
    if (cancelAddPromptModal) {
      cancelAddPromptModal.addEventListener('click', () => closeModal('addPromptModal'));
    }

    // Close modals when clicking outside
    document.querySelectorAll('.modal').forEach(modal => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          closeModal(modal.id);
        }
      });
    });
  }

  // Update statistics
  function updateStats() {
    elements.totalFolders.textContent = folders.length;
    elements.totalPrompts.textContent = prompts.length;
    
    // Count selection-based prompts
    const selectionCount = prompts.filter(p => p.source === 'selection').length;
    elements.totalSelections.textContent = selectionCount;
  }

  // Render folders in sidebar
  function renderFolders() {
    if (folders.length === 0) {
      elements.folderList.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📁</div>
          <h3>No folders yet</h3>
          <p>Create your first folder to get started</p>
        </div>
      `;
      return;
    }

    elements.folderList.innerHTML = folders.map(folder => {
      const folderPrompts = prompts.filter(p => p.folderId === folder.id);
      const isActive = currentFolder === folder.id;
      
      return `
        <div class="folder-item ${isActive ? 'active' : ''}" data-folder-id="${folder.id}">
          <div class="folder-info">
            <div class="folder-icon">📁</div>
            <div class="folder-name">${escapeHtml(folder.name)}</div>
          </div>
          <div class="folder-count">${folderPrompts.length}</div>
        </div>
      `;
    }).join('');

    // Add click listeners
    elements.folderList.querySelectorAll('.folder-item').forEach(item => {
      item.addEventListener('click', () => {
        const folderId = item.dataset.folderId;
        selectFolder(folderId);
      });
    });
  }

  // Select a folder
  function selectFolder(folderId) {
    currentFolder = folderId;
    
    // Update active state
    elements.folderList.querySelectorAll('.folder-item').forEach(item => {
      item.classList.toggle('active', item.dataset.folderId === folderId);
    });

    // Update content title
    const folder = folders.find(f => f.id === folderId);
    elements.contentTitle.textContent = folder ? escapeHtml(folder.name) : 'All Prompts';

    // Re-render prompts
    renderPrompts();
  }

  // Render prompts
  function renderPrompts() {
    let filteredPrompts = prompts;

    // Filter by current folder
    if (currentFolder) {
      filteredPrompts = filteredPrompts.filter(p => p.folderId === currentFolder);
    }

    // Filter by search term
    if (searchTerm) {
      filteredPrompts = filteredPrompts.filter(p => 
        p.title.toLowerCase().includes(searchTerm) || 
        p.text.toLowerCase().includes(searchTerm) ||
        (p.folderName && p.folderName.toLowerCase().includes(searchTerm))
      );
    }

    // Sort prompts
    filteredPrompts = sortPrompts(filteredPrompts, sortBy);

    if (filteredPrompts.length === 0) {
      elements.promptGrid.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📝</div>
          <h3>No prompts found</h3>
          <p>Try adjusting your search or create some prompts</p>
        </div>
      `;
      return;
    }

    // Render based on current view
    if (currentView === 'grid') {
      renderGridView(filteredPrompts);
    } else {
      renderListView(filteredPrompts);
    }
  }

  // Sort prompts
  function sortPrompts(promptsArray, sortMethod) {
    const sorted = [...promptsArray];
    
    switch (sortMethod) {
      case 'newest':
        return sorted.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      case 'oldest':
        return sorted.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
      case 'name':
        return sorted.sort((a, b) => a.title.localeCompare(b.title));
      case 'name-desc':
        return sorted.sort((a, b) => b.title.localeCompare(a.title));
      default:
        return sorted;
    }
  }

  // Render grid view
  function renderGridView(promptsArray) {
    elements.promptGrid.className = 'prompt-grid';
    elements.promptGrid.innerHTML = promptsArray.map(prompt => createPromptCard(prompt)).join('');

    // Add event listeners
    addPromptEventListeners();
  }

  // Render list view
  function renderListView(promptsArray) {
    elements.promptGrid.className = 'prompt-list';
    elements.promptGrid.innerHTML = promptsArray.map(prompt => createPromptListItem(prompt)).join('');

    // Add event listeners
    addPromptEventListeners();
  }

  // Create prompt card HTML
  function createPromptCard(prompt) {
    const sourceBadge = prompt.source ? `<span class="prompt-source">${prompt.source}</span>` : '';
    const truncatedContent = prompt.text.length > 200 ? prompt.text.substring(0, 200) + '...' : prompt.text;
    
    return `
      <div class="prompt-card" data-prompt-id="${prompt.id}">
        <div class="prompt-header">
          <h3 class="prompt-title">${escapeHtml(prompt.title)}</h3>
          ${sourceBadge}
        </div>
        <div class="prompt-content">${escapeHtml(truncatedContent)}</div>
        <div class="prompt-actions">
          <button class="btn-small btn-copy" data-prompt-id="${prompt.id}" data-text="${escapeHtml(prompt.text)}">📋 Copy</button>
          <button class="btn-small btn-edit" data-prompt-id="${prompt.id}">✏️ Edit</button>
          <button class="btn-small btn-delete" data-prompt-id="${prompt.id}">🗑️ Delete</button>
        </div>
        <div class="prompt-meta">
          <span>📁 ${escapeHtml(prompt.folderName || 'Unknown')}</span>
          <span>📅 ${new Date(prompt.timestamp).toLocaleDateString()}</span>
        </div>
      </div>
    `;
  }

  // Create prompt list item HTML
  function createPromptListItem(prompt) {
    const sourceBadge = prompt.source ? `<span class="prompt-source">${prompt.source}</span>` : '';
    
    return `
      <div class="prompt-card" data-prompt-id="${prompt.id}" style="margin-bottom: 12px;">
        <div class="prompt-header">
          <h3 class="prompt-title">${escapeHtml(prompt.title)}</h3>
          ${sourceBadge}
        </div>
        <div class="prompt-content">${escapeHtml(prompt.text)}</div>
        <div class="prompt-actions">
          <button class="btn-small btn-copy" data-prompt-id="${prompt.id}" data-text="${escapeHtml(prompt.text)}">📋 Copy</button>
          <button class="btn-small btn-edit" data-prompt-id="${prompt.id}">✏️ Edit</button>
          <button class="btn-small btn-delete" data-prompt-id="${prompt.id}">🗑️ Delete</button>
        </div>
        <div class="prompt-meta">
          <span>📁 ${escapeHtml(prompt.folderName || 'Unknown')}</span>
          <span>📅 ${new Date(prompt.timestamp).toLocaleDateString()}</span>
        </div>
      </div>
    `;
  }

  // Add event listeners to prompt elements
  function addPromptEventListeners() {
    // Copy buttons
    elements.promptGrid.querySelectorAll('.btn-copy').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const text = e.target.dataset.text;
        copyToClipboard(text);
      });
    });

    // Edit buttons
    elements.promptGrid.querySelectorAll('.btn-edit').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const promptId = e.target.dataset.promptId;
        editPrompt(promptId);
      });
    });

    // Delete buttons
    elements.promptGrid.querySelectorAll('.btn-delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const promptId = e.target.dataset.promptId;
        deletePrompt(promptId);
      });
    });
  }

  // Modal functions
  function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
  }

  function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
  }

  // Handle add folder form submission
  async function handleAddFolder(e) {
    e.preventDefault();
    
    const name = document.getElementById('folderNameInput').value.trim();
    const description = document.getElementById('folderDescInput').value.trim();
    
    if (!name) return;

    try {
      const response = await browser.runtime.sendMessage({ 
        action: 'createFolder', 
        name: name 
      });

      if (response.success) {
        showNotification('Folder created successfully!', 'success');
        closeModal('addFolderModal');
        elements.addFolderForm.reset();
        await loadData();
        updateStats();
        renderFolders();
      } else {
        showNotification('Failed to create folder: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error creating folder:', error);
      showNotification('Error creating folder. Please try again.', 'error');
    }
  }

  // Handle add prompt form submission
  async function handleAddPrompt(e) {
    e.preventDefault();
    
    const title = document.getElementById('promptTitleInput').value.trim();
    const content = document.getElementById('promptContentInput').value.trim();
    const folderId = document.getElementById('promptFolderSelect').value;
    const source = document.getElementById('promptSourceInput').value.trim();
    
    if (!title || !content || !folderId) return;

    try {
      const response = await browser.runtime.sendMessage({ 
        action: 'savePrompt', 
        title: title, 
        text: content, 
        folderId: folderId
      });

      if (response.success) {
        showNotification('Prompt created successfully!', 'success');
        closeModal('addPromptModal');
        elements.addPromptForm.reset();
        await loadData();
        updateStats();
        renderFolders();
        renderPrompts();
      } else {
        showNotification('Failed to create prompt: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error creating prompt:', error);
      showNotification('Error creating prompt. Please try again.', 'error');
    }
  }

  // Handle save selection
  async function handleSaveSelection() {
    try {
      const [activeTab] = await browser.tabs.query({ active: true, currentWindow: true });
      
      if (!activeTab || !activeTab.id) {
        showNotification('No active tab found.', 'error');
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
        showNotification('Please highlight some text on the page first.', 'info');
        return;
      }

      await browser.storage.local.set({ 
        pendingPromptText: selectedText,
        pendingPromptSource: 'full-ui'
      });

      await browser.scripting.executeScript({
        target: { tabId: activeTab.id },
        files: ['category-selector.js']
      });

      showNotification('Selection saved! Check the page for category selection.', 'success');
      
    } catch (error) {
      console.error('Error handling save selection:', error);
      showNotification('Failed to save selection. Please try again.', 'error');
    }
  }

  // Handle discover prompts
  async function handleDiscover() {
    const categories = ['writing', 'coding', 'analysis', 'business', 'education', 'creative', 'communication', 'problems'];
    const category = categories[Math.floor(Math.random() * categories.length)];
    
    try {
      showNotification(`Discovering ${category} prompts...`, 'info');
      
      const response = await browser.runtime.sendMessage({ 
        action: 'discoverPrompts', 
        category: category 
      });
      
      if (response.success) {
        showNotification(`Discovered ${response.count} new ${category} prompts!`, 'success');
        await loadData();
        updateStats();
        renderFolders();
        renderPrompts();
      } else {
        showNotification('Failed to discover prompts: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error discovering prompts:', error);
      showNotification('Error discovering prompts. Please try again.', 'error');
    }
  }

  // Handle import
  function handleImport() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.md,.txt,.json';
    input.multiple = true;
    
    input.onchange = async (e) => {
      e.preventDefault();
      e.stopPropagation();
      const files = Array.from(e.target.files);
      if (!files || files.length === 0) return;
      
      let totalImportCount = 0;
      let processedFiles = 0;
      
      for (const file of files) {
        try {
          const text = await file.text();
          let data;
          
          // Handle different file types
          if (file.name.endsWith('.json')) {
            data = JSON.parse(text);
            
            // Validate import data structure
            if (!Array.isArray(data)) {
              throw new Error('Invalid JSON import file format');
            }
            
            // Process JSON format (array of folders with prompts)
            for (const item of data) {
              if (item.name && Array.isArray(item.prompts)) {
                // Create folder if it doesn't exist
                let folder = folders.find(f => f.name === item.name);
                if (!folder) {
                  const folderResponse = await browser.runtime.sendMessage({
                    action: 'createFolder',
                    name: item.name
                  });
                  
                  if (folderResponse.success) {
                    await loadData();
                    folder = folders.find(f => f.name === item.name);
                  }
                }
                
                if (folder) {
                  // Import prompts
                  for (const prompt of item.prompts) {
                    if (prompt.title && prompt.text) {
                      await browser.runtime.sendMessage({
                        action: 'savePrompt',
                        title: prompt.title,
                        text: prompt.text,
                        folderId: folder.id
                      });
                      totalImportCount++;
                    }
                  }
                }
              }
            }
          } else if (file.name.endsWith('.md') || file.name.endsWith('.txt')) {
            // Process markdown/text files - create a single prompt from the file content
            const fileName = file.name.replace(/\.(md|txt)$/, '');
            const folderName = 'Imported Files';
            
            // Create folder if it doesn't exist
            let folder = folders.find(f => f.name === folderName);
            if (!folder) {
              const folderResponse = await browser.runtime.sendMessage({
                action: 'createFolder',
                name: folderName
              });
              
              if (folderResponse.success) {
                await loadData();
                folder = folders.find(f => f.name === folderName);
              }
            }
            
            if (folder) {
              // Create prompt from file content
              await browser.runtime.sendMessage({
                action: 'savePrompt',
                title: fileName,
                text: text,
                folderId: folder.id
              });
              totalImportCount++;
            }
          }
          
          processedFiles++;
          
        } catch (error) {
          console.error(`Error processing file ${file.name}:`, error);
          showNotification(`Failed to process ${file.name}. ${error.message}`, 'error');
        }
      }
      
      if (totalImportCount > 0) {
        await loadData();
        updateStats();
        renderFolders();
        renderPrompts();
        showNotification(`Successfully imported ${totalImportCount} prompts from ${processedFiles} files!`, 'success');
      } else {
        showNotification('No prompts were imported. Please check your files.', 'error');
      }
    };
    
    // Prevent default behavior and trigger click
    setTimeout(() => {
      input.click();
    }, 100);
  }

  // Handle export
  function handleExport() {
    const exportData = folders.map(folder => ({
      name: folder.name,
      description: folder.description || '',
      prompts: (folder.prompts || []).map(prompt => ({
        title: prompt.title,
        text: prompt.text,
        source: prompt.source || '',
        timestamp: prompt.timestamp
      }))
    }));
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `rcp-export-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Data exported successfully!', 'success');
  }

  // Handle reset
  function handleReset() {
    if (confirm('Are you sure you want to reset the preloaded prompt library? This will remove all preloaded prompts and reload them. Your custom folders and prompts will be preserved.')) {
      resetPreloadedPrompts();
    }
  }

  // Reset preloaded prompts
  async function resetPreloadedPrompts() {
    try {
      showNotification('Resetting preloaded prompt library...', 'info');
      
      const response = await browser.runtime.sendMessage({ 
        action: 'resetPreloadedPrompts'
      });
      
      if (response.success) {
        showNotification('Preloaded prompt library reset successfully!', 'success');
        await loadData();
        updateStats();
        renderFolders();
        renderPrompts();
      } else {
        showNotification('Failed to reset preloaded prompts: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error resetting preloaded prompts:', error);
      showNotification('Error resetting preloaded prompts. Please try again.', 'error');
    }
  }

  // Edit prompt (placeholder for future implementation)
  function editPrompt(promptId) {
    showNotification('Edit functionality coming soon!', 'info');
  }

  // Delete prompt
  async function deletePrompt(promptId) {
    if (!confirm('Are you sure you want to delete this prompt?')) return;
    
    try {
      const response = await browser.runtime.sendMessage({ 
        action: 'deletePrompt', 
        promptId: promptId 
      });
      
      if (response.success) {
        showNotification('Prompt deleted successfully!', 'success');
        await loadData();
        updateStats();
        renderFolders();
        renderPrompts();
      } else {
        showNotification('Failed to delete prompt: ' + (response.error || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error deleting prompt:', error);
      showNotification('Error deleting prompt. Please try again.', 'error');
    }
  }

  // Copy to clipboard
  async function copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      showNotification('Prompt copied to clipboard!', 'success');
    } catch (error) {
      console.error('Error copying to clipboard:', error);
      showNotification('Failed to copy to clipboard.', 'error');
    }
  }

  // Show notification
  function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
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

  // Escape HTML to prevent XSS
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Update folder select in add prompt modal
  function updateFolderSelect() {
    elements.promptFolderSelect.innerHTML = '<option value="">Select a folder...</option>';
    
    folders.forEach(folder => {
      const option = document.createElement('option');
      option.value = folder.id;
      option.textContent = folder.name;
      elements.promptFolderSelect.appendChild(option);
    });
  }

  // Open add prompt modal with updated folder list
  elements.addPromptBtn.addEventListener('click', () => {
    updateFolderSelect();
    openModal('addPromptModal');
  });

  // Listen for storage changes
  browser.storage.onChanged.addListener((changes, areaName) => {
    if (areaName === 'local' && changes.folders) {
      loadData().then(() => {
        updateStats();
        renderFolders();
        renderPrompts();
      });
    }
  });

  // Initialize the application
  init();
});