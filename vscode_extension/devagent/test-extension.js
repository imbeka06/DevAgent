#!/usr/bin/env node
/**
 * DevAgent Extension Verification Script
 * Tests if all required files exist and configuration is correct
 */

const fs = require('fs');
const path = require('path');

const baseDir = __dirname;
const tests = [];
let passed = 0;
let failed = 0;

// Helper to check file existence
function fileExists(filePath, description) {
    const fullPath = path.join(baseDir, filePath);
    const exists = fs.existsSync(fullPath);
    const status = exists ? '✅' : '❌';
    console.log(`${status} ${description}: ${filePath}`);
    if (exists) passed++;
    else failed++;
    return exists;
}

// Helper to check JSON validity
function validateJSON(filePath, description) {
    const fullPath = path.join(baseDir, filePath);
    try {
        const content = fs.readFileSync(fullPath, 'utf8');
        JSON.parse(content);
        console.log(`✅ ${description} (valid JSON): ${filePath}`);
        passed++;
        return true;
    } catch (e) {
        console.log(`❌ ${description} (invalid JSON): ${filePath}`);
        console.log(`   Error: ${e.message}`);
        failed++;
        return false;
    }
}

// Helper to check file contains string
function fileContains(filePath, searchString, description) {
    const fullPath = path.join(baseDir, filePath);
    try {
        const content = fs.readFileSync(fullPath, 'utf8');
        const found = content.includes(searchString);
        const status = found ? '✅' : '❌';
        console.log(`${status} ${description}`);
        if (found) passed++;
        else failed++;
        return found;
    } catch (e) {
        console.log(`❌ ${description} - File read error`);
        failed++;
        return false;
    }
}

console.log('🚀 DevAgent Extension Verification\n');
console.log('=' .repeat(50));

// Test 1: Icon file exists
console.log('\n📦 CHECKING RESOURCES:');
fileExists('resources/icon.svg', 'Icon SVG file');

// Test 2: Check package.json
console.log('\n📋 CHECKING PACKAGE.JSON:');
validateJSON('package.json', 'package.json');
fileContains('package.json', '"icon": "resources/icon.svg"', 'Top-level icon property');
fileContains('package.json', '"icon": "resources/icon.svg"', 'Activity bar icon reference');
fileContains('package.json', 'devagent-sidebar', 'Sidebar container ID');
fileContains('package.json', 'devagent.chatView', 'Chat view registration');

// Test 3: Check compiled output
console.log('\n⚙️ CHECKING COMPILED OUTPUT:');
fileExists('out/extension.js', 'Compiled extension.js');
fileExists('out/extension.js.map', 'Source map');

// Test 4: Check source code
console.log('\n💻 CHECKING SOURCE CODE:');
fileExists('src/extension.ts', 'TypeScript source');
fileContains('src/extension.ts', 'DevAgentChatViewProvider', 'Chat provider class');
fileContains('src/extension.ts', 'registerWebviewViewProvider', 'Webview registration');
fileContains('src/extension.ts', 'askAgent', 'Message handler');

// Test 5: Check launch configuration
console.log('\n🎯 CHECKING DEBUG CONFIGURATION:');
fileExists('.vscode/launch.json', 'launch.json (comments OK in VS Code)');
fileContains('.vscode/launch.json', 'extensionHost', 'Extension host debugger');

// Test 6: Check .vscodeignore
console.log('\n📝 CHECKING PACKAGING:');
fileExists('.vscodeignore', '.vscodeignore file');
fileContains('.vscodeignore', 'src/**', 'Source files excluded from package');

// Summary
console.log('\n' + '='.repeat(50));
console.log(`\n📊 RESULTS: ${passed} passed, ${failed} failed\n`);

if (failed === 0) {
    console.log('✅ ALL TESTS PASSED! Extension is ready to run.');
    console.log('\n🚀 NEXT STEPS:');
    console.log('   1. Press F5 in VS Code to start debugging');
    console.log('   2. Look for the rocket icon in the Activity Bar');
    console.log('   3. Click it to open the Chat interface');
    console.log('   4. Try typing a message!');
    process.exit(0);
} else {
    console.log('❌ TESTS FAILED! Fix the issues above.');
    process.exit(1);
}
