// RCP Firefox Extension Test Script
// This script helps verify that the extension is working correctly

console.log('🧪 RCP Firefox Extension Test Script');
console.log('=====================================');

// Test 1: Check if browser APIs are available
function testBrowserAPIs() {
    console.log('📋 Test 1: Browser APIs Availability');
    
    const requiredAPIs = [
        'browser.runtime',
        'browser.storage',
        'browser.contextMenus',
        'browser.clipboardWrite'
    ];
    
    let allAvailable = true;
    
    requiredAPIs.forEach(api => {
        const parts = api.split('.');
        let obj = window;
        let available = true;
        
        for (const part of parts) {
            if (obj[part]) {
                obj = obj[part];
            } else {
                available = false;
                break;
            }
        }
        
        if (available) {
            console.log(`✅ ${api} - Available`);
        } else {
            console.log(`❌ ${api} - Not Available`);
            allAvailable = false;
        }
    });
    
    return allAvailable;
}

// Test 2: Check storage functionality
async function testStorage() {
    console.log('\n📋 Test 2: Storage Functionality');
    
    try {
        // Test setting data
        await browser.storage.local.set({ testKey: 'testValue' });
        console.log('✅ Storage set - Success');
        
        // Test getting data
        const result = await browser.storage.local.get('testKey');
        if (result.testKey === 'testValue') {
            console.log('✅ Storage get - Success');
        } else {
            console.log('❌ Storage get - Failed');
            return false;
        }
        
        // Clean up
        await browser.storage.local.remove('testKey');
        console.log('✅ Storage cleanup - Success');
        
        return true;
    } catch (error) {
        console.log('❌ Storage test - Failed:', error.message);
        return false;
    }
}

// Test 3: Check message passing
async function testMessagePassing() {
    console.log('\n📋 Test 3: Message Passing');
    
    try {
        // Test sending a message to background script
        const response = await browser.runtime.sendMessage({ 
            action: 'test',
            data: 'test message'
        });
        
        if (response && response.success) {
            console.log('✅ Message passing - Success');
            return true;
        } else {
            console.log('❌ Message passing - No response or failed');
            return false;
        }
    } catch (error) {
        console.log('❌ Message passing - Failed:', error.message);
        return false;
    }
}

// Test 4: Check context menus
async function testContextMenus() {
    console.log('\n📋 Test 4: Context Menus');
    
    try {
        // Try to get all context menus
        const menus = await browser.contextMenus.getAll();
        console.log(`✅ Context menus - Found ${menus.length} menus`);
        return true;
    } catch (error) {
        console.log('❌ Context menus - Failed:', error.message);
        return false;
    }
}

// Test 5: Check preloaded prompts
async function testPreloadedPrompts() {
    console.log('\n📋 Test 5: Preloaded Prompts');
    
    try {
        const response = await browser.runtime.sendMessage({ 
            action: 'getFolders' 
        });
        
        if (response && response.folders) {
            const folderCount = response.folders.length;
            let promptCount = 0;
            
            response.folders.forEach(folder => {
                if (folder.prompts) {
                    promptCount += folder.prompts.length;
                }
            });
            
            console.log(`✅ Preloaded prompts - Found ${folderCount} folders with ${promptCount} prompts`);
            return true;
        } else {
            console.log('❌ Preloaded prompts - Failed to load');
            return false;
        }
    } catch (error) {
        console.log('❌ Preloaded prompts - Failed:', error.message);
        return false;
    }
}

// Run all tests
async function runAllTests() {
    console.log('🚀 Starting RCP Extension Tests...\n');
    
    const results = {
        browserAPIs: testBrowserAPIs(),
        storage: await testStorage(),
        messagePassing: await testMessagePassing(),
        contextMenus: await testContextMenus(),
        preloadedPrompts: await testPreloadedPrompts()
    };
    
    console.log('\n📊 Test Results Summary:');
    console.log('========================');
    
    let passedTests = 0;
    const totalTests = Object.keys(results).length;
    
    Object.entries(results).forEach(([test, passed]) => {
        const status = passed ? '✅ PASS' : '❌ FAIL';
        console.log(`${status} ${test.replace(/([A-Z])/g, ' $1').toLowerCase()}`);
        if (passed) passedTests++;
    });
    
    console.log(`\n🎯 Overall Result: ${passedTests}/${totalTests} tests passed`);
    
    if (passedTests === totalTests) {
        console.log('🎉 All tests passed! The extension is working correctly.');
    } else {
        console.log('⚠️  Some tests failed. Please check the extension configuration.');
    }
    
    return results;
}

// Auto-run tests when script is loaded
if (typeof browser !== 'undefined') {
    runAllTests().catch(console.error);
} else {
    console.log('❌ This script must be run in a Firefox extension context.');
    console.log('Please load it as a content script or background script in your extension.');
}

// Export functions for manual testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        testBrowserAPIs,
        testStorage,
        testMessagePassing,
        testContextMenus,
        testPreloadedPrompts,
        runAllTests
    };
}