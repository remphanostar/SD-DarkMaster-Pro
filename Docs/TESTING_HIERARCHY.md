# 🧪 Testing Hierarchy - How to Test the Notebook

## ✅ **TESTING ORDER OF PREFERENCE:**

### 1️⃣ **PAPERMILL (PRIMARY - ALWAYS TRY FIRST)**
```bash
# This is the BEST method - automated, reliable, captures everything
timeout 60 /workspace/ai_tools_env/bin/papermill \
    /workspace/SD-DarkMaster-Pro-SUPER-DUPER-FINAL-LAST-EDITION/notebook/SD-DarkMaster-Pro.ipynb \
    /workspace/SD-DarkMaster-Pro-SUPER-DUPER-FINAL-LAST-EDITION/notebook/test-output.ipynb \
    --kernel python3

# Check results:
timeout 10 grep -i "error\|exception" test-output.ipynb
```

**Why Papermill is Best:**
- ✅ Runs all cells automatically in order
- ✅ Captures ALL output and errors
- ✅ Creates reviewable output file
- ✅ No manual intervention needed
- ✅ Consistent results every time
- ✅ Shows exactly which cell fails

### 2️⃣ **JUPYTERLAB (FALLBACK - IF PAPERMILL FAILS)**
```bash
# Only use if papermill doesn't work
timeout 30 /workspace/ai_tools_env/bin/jupyter lab \
    --no-browser \
    --port=8888 \
    --NotebookApp.token='' \
    --NotebookApp.password=''

# Then:
# 1. Navigate to notebook
# 2. Run → Run All Cells
# 3. Watch for errors
# 4. CRITICAL: Close after testing!
timeout 5 pkill -f jupyter
```

**When to Use JupyterLab:**
- ⚠️ If papermill installation is broken
- ⚠️ If kernel issues prevent papermill
- ⚠️ For interactive debugging only
- ⚠️ As a last resort

**Problems with JupyterLab:**
- ❌ Manual process (prone to errors)
- ❌ Might skip cells accidentally
- ❌ No automatic output capture
- ❌ Processes can accumulate
- ❌ Slower than papermill

### 3️⃣ **DIRECT PYTHON (NEVER USE)**
```bash
# DON'T DO THIS - Won't work properly
python notebook.py  # ❌ WRONG
exec(open('cell1.py').read())  # ❌ WRONG
```

## 📊 **Testing Decision Tree:**

```
Start Testing
    ↓
Try Papermill First
    ↓
Did it work? → YES → Done! ✅
    ↓ NO
Why did it fail?
    ├─ Papermill not installed → Install it → Try again
    ├─ Kernel issues → Fix kernel → Try again
    └─ Other error → Use JupyterLab as fallback
                        ↓
                   Run in JupyterLab
                        ↓
                   ALWAYS close after:
                   timeout 5 pkill -f jupyter
```

## 🎯 **Testing Commands Summary:**

### Always Start With:
```bash
# 1. Check papermill is available
timeout 5 which /workspace/ai_tools_env/bin/papermill

# 2. Run test with papermill
timeout 60 /workspace/ai_tools_env/bin/papermill \
    notebook/SD-DarkMaster-Pro.ipynb \
    notebook/test-$(date +%s).ipynb

# 3. Check for errors
timeout 10 grep -C5 -i "error\|exception\|failed" notebook/test-*.ipynb
```

### Only If Papermill Fails:
```bash
# 1. Start JupyterLab
timeout 30 /workspace/ai_tools_env/bin/jupyter lab --no-browser --port=8888

# 2. Note the URL, test manually

# 3. CRITICAL - Always cleanup
timeout 5 pkill -f jupyter
```

## ⚠️ **Common Testing Mistakes:**

### DON'T:
- ❌ Skip papermill and go straight to JupyterLab
- ❌ Leave JupyterLab running after testing
- ❌ Test cells individually (test all or nothing)
- ❌ Modify the notebook during testing
- ❌ Forget to check the output for errors

### DO:
- ✅ Always try papermill first
- ✅ Always use timeout on commands
- ✅ Always cleanup Jupyter processes
- ✅ Save test outputs with timestamps
- ✅ Review error messages carefully

## 📝 **Reporting Test Results:**

### After Papermill Success:
```markdown
✅ Notebook tested with papermill
- All 5 cells executed successfully
- Output saved to: test-output.ipynb
- No errors detected
- Execution time: XX seconds
```

### After JupyterLab Fallback:
```markdown
⚠️ Tested with JupyterLab (papermill failed because: [reason])
- All 5 cells executed manually
- [Any errors observed]
- JupyterLab closed after testing
```

## 🚀 **Remember:**

**PAPERMILL = Professional, Automated, Reliable**
**JupyterLab = Manual fallback only**

Always prefer the robot (papermill) over manual clicking!