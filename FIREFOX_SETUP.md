# Firefox Extension Setup and Testing Guide

## Overview
This guide will help you set up and test the RCP (Right Click Prompt) Firefox extension. The extension has been converted from Chrome Manifest V3 to Firefox Manifest V2 format while maintaining full functionality.

## What RCP Actually Does
RCP is a powerful prompt management extension that allows you to:
- **Create folders** to organize your AI prompts
- **Save prompts** with titles and content
- **Access prompts instantly** via right-click context menu
- **Copy prompts to clipboard** with one click
- **Auto-paste prompts** directly into text fields
- **Use floating icon** to save selected text as prompts

## Extension Architecture
- **Hierarchical Context Menu**: Right-click → "Right Click Prompt" → Folders → Prompts
- **Folder-based Organization**: Prompts are organized in customizable folders
- **Floating Icon**: Appears when text is selected for quick saving
- **Popup Interface**: Manage folders and prompts through the extension popup

## Prerequisites
- Firefox browser (version 78.0 or higher)
- The extension files from this repository

## Installation Steps

### Method 1: Using about:debugging (Recommended)

1. **Open Firefox Debugging Mode**
   - Type `about:debugging` in the Firefox address bar
   - Press Enter to access the debugging page

2. **Enable Temporary Extension Installation**
   - Click on "This Firefox" in the left sidebar
   - Look for "Temporary Extensions" section

3. **Load the Extension**
   - Click the "Load Temporary Add-on" button
   - Navigate to and select any file from the extension directory (e.g., `manifest.json`)
   - The extension will be installed and activated

### Method 2: Using WebExtension API

1. **Package the Extension**
   - Create a ZIP file of all extension files
   - Make sure to include all files and maintain the directory structure

2. **Install the Extension**
   - Open Firefox and go to `about:addons`
   - Click the gear icon ⚙️ and select "Install Add-on From File..."
   - Choose the ZIP file you created
   - Confirm the installation

## Testing the Extension

### 1. Context Menu Functionality
- **Test**: Right-click on any webpage
- **Expected**: Should see "Right Click Prompt" in the context menu
- **Verify**: Hover over it to see folder structure (starts with "Default" folder)

### 2. Popup Interface Management
- **Test**: Click the extension icon in the toolbar
- **Expected**: Should see the RCP popup interface
- **Verify**:
  - "New Folder" and "New Prompt" buttons are visible
  - Can create folders and add prompts
  - Interface shows folder-based organization

### 3. Creating Folders and Prompts
- **Test**: 
  1. Click "New Folder" button
  2. Enter a folder name (e.g., "AI Prompts")
  3. Click "New Prompt" button
  4. Enter prompt text and title
  5. Choose destination folder
- **Expected**: Folders and prompts should be created and visible
- **Verify**: Check that prompts appear under correct folders

### 4. Context Menu Integration
- **Test**: After creating prompts, right-click on any webpage
- **Expected**: "Right Click Prompt" should show your folders and prompts
- **Verify**: Click on a prompt to copy it to clipboard

### 5. Floating Icon Feature
- **Test**: Select any text on a webpage
- **Expected**: A floating icon should appear near the selected text
- **Verify**: Click the icon to open a modal and save the selected text as a prompt

### 6. Copy and Auto-paste Functionality
- **Test**: 
  1. Create a prompt with some text
  2. Right-click and access the prompt via context menu
  3. Click on the prompt
- **Expected**: Text should be copied to clipboard
- **Verify**: Check clipboard content and auto-paste functionality

### 7. Data Persistence
- **Test**: Create folders and prompts, then close and reopen Firefox
- **Expected**: All data should persist
- **Verify**: Folders and prompts should still be available

## Firefox-Specific Considerations

### API Conversions Made
- **API Namespace**: All `chrome.*` calls replaced with `browser.*`
- **Manifest Version**: Converted from V3 (Chrome) to V2 (Firefox)
- **Background Script**: Uses background.js instead of service worker
- **Permissions**: Adjusted for Firefox compatibility

### Permissions Used
- `storage`: For saving folders, prompts, and settings
- `contextMenus`: For right-click menu functionality
- `clipboardWrite`: For copying prompts to clipboard
- `activeTab`: For accessing the current tab
- `scripting`: For content script injection and auto-paste

### Key Features Maintained
- **Hierarchical context menu system** with folders and prompts
- **Toast notifications** for user feedback
- **Auto-paste functionality** with smart text insertion
- **Floating icon** for quick prompt creation
- **Real-time updates** across all extension components

## Troubleshooting

### Common Issues

#### 1. Extension Won't Install
**Problem**: Firefox shows an error when installing the extension
**Solution**:
- Check that all files are present and correctly structured
- Verify manifest.json syntax is correct
- Ensure all referenced files exist

#### 2. Context Menu Not Appearing
**Problem**: Right-click doesn't show "Right Click Prompt" option
**Solution**:
- Check that background.js is running correctly
- Verify folders exist (extension creates "Default" folder automatically)
- Check browser console for errors

#### 3. Floating Icon Not Working
**Problem**: Floating icon doesn't appear when text is selected
**Solution**:
- Check that content-script.js is properly injected
- Verify floatingIcon.ts-CJpmuZwW.js is accessible
- Check browser console for JavaScript errors

#### 4. Popup Not Opening
**Problem**: Clicking extension icon doesn't open popup
**Solution**:
- Verify popup.html and popup.js are correctly referenced in manifest.json
- Check for JavaScript errors in popup
- Ensure popup.html file exists in the correct location

#### 5. Prompts Not Saving
**Problem**: Created prompts disappear after browser restart
**Solution**:
- Check that storage permissions are granted
- Verify storage.local API calls are working
- Check for quota limits

#### 6. Auto-paste Not Working
**Problem**: Prompts copy to clipboard but don't auto-paste
**Solution**:
- Verify scripting permissions are granted
- Check that the active tab is not a restricted URL
- Test with different text fields and editors

### Debugging Steps

1. **Open Browser Console**
   - Press Ctrl+Shift+J (or Cmd+Opt+J on Mac)
   - Look for error messages related to the extension

2. **Check Extension Debugger**
   - Go to `about:debugging`
   - Click on your extension under "Temporary Extensions"
   - Use the "Inspect" button to open debugging tools

3. **Verify File Structure**
   - Ensure all files referenced in manifest.json exist
   - Check file paths and permissions

4. **Test Permissions**
   - Verify all required permissions are granted
   - Check Firefox's privacy settings

## Development Notes

### Key Files Modified
- `manifest.json`: Converted to Firefox Manifest V2 format
- `background.js`: Complete rewrite with folder-based context menu system
- `popup.js`: Full folder and prompt management functionality
- `popup.html`: Updated interface for folder-based organization
- `content-script.js`: Firefox-compatible message passing

### Testing Checklist
- [ ] Extension installs successfully in Firefox
- [ ] Context menu appears with "Right Click Prompt" option
- [ ] Default folder is created automatically
- [ ] Can create new folders via popup interface
- [ ] Can create new prompts via popup interface
- [ ] Folders and prompts appear in context menu hierarchy
- [ ] Clicking prompts copies them to clipboard
- [ ] Floating icon appears when text is selected
- [ ] Floating icon can save selected text as prompts
- [ ] Data persists across browser sessions
- [ ] No JavaScript errors in console
- [ ] Toast notifications work correctly
- [ ] Auto-paste functionality works in text fields

## Advanced Features

### Auto-paste Support
The extension supports auto-pasting into various editors:
- **Regular text fields** and textareas
- **ContentEditable** elements
- **Monaco Editor** (VS Code web editor)
- **CodeMirror** (many code editors)
- **Ace Editor** (web IDEs)
- **TinyMCE** and **CKEditor** (WYSIWYG editors)

### Toast Notifications
Instead of basic alerts, RCP uses styled toast notifications that:
- Appear as overlays on web pages
- Show random success messages for variety
- Fallback to badge notifications on restricted pages
- Auto-dismiss after 2 seconds

### Theme Support
The extension supports dark/light themes:
- Automatically detects system preference
- Floating icon and modal adapt to theme
- Theme changes propagate across all components

## Submitting to Firefox Add-on Store

When ready to publish:
1. Create a Mozilla Developer account
2. Package the extension as a signed XPI file
3. Submit to Firefox Add-on Store for review
4. Address any review feedback promptly

## Support

If you encounter issues not covered in this guide:
1. Check the browser console for error messages
2. Verify all files are correctly structured
3. Test with a clean Firefox profile
4. Consult Firefox extension documentation

## Feature Comparison

| Feature | Chrome Extension | Firefox Extension |
|---------|-----------------|-------------------|
| Hierarchical Context Menu | ✅ | ✅ |
| Folder Organization | ✅ | ✅ |
| Floating Icon | ✅ | ✅ |
| Auto-paste | ✅ | ✅ |
| Toast Notifications | ✅ | ✅ |
| Theme Support | ✅ | ✅ |
| Data Persistence | ✅ | ✅ |
| Cross-editor Support | ✅ | ✅ |
| Real-time Updates | ✅ | ✅ |