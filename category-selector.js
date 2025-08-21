// Category Selector for RCP Extension
// This script creates a modal interface for selecting a category when saving highlighted text as a prompt

(function() {
    'use strict';

    // Check if the modal already exists
    if (document.getElementById('rcp-category-selector')) {
        return;
    }

    // Create modal container
    const modal = document.createElement('div');
    modal.id = 'rcp-category-selector';
    modal.innerHTML = `
        <div class="rcp-modal-overlay">
            <div class="rcp-modal-container">
                <div class="rcp-modal-header">
                    <h3>💾 Save Selection as Prompt</h3>
                    <button class="rcp-close-btn" title="Close">&times;</button>
                </div>
                <div class="rcp-modal-content">
                    <div class="rcp-preview-section">
                        <h4>Selected Text:</h4>
                        <div class="rcp-text-preview" id="rcp-text-preview"></div>
                    </div>
                    <div class="rcp-input-section">
                        <label for="rcp-prompt-title">Prompt Title (optional):</label>
                        <input type="text" id="rcp-prompt-title" placeholder="Enter a title for this prompt..." maxlength="100">
                    </div>
                    <div class="rcp-category-section">
                        <h4>Select Category:</h4>
                        <div class="rcp-category-list" id="rcp-category-list">
                            <div class="rcp-loading">Loading categories...</div>
                        </div>
                        <div class="rcp-new-category">
                            <input type="text" id="rcp-new-category-input" placeholder="Or create a new category..." maxlength="50">
                            <button id="rcp-create-category-btn" class="rcp-btn rcp-btn-secondary">Create</button>
                        </div>
                    </div>
                </div>
                <div class="rcp-modal-footer">
                    <button id="rcp-cancel-btn" class="rcp-btn rcp-btn-secondary">Cancel</button>
                    <button id="rcp-save-btn" class="rcp-btn rcp-btn-primary">Save Prompt</button>
                </div>
            </div>
        </div>
    `;

    // Add CSS styles
    const styles = document.createElement('style');
    styles.textContent = `
        #rcp-category-selector {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 999999;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .rcp-modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .rcp-modal-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            width: 100%;
            max-width: 500px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .rcp-modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px;
            border-bottom: 1px solid #e5e7eb;
            background: #f9fafb;
        }

        .rcp-modal-header h3 {
            margin: 0;
            color: #374151;
            font-size: 18px;
            font-weight: 600;
        }

        .rcp-close-btn {
            background: none;
            border: none;
            font-size: 24px;
            color: #6b7280;
            cursor: pointer;
            padding: 0;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        .rcp-close-btn:hover {
            background: #e5e7eb;
            color: #374151;
        }

        .rcp-modal-content {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }

        .rcp-preview-section {
            margin-bottom: 20px;
        }

        .rcp-preview-section h4 {
            margin: 0 0 8px 0;
            color: #374151;
            font-size: 14px;
            font-weight: 600;
        }

        .rcp-text-preview {
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: 12px;
            font-size: 13px;
            line-height: 1.5;
            color: #4b5563;
            max-height: 100px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .rcp-input-section {
            margin-bottom: 20px;
        }

        .rcp-input-section label {
            display: block;
            margin-bottom: 6px;
            color: #374151;
            font-size: 14px;
            font-weight: 600;
        }

        .rcp-input-section input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.2s ease;
        }

        .rcp-input-section input:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .rcp-category-section h4 {
            margin: 0 0 12px 0;
            color: #374151;
            font-size: 14px;
            font-weight: 600;
        }

        .rcp-category-list {
            margin-bottom: 16px;
            max-height: 200px;
            overflow-y: auto;
        }

        .rcp-category-item {
            display: flex;
            align-items: center;
            padding: 10px 12px;
            margin-bottom: 4px;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .rcp-category-item:hover {
            background: #f3f4f6;
            border-color: #d1d5db;
        }

        .rcp-category-item.selected {
            background: #dbeafe;
            border-color: #3b82f6;
        }

        .rcp-category-item input[type="radio"] {
            margin-right: 8px;
        }

        .rcp-category-item label {
            flex: 1;
            cursor: pointer;
            font-size: 14px;
            color: #374151;
        }

        .rcp-category-item .rcp-prompt-count {
            font-size: 12px;
            color: #6b7280;
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
        }

        .rcp-new-category {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .rcp-new-category input {
            flex: 1;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
        }

        .rcp-new-category input:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .rcp-modal-footer {
            display: flex;
            gap: 12px;
            justify-content: flex-end;
            padding: 16px 20px;
            border-top: 1px solid #e5e7eb;
            background: #f9fafb;
        }

        .rcp-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .rcp-btn-primary {
            background: #3b82f6;
            color: white;
        }

        .rcp-btn-primary:hover:not(:disabled) {
            background: #2563eb;
        }

        .rcp-btn-primary:disabled {
            background: #9ca3af;
            cursor: not-allowed;
        }

        .rcp-btn-secondary {
            background: #6b7280;
            color: white;
        }

        .rcp-btn-secondary:hover:not(:disabled) {
            background: #4b5563;
        }

        .rcp-loading {
            text-align: center;
            color: #6b7280;
            font-style: italic;
            padding: 20px;
        }

        .rcp-empty-categories {
            text-align: center;
            color: #6b7280;
            font-style: italic;
            padding: 20px;
        }

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .rcp-modal-container {
                background: #1f2937;
                color: #f9fafb;
            }

            .rcp-modal-header {
                background: #374151;
                border-bottom-color: #4b5563;
            }

            .rcp-modal-header h3 {
                color: #f9fafb;
            }

            .rcp-close-btn {
                color: #9ca3af;
            }

            .rcp-close-btn:hover {
                background: #4b5563;
                color: #f9fafb;
            }

            .rcp-text-preview {
                background: #374151;
                border-color: #4b5563;
                color: #d1d5db;
            }

            .rcp-input-section label,
            .rcp-category-section h4 {
                color: #f9fafb;
            }

            .rcp-input-section input,
            .rcp-new-category input {
                background: #374151;
                border-color: #4b5563;
                color: #f9fafb;
            }

            .rcp-category-item {
                border-color: #4b5563;
                color: #f9fafb;
            }

            .rcp-category-item:hover {
                background: #374151;
                border-color: #6b7280;
            }

            .rcp-category-item.selected {
                background: #1e3a8a;
                border-color: #3b82f6;
            }

            .rcp-category-item label {
                color: #f9fafb;
            }

            .rcp-category-item .rcp-prompt-count {
                background: #374151;
                color: #9ca3af;
            }

            .rcp-modal-footer {
                background: #374151;
                border-top-color: #4b5563;
            }
        }
    `;

    // Add modal and styles to the page
    document.head.appendChild(styles);
    document.body.appendChild(modal);

    // Get DOM elements
    const modalElement = document.getElementById('rcp-category-selector');
    const closeBtn = modalElement.querySelector('.rcp-close-btn');
    const cancelBtn = document.getElementById('rcp-cancel-btn');
    const saveBtn = document.getElementById('rcp-save-btn');
    const textPreview = document.getElementById('rcp-text-preview');
    const titleInput = document.getElementById('rcp-prompt-title');
    const categoryList = document.getElementById('rcp-category-list');
    const newCategoryInput = document.getElementById('rcp-new-category-input');
    const createCategoryBtn = document.getElementById('rcp-create-category-btn');

    let selectedFolderId = null;
    let folders = [];
    let pendingPrompt = null;

    // Load pending prompt data
    async function loadPendingPrompt() {
        try {
            // Ensure browser API is available
            if (typeof browser === 'undefined' || !browser.runtime) {
                console.error('Browser runtime API not available');
                textPreview.textContent = 'Extension context not available.';
                saveBtn.disabled = true;
                return;
            }

            const response = await browser.runtime.sendMessage({ action: 'getPendingPrompt' });
            if (response && response.success && response.text) {
                pendingPrompt = response;
                textPreview.textContent = response.text;
                
                // Auto-generate a title from the first few words
                if (!titleInput.value) {
                    const words = response.text.split(' ').slice(0, 6);
                    const autoTitle = words.join(' ') + (response.text.split(' ').length > 6 ? '...' : '');
                    titleInput.value = autoTitle;
                }
            } else {
                textPreview.textContent = 'No text selected.';
                saveBtn.disabled = true;
            }
        } catch (error) {
            console.error('Error loading pending prompt:', error);
            textPreview.textContent = 'Error loading selected text.';
            saveBtn.disabled = true;
        }
    }

    // Load folders
    async function loadFolders() {
        try {
            // Ensure browser API is available
            if (typeof browser === 'undefined' || !browser.runtime) {
                console.error('Browser runtime API not available');
                categoryList.innerHTML = '<div class="rcp-empty-categories">Extension context not available.</div>';
                return;
            }

            const response = await browser.runtime.sendMessage({ action: 'getFolders' });
            if (response && response.success && response.folders) {
                folders = response.folders;
                console.log('Loaded folders:', folders); // Debug log
                renderCategories();
            } else {
                console.log('No folders found or error in response:', response); // Debug log
                categoryList.innerHTML = '<div class="rcp-empty-categories">No categories found. Create one below.</div>';
            }
        } catch (error) {
            console.error('Error loading folders:', error);
            categoryList.innerHTML = '<div class="rcp-empty-categories">Error loading categories. Please try again.</div>';
        }
    }

    // Render categories
    function renderCategories() {
        console.log('Rendering categories, folders count:', folders.length); // Debug log
        
        if (folders.length === 0) {
            categoryList.innerHTML = '<div class="rcp-empty-categories">No categories found. Create one below.</div>';
            return;
        }

        categoryList.innerHTML = '';
        folders.forEach(folder => {
            const categoryItem = document.createElement('div');
            categoryItem.className = 'rcp-category-item';
            categoryItem.innerHTML = `
                <input type="radio" name="rcp-category" value="${folder.id}" id="category-${folder.id}">
                <label for="category-${folder.id}">
                    ${escapeHtml(folder.name)}
                    <span class="rcp-prompt-count">${folder.prompts ? folder.prompts.length : 0}</span>
                </label>
            `;

            categoryItem.addEventListener('click', () => {
                selectCategory(folder.id, categoryItem);
            });

            categoryList.appendChild(categoryItem);
        });
        
        console.log('Rendered', folders.length, 'categories'); // Debug log
    }

    // Select category
    function selectCategory(folderId, element) {
        console.log('Selecting category:', folderId); // Debug log
        selectedFolderId = folderId;
        
        // Update visual selection
        document.querySelectorAll('.rcp-category-item').forEach(item => {
            item.classList.remove('selected');
        });
        element.classList.add('selected');
        
        // Update radio button
        const radio = element.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
        }

        // Enable save button
        saveBtn.disabled = false;
        console.log('Category selected, save button enabled'); // Debug log
    }

    // Create new category
    async function createNewCategory() {
        const categoryName = newCategoryInput.value.trim();
        console.log('Creating new category:', categoryName); // Debug log
        
        if (!categoryName) {
            alert('Please enter a category name.');
            return;
        }

        // Ensure browser API is available
        if (typeof browser === 'undefined' || !browser.runtime) {
            console.error('Browser runtime API not available');
            alert('Extension context not available.');
            return;
        }

        try {
            const response = await browser.runtime.sendMessage({ 
                action: 'createFolder', 
                name: categoryName 
            });
            
            console.log('Create folder response:', response); // Debug log

            if (response && response.success) {
                // Reload folders and select the new one
                await loadFolders();
                newCategoryInput.value = '';
                
                // Find and select the new folder
                const newFolder = folders.find(f => f.name === categoryName);
                if (newFolder) {
                    const newCategoryElement = document.querySelector(`#category-${newFolder.id}`);
                    if (newCategoryElement) {
                        const categoryItem = newCategoryElement.closest('.rcp-category-item');
                        if (categoryItem) {
                            selectCategory(newFolder.id, categoryItem);
                        }
                    }
                }
            } else {
                alert('Failed to create category: ' + (response && response.error ? response.error : 'Unknown error'));
            }
        } catch (error) {
            console.error('Error creating category:', error);
            alert('Error creating category. Please try again.');
        }
    }

    // Save prompt
    async function savePrompt() {
        console.log('Saving prompt, selected folder:', selectedFolderId); // Debug log
        
        if (!selectedFolderId) {
            alert('Please select a category.');
            return;
        }

        if (!pendingPrompt || !pendingPrompt.text) {
            alert('No text to save.');
            return;
        }

        // Ensure browser API is available
        if (typeof browser === 'undefined' || !browser.runtime) {
            console.error('Browser runtime API not available');
            alert('Extension context not available.');
            return;
        }

        const title = titleInput.value.trim() || 'Selection Prompt';

        try {
            const response = await browser.runtime.sendMessage({
                action: 'saveSelectionAsPrompt',
                text: pendingPrompt.text,
                title: title,
                folderId: selectedFolderId
            });
            
            console.log('Save prompt response:', response); // Debug log

            if (response && response.success) {
                // Show success message
                showNotification('Prompt saved successfully!', 'success');
                closeModal();
            } else {
                alert('Failed to save prompt: ' + (response && response.error ? response.error : 'Unknown error'));
            }
        } catch (error) {
            console.error('Error saving prompt:', error);
            alert('Error saving prompt. Please try again.');
        }
    }

    // Close modal
    function closeModal() {
        if (modalElement && modalElement.parentNode) {
            modalElement.parentNode.removeChild(modalElement);
        }
        if (styles && styles.parentNode) {
            styles.parentNode.removeChild(styles);
        }
    }

    // Show notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `rcp-notification rcp-notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000000;
            max-width: 300px;
            word-wrap: break-word;
            animation: slideIn 0.3s ease-out;
            background-color: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        `;

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

    // Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Event listeners
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);

    saveBtn.addEventListener('click', savePrompt);
    createCategoryBtn.addEventListener('click', createNewCategory);

    newCategoryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            createNewCategory();
        }
    });

    titleInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && selectedFolderId) {
            savePrompt();
        }
    });

    // Close modal when clicking outside
    modalElement.addEventListener('click', (e) => {
        if (e.target === modalElement || e.target.classList.contains('rcp-modal-overlay')) {
            closeModal();
        }
    });

    // Escape key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalElement.parentNode) {
            closeModal();
        }
    });

    // Initialize with a small delay to ensure everything is ready
    setTimeout(() => {
        console.log('Initializing category selector...'); // Debug log
        loadPendingPrompt();
        loadFolders();
    }, 100);
})();