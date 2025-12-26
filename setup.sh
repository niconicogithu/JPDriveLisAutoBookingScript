#!/bin/bash

# Setup script for JP Driving License Auto-Booking System

echo "🚀 Setting up JP Driving License Auto-Booking System..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment and install dependencies
echo "📥 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Python dependencies installed"
echo ""

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium
echo "✅ Playwright browsers installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env configuration file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your Telegram credentials!"
    echo "   1. Get bot token from @BotFather on Telegram"
    echo "   2. Get chat ID from https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
    echo "   3. Edit .env file: nano .env"
else
    echo "✅ .env file already exists"
fi
echo ""

echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env file with your credentials: nano .env"
echo "  2. Activate virtual environment: source venv/bin/activate"
echo "  3. Run in test mode: python main.py --test-mode --headed"
echo ""
echo "For more information, see:"
echo "  - QUICKSTART.md for quick setup guide"
echo "  - README.md for full documentation"
echo "  - TESTING.md for testing instructions"
