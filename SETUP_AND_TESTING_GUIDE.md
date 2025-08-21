# RCP Firefox Extension - Setup and Testing Guide

## 🎯 What We Fixed

Your Firefox extension now has the following critical fixes:

### ✅ **Prompt Saving Issues Fixed**
1. **Background script now returns complete folder data** (including prompts)
2. **Popup.js uses proper storage management** through background script
3. **Added missing message handlers** for deleteFolder and deletePrompt actions
4. **Fixed data consistency** between all extension components

### ✅ **Auto-Paste Functionality Fixed**
1. **Auto-paste is now enabled by default** for better user experience
2. **Enhanced text field detection** for various editors (VS Code, CodeMirror, etc.)
3. **Improved clipboard handling** with multiple fallback methods
4. **Better error handling** for restricted URLs

### ✅ **Floating Icon Issues Fixed**
1. **Added Chrome API compatibility layer** for the minified floating icon script
2. **Text-to-prompt feature enabled by default**
3. **Improved API injection** in content script
4. **Better error handling** for feature state management

## 🚀 Quick Setup Instructions

### Step 1: Install the Extension in Firefox

1. **Open Firefox Debugging Mode**
   - Type `about:debugging` in the Firefox address bar
   - Press Enter to access the debugging page

2. **Load the Extension**
   - Click on "This Firefox" in the left sidebar
   - Look for "Temporary Extensions" section
   - Click the "Load Temporary Add-on" button
   - Navigate to and select `manifest.json` from your RCP-Firefox directory
   - The extension should install successfully

### Step 2: Verify Installation

✅ **Extension should appear in the Firefox toolbar**  
✅ **No error messages should appear during installation**  
✅ **A "Default" folder should be created automatically**

## 🧪 Testing the Extension

### Test 1: Basic Popup Interface
1. **Click the RCP icon** in the Firefox toolbar
2. **Expected**: Should see the RCP popup interface with:
   - Header: "RCP - Right Click Prompt"
   - Action buttons: "+ New Folder", "+ New Prompt", "🔍 Discover"
   - A "Default" folder with no prompts yet

### Test 2: Create Folders and Prompts
1. **Click "+ New Folder"**
2. **Enter**: "Test Folder"
3. **Click "+ New Prompt"**
4. **Enter prompt text**: "This is a test prompt"
5. **Enter title**: "Test Prompt"
6. **Select**: "Test Folder" as destination
7. **Expected**: Prompt should appear under "Test Folder"

### Test 3: Context Menu Integration
1. **Right-click on any webpage**
2. **Expected**: Should see "Right Click Prompt" in the context menu
3. **Hover over it**: Should see your folders and prompts
4. **Click on your test prompt**: Should copy to clipboard AND auto-paste into any active text field

### Test 4: Floating Icon Feature
1. **Select any text on a webpage** (like this sentence)
2. **Expected**: A red hexagonal floating icon should appear near the selected text
3. **Click the icon**: Should open a modal to save the selected text as a prompt
4. **Fill in the form**: Add title and select folder
5. **Click Save**: Should save the selected text as a new prompt

### Test 5: Auto-Paste Functionality
1. **Create a test prompt** with some text
2. **Go to any website with a text field** (Google search, GitHub issue, etc.)
3. **Click in the text field** to focus it
4. **Right-click and access your prompt** via context menu
5. **Click on the prompt**
6. **Expected**: Text should automatically paste into the text field

## 🔧 Advanced Testing

### Test with Different Text Editors
The extension should work with:
- **Regular text fields** and textareas ✅
- **ContentEditable elements** (like Gmail compose) ✅
- **Code editors** like GitHub, CodePen, JSFiddle ✅
- **Monaco Editor** (VS Code web editor) ✅
- **CodeMirror** (many code editors) ✅

### Test Data Persistence
1. **Create several folders and prompts**
2. **Close Firefox completely**
3. **Reopen Firefox**
4. **Check extension**: All folders and prompts should still be there

## 🐛 Troubleshooting

### Issue: Extension won't install
**Solution**: 
- Check that all files are present in the RCP-Firefox directory
- Verify manifest.json has no syntax errors
- Try loading a different file from the directory

### Issue: Floating icon doesn't appear
**Solution**:
- Make sure you're selecting text (not just clicking)
- Check browser console for errors (Ctrl+Shift+J)
- Try refreshing the webpage

### Issue: Prompts don't save
**Solution**:
- Check browser console for error messages
- Verify you're filling in both title and selecting a folder
- Try creating a new folder first

### Issue: Auto-paste doesn't work
**Solution**:
- Make sure you click in a text field first
- Check that the URL is not restricted (chrome://, about:, etc.)
- Try different websites with text fields

### Issue: Context menu doesn't show prompts
**Solution**:
- Make sure you have at least one folder and one prompt
- Try right-clicking on different parts of the webpage
- Check that folders have prompts in them

## 📋 Test Checklist

Use this checklist to verify all features work:

### ✅ **Installation & Setup**
- [ ] Extension installs successfully in Firefox
- [ ] No error messages during installation
- [ ] Extension icon appears in toolbar
- [ ] Default folder is created automatically

### ✅ **Basic Functionality**
- [ ] Popup interface opens when clicking extension icon
- [ ] Can create new folders
- [ ] Can create new prompts
- [ ] Prompts appear under correct folders
- [ ] Can delete folders
- [ ] Can delete prompts

### ✅ **Context Menu Features**
- [ ] Right-click shows "Right Click Prompt" option
- [ ] Folders appear in context menu
- [ ] Prompts appear under folders in context menu
- [ ] Clicking prompts copies to clipboard
- [ ] Auto-paste works in text fields

### ✅ **Floating Icon Features**
- [ ] Floating icon appears when text is selected
- [ ] Clicking icon opens save prompt modal
- [ ] Can save selected text as prompt
- [ ] Modal has proper styling and functionality

### ✅ **Advanced Features**
- [ ] Auto-paste works in different text editors
- [ ] Data persists across browser sessions
- [ ] Toast notifications appear
- [ ] No JavaScript errors in console
- [ ] Works on different websites

## 🎯 Success Criteria

Your Firefox extension is working correctly when:

1. **You can create folders and prompts** that persist across sessions
2. **Right-click context menu** shows your prompts and folders
3. **Clicking prompts auto-pastes** text into active text fields
4. **Floating icon appears** when you select text and allows saving
5. **All features work** just like the original Chrome extension

## 📞 Getting Help

If you encounter issues:

1. **Check browser console**: Press `Ctrl+Shift+J` to see error messages
2. **Review this guide**: Make sure you followed all steps correctly
3. **Test with clean profile**: Create a new Firefox profile for testing
4. **Check file permissions**: Ensure all extension files are accessible

## 🎉 Next Steps

Once all tests pass:

1. **Test with real-world scenarios**: Use it for your actual AI prompting workflow
2. **Consider publishing**: Package for Firefox Add-on Store
3. **Gather feedback**: Get other users to test it
4. **Iterate**: Fix any remaining issues based on real usage

---

**🔥 Your RCP Firefox extension should now work just like the Chrome version!**  
**If you follow this guide and all tests pass, you'll have full functionality including prompt saving, auto-paste, and floating icon features.**