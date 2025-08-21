# RCP Firefox Extension - Quick Start Guide

## 🚀 Installation (5 Minutes)

### Step 1: Open Firefox
Launch Firefox browser on your computer.

### Step 2: Open Debugging Mode
- Type `about:debugging` in the address bar
- Press Enter
- Click on "This Firefox" in the left sidebar

### Step 3: Load Extension
- Click the "Load Temporary Add-on..." button
- Navigate to the RCP-Firefox folder
- Select the `manifest.json` file
- Click "Open"

### Step 4: Verify Installation
- Look for the RCP icon in the Firefox toolbar
- Click the icon to open the extension popup
- You should see preloaded prompts ready to use

## 🧪 Quick Testing (2 Minutes)

### Test 1: Basic Functionality
1. Click the RCP icon in the toolbar
2. Verify you see folders with prompts
3. Click "📋 Copy" on any prompt
4. Paste into a text field to confirm it works

### Test 2: Right-Click Menu
1. Open the test page: `test-page.html`
2. Right-click on any text field
3. Look for "RCP" in the context menu
4. Select a prompt to auto-paste

### Test 3: Floating Icon
1. Navigate to any webpage with text fields
2. Look for the RCP floating icon (bottom-right corner)
3. Click it to access prompts

### Test 4: Reset Library (If you see fewer than 30 prompts)
1. Click the RCP icon in the toolbar
2. Click the "🔄 Reset Library" button
3. Confirm the reset action
4. Verify you now see 30+ preloaded prompts

## 📋 Key Features

✅ **30 Preloaded Prompts** - Ready to use across 10 categories  
✅ **Save Custom Prompts** - Create your own prompt library  
✅ **Organize in Folders** - Group prompts by project or topic  
✅ **Right-Click Access** - Quick access from any text field  
✅ **Auto-Paste** - Automatically paste prompts into text fields  
✅ **Floating Icon** - Access prompts without leaving your workflow  

## 🎯 Preloaded Prompt Categories

1. **Programming & Development** (3 prompts)
   - Professional Coder, Code Review Assistant, Algorithm Designer

2. **Writing & Content Creation** (3 prompts)
   - Academic Assistant Pro, All-around Writer, Content Summarizer

3. **Business & Productivity** (3 prompts)
   - Business Strategy Analyst, Marketing Strategist, Productivity Coach

4. **Analysis & Research** (3 prompts)
   - Data Analysis Pro, Research Assistant, Critical Thinking Expert

5. **Education & Learning** (3 prompts)
   - All-around Teacher, Learning Coach, Curriculum Designer

6. **Creative & Artistic** (3 prompts)
   - Creative Director, Storyteller, Design Consultant

7. **Communication** (3 prompts)
   - Communication Expert, Email Specialist, Presentation Designer

8. **Problem Solving** (3 prompts)
   - Problem Solver, Decision Maker, Innovation Consultant

9. **Technical Documentation** (3 prompts)
   - Technical Writer, API Documentation Specialist, User Guide Creator

10. **Personal Development** (3 prompts)
    - Life Coach, Career Counselor, Skill Development Advisor  
✅ **Reset Library** - Reload all 30 preloaded prompts if needed  

## 🔧 Troubleshooting

### Only Seeing 5-10 Prompts Instead of 30?
This is a common issue. Here's how to fix it:

1. **Reset the Library**:
   - Click the RCP icon in the toolbar
   - Click the "🔄 Reset Library" button
   - Confirm the reset action
   - The extension will reload all 30 preloaded prompts

2. **Reinstall the Extension**:
   - Go to `about:debugging`
   - Remove the extension
   - Reload the extension using `manifest.json`

3. **Check Browser Console**:
   - Press Ctrl+Shift+J to open the console
   - Look for error messages
   - Reload the extension and check for loading messages

### Extension Won't Install
- Ensure you selected `manifest.json` (not other files)
- Check that Firefox is up to date
- Try restarting Firefox

### Prompts Not Saving
- Open browser console (Ctrl+Shift+J) for errors
- Try reloading the extension
- Check storage permissions

### Context Menu Not Working
- Refresh the webpage after installing
- Try right-clicking on different text fields
- Check that the extension has proper permissions

## 📁 File Structure

```
RCP-Firefox/
├── manifest.json              # Extension configuration
├── background.js              # Background service worker
├── popup.html                 # Extension popup UI
├── popup.js                   # Popup functionality
├── content-script.js          # Page interaction
├── preloaded-prompts-library.js # 30 ready-to-use prompts
├── test-page.html             # Testing page
├── test-extension.js          # Test script
├── test-library.js            # Library test script
├── QUICK_START.md             # This guide
├── README.md                  # Full documentation
├── FIREFOX_SETUP.md           # Detailed setup
└── SETUP_AND_TESTING_GUIDE.md  # Comprehensive testing
```

## 🎯 Expected Prompts

The extension should include **30 high-quality prompts** across these categories:

1. **Programming & Development** (3 prompts)
2. **Writing & Content Creation** (3 prompts)
3. **Business & Productivity** (3 prompts)
4. **Analysis & Research** (3 prompts)
5. **Education & Learning** (3 prompts)
6. **Creative & Artistic** (3 prompts)
7. **Communication** (3 prompts)
8. **Problem Solving** (3 prompts)
9. **Technical Documentation** (3 prompts)
10. **Personal Development** (3 prompts)

If you don't see all 30 prompts, use the "🔄 Reset Library" button to reload them.

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review `SETUP_AND_TESTING_GUIDE.md` for comprehensive testing
- Use `test-page.html` to test extension functionality
- Check browser console (Ctrl+Shift+J) for error messages
- Use the "🔄 Reset Library" button if prompts are missing

---

**🎉 Congratulations! Your RCP Firefox extension is ready to use!**