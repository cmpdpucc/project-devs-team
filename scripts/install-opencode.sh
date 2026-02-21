#!/bin/bash

# scripts/install-opencode.sh
# Purpose: Installs OpenCode via npm and verifies Truecolor support.
# Usage: ./scripts/install-opencode.sh

set -e

echo "🚀 Starting OpenCode installation..."

# 1. Check for npm
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# 2. Install/Update OpenCode
echo "📦 Installing opencode-ai globally..."
if npm install -g opencode-ai@latest; then
    echo "✅ Successfully installed opencode-ai."
else
    echo "❌ Error: Failed to install opencode-ai. Please check your npm configuration or permissions."
    exit 1
fi

# 3. Verify Installation
if ! command -v opencode &> /dev/null; then
    echo "⚠️ Warning: 'opencode' command not found in PATH."
    echo "   Ensure your npm global bin directory is in your PATH."
    # Try to find where it was installed
    NPM_BIN=$(npm bin -g 2>/dev/null || echo "")
    if [[ -n "$NPM_BIN" && -f "$NPM_BIN/opencode" ]]; then
        echo "   Found at: $NPM_BIN/opencode"
        echo "   Please add $NPM_BIN to your PATH."
    fi
    exit 1
else
    VERSION=$(opencode --version 2>/dev/null || echo "unknown")
    echo "✅ Verified installation: opencode version $VERSION"
fi

# 4. Truecolor Check
echo "🎨 Checking Truecolor support..."
if [[ "$COLORTERM" != "truecolor" ]]; then
    echo "⚠️  Warning: COLORTERM is not set to 'truecolor'."
    echo "   To ensure the best TUI experience, please add the following to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
    echo "   export COLORTERM=truecolor"
    
    # Export for current session just in case this is sourced
    export COLORTERM=truecolor
else
    echo "✅ Truecolor support is enabled (COLORTERM=$COLORTERM)."
fi

echo "🎉 Setup complete! Run 'opencode' to start."
