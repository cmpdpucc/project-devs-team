#!/bin/bash
# scripts/install-opencode.sh
# Installs OpenCode via npm and configures the environment.

set -e

echo "🚀 Installing OpenCode..."

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm could not be found. Please install Node.js and npm first."
    exit 1
fi

# Install OpenCode globally
echo "📦 Running: npm install -g opencode-ai@latest"
npm install -g opencode-ai@latest

# Verify installation
if command -v opencode &> /dev/null; then
    echo "✅ OpenCode installed successfully version $(opencode --version)"
else
    echo "❌ OpenCode installation failed."
    exit 1
fi

# Check for Truecolor support
if [ -z "$COLORTERM" ] || [ "$COLORTERM" != "truecolor" ]; then
    echo "⚠️  Truecolor support not detected (COLORTERM=$COLORTERM)."
    echo "   Recommended: Add 'export COLORTERM=truecolor' to your shell profile (.bashrc/.zshrc)."
    
    # Attempt to auto-configure for current session
    export COLORTERM=truecolor
    echo "   Temporary fix applied for this session."
fi

# Check for recommended terminals
RECOMMENDED_TERMINALS=("wezterm" "alacritty" "ghostty" "kitty" "hyper")
FOUND_TERMINAL=false

for term in "${RECOMMENDED_TERMINALS[@]}"; do
    if command -v "$term" &> /dev/null; then
        echo "✅ Detected recommended terminal: $term"
        FOUND_TERMINAL=true
        break
    fi
done

if [ "$FOUND_TERMINAL" = false ]; then
    echo "ℹ️  Note: For the best TUI experience, consider using a modern GPU-accelerated terminal like WezTerm, Alacritty, Ghostty, or Kitty."
fi

echo "🎉 Setup complete! Configure OpenCode by editing config/opencode.json"
