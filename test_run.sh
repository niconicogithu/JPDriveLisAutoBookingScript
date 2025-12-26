#!/bin/bash

echo "=========================================="
echo "JP Driving License Auto-Booking System"
echo "Test Run"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  Target: 準中型車ＡＭ"
echo "  Headless: false (browser visible)"
echo "  Refresh: 5 seconds"
echo ""
echo "Starting system..."
echo ""

# Activate virtual environment and run
source venv/bin/activate
python main.py
