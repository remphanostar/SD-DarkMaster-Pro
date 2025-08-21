// Test script to verify the preloaded prompts library is working correctly
console.log('🧪 Testing Preloaded Prompts Library');

// Test 1: Check if PRELOADED_PROMPTS_LIBRARY is available
function testLibraryAvailability() {
    console.log('📋 Test 1: Library Availability');
    
    if (typeof PRELOADED_PROMPTS_LIBRARY !== 'undefined' && PRELOADED_PROMPTS_LIBRARY) {
        console.log('✅ PRELOADED_PROMPTS_LIBRARY is available');
        
        const categories = Object.keys(PRELOADED_PROMPTS_LIBRARY);
        console.log(`📂 Found ${categories.length} categories: ${categories.join(', ')}`);
        
        let totalPrompts = 0;
        categories.forEach(category => {
            const prompts = PRELOADED_PROMPTS_LIBRARY[category].prompts || [];
            totalPrompts += prompts.length;
            console.log(`📝 ${category}: ${prompts.length} prompts`);
        });
        
        console.log(`🎯 Total prompts in library: ${totalPrompts}`);
        
        if (totalPrompts >= 30) {
            console.log('✅ Library contains expected number of prompts (30+)');
            return true;
        } else {
            console.log('❌ Library contains fewer prompts than expected');
            return false;
        }
    } else {
        console.log('❌ PRELOADED_PROMPTS_LIBRARY is not available');
        return false;
    }
}

// Test 2: Check library structure
function testLibraryStructure() {
    console.log('\n📋 Test 2: Library Structure');
    
    if (!PRELOADED_PROMPTS_LIBRARY) {
        console.log('❌ Library not available for structure test');
        return false;
    }
    
    const requiredCategories = [
        'programming_&_development',
        'writing_&_content_creation',
        'business_&_productivity',
        'analysis_&_research',
        'education_&_learning'
    ];
    
    let allCategoriesPresent = true;
    
    requiredCategories.forEach(category => {
        if (PRELOADED_PROMPTS_LIBRARY[category]) {
            console.log(`✅ Category '${category}' is present`);
        } else {
            console.log(`❌ Category '${category}' is missing`);
            allCategoriesPresent = false;
        }
    });
    
    // Check prompt structure
    let promptStructureValid = true;
    Object.keys(PRELOADED_PROMPTS_LIBRARY).forEach(category => {
        const categoryData = PRELOADED_PROMPTS_LIBRARY[category];
        if (categoryData.prompts && Array.isArray(categoryData.prompts)) {
            categoryData.prompts.forEach((prompt, index) => {
                if (!prompt.id || !prompt.text || !prompt.title) {
                    console.log(`❌ Invalid prompt structure in ${category} at index ${index}`);
                    promptStructureValid = false;
                }
            });
        } else {
            console.log(`❌ Invalid prompts structure in category ${category}`);
            promptStructureValid = false;
        }
    });
    
    if (promptStructureValid) {
        console.log('✅ All prompts have valid structure');
    }
    
    return allCategoriesPresent && promptStructureValid;
}

// Test 3: Check specific prompts
function testSpecificPrompts() {
    console.log('\n📋 Test 3: Specific Prompts');
    
    if (!PRELOADED_PROMPTS_LIBRARY) {
        console.log('❌ Library not available for specific prompts test');
        return false;
    }
    
    const expectedPrompts = [
        { category: 'programming_&_development', title: 'Professional Coder' },
        { category: 'writing_&_content_creation', title: 'Academic Assistant Pro' },
        { category: 'business_&_productivity', title: 'Business Strategy Analyst' },
        { category: 'analysis_&_research', title: 'Data Analysis Pro' },
        { category: 'education_&_learning', title: 'All-around Teacher' }
    ];
    
    let allPromptsFound = true;
    
    expectedPrompts.forEach(expected => {
        const category = PRELOADED_PROMPTS_LIBRARY[expected.category];
        if (category) {
            const prompt = category.prompts.find(p => p.title === expected.title);
            if (prompt) {
                console.log(`✅ Found prompt: ${expected.title}`);
            } else {
                console.log(`❌ Missing prompt: ${expected.title}`);
                allPromptsFound = false;
            }
        } else {
            console.log(`❌ Missing category: ${expected.category}`);
            allPromptsFound = false;
        }
    });
    
    return allPromptsFound;
}

// Run all tests
function runLibraryTests() {
    console.log('🚀 Starting Preloaded Prompts Library Tests...\n');
    
    const results = {
        availability: testLibraryAvailability(),
        structure: testLibraryStructure(),
        specificPrompts: testSpecificPrompts()
    };
    
    console.log('\n📊 Library Test Results:');
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
        console.log('🎉 All library tests passed! The extension should have 30+ preloaded prompts.');
    } else {
        console.log('⚠️  Some library tests failed. The extension may not have all expected prompts.');
    }
    
    return results;
}

// Auto-run tests when script is loaded
if (typeof document !== 'undefined') {
    // Running in browser context
    document.addEventListener('DOMContentLoaded', function() {
        runLibraryTests();
    });
} else {
    // Running in extension context
    runLibraryTests();
}

// Export functions for manual testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        testLibraryAvailability,
        testLibraryStructure,
        testSpecificPrompts,
        runLibraryTests
    };
}