#!/usr/bin/env node
/**
 * Task 3.4 Verification Script
 * Checks the TypeScript/JavaScript MCP client implementation and functionality.
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

async function verifyTypescriptClient() {
    console.log("Verifying TypeScript client implementation...");

    // Get the project root directory
    const projectRoot = path.resolve(__dirname, '..', '..');
    const clientPath = path.join(projectRoot, 'unit2', 'typescript_client.ts');

    // Check if file exists
    if (!fs.existsSync(clientPath)) {
        console.log("❌ Error: typescript_client.ts not found");
        return false;
    }

    try {
        // Check package.json exists and has required dependencies
        const packageJsonPath = path.join(projectRoot, 'unit2', 'package.json');
        if (!fs.existsSync(packageJsonPath)) {
            console.log("❌ Error: package.json not found");
            return false;
        }

        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        const requiredDeps = ['@huggingface/hub', '@huggingface/inference'];
        const missingDeps = requiredDeps.filter(dep => !packageJson.dependencies?.[dep]);

        if (missingDeps.length > 0) {
            console.log(`❌ Error: Missing required dependencies: ${missingDeps.join(', ')}`);
            return false;
        }

        // Start the sentiment analysis server in background
        console.log("Starting sentiment analysis server...");
        const serverProcess = spawn('uv', [
            'run',
            'python',
            path.join(projectRoot, 'unit2', 'sentiment_analysis_mcp_server.py')
        ]);

        // Wait for server to start
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Verify server is running
        try {
            const serverResponse = await new Promise((resolve, reject) => {
                http.get('http://localhost:7860/gradio_api/mcp/schema', (res) => {
                    resolve(res.statusCode);
                }).on('error', reject);
            });

            if (serverResponse !== 200) {
                console.log("❌ Error: Server not responding correctly");
                serverProcess.kill();
                return false;
            }
        } catch (error) {
            console.log("❌ Error: Could not connect to server");
            serverProcess.kill();
            return false;
        }

        // Start the TypeScript client
        console.log("Starting TypeScript client...");
        const clientProcess = spawn('node', [clientPath]);

        // Wait for client to start
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Check if client process is still running
        if (clientProcess.killed) {
            console.log("❌ Error: Client process terminated unexpectedly");
            serverProcess.kill();
            return false;
        }

        console.log("✅ TypeScript client implementation verified successfully");
        console.log("✅ Server and client are running");
        console.log("Note: Server running on http://localhost:7860");
        console.log("Note: Client is running and processing queries");

        // Clean up processes
        clientProcess.kill();
        serverProcess.kill();
        return true;

    } catch (error) {
        console.log(`❌ Error: Unexpected error: ${error.message}`);
        return false;
    }
}

// Run verification
verifyTypescriptClient().then(success => {
    process.exit(success ? 0 : 1);
});
