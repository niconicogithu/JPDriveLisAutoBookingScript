# Quick Start Guide - JP Driving License Auto-Booking

## Prerequisites

1. Python 3.8+ installed
2. Virtual environment activated
3. Dependencies installed: `pip install -r requirements.txt`
4. Playwright browsers installed: `playwright install chromium`
5. `.env` file configured with your Telegram credentials

## Configuration

Edit `.env` file:

```bash
# Required: Your Telegram bot credentials
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Target categories (comma-separated, no spaces)
TARGET_CATEGORIES=準中型車ＡＭ

# How often to check (in seconds)
REFRESH_INTERVAL=5

# Show browser window (false) or run hidden (true)
HEADLESS=false

# Test mode
TEST_MODE=true

# Logging level
LOG_LEVEL=INFO
```

## Running the System

### Test Mode (Recommended First)

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Run the system
python main.py
```

### What to Expect

1. **Browser opens** (if HEADLESS=false)
2. **Navigates** to facility selection page
3. **Checks consent** checkbox automatically
4. **Monitors** for available slots every 5 seconds
5. **Logs status** every 60 seconds
6. **Clicks slot** when found
7. **Sends notification** via Telegram

### Console Output

```
INFO - Starting JP Driving License Auto-Booking System
INFO - Target categories: ['準中型車ＡＭ']
INFO - Test mode: True
INFO - Refresh interval: 5 seconds
INFO - Starting browser (headless=False)
INFO - Navigating to initial page
INFO - Agreement checkbox checked
INFO - Clicked '1か月後' button
INFO - Successfully navigated to facility selection page
INFO - Starting monitoring loop
DEBUG - Check #1: Looking for available slots...
DEBUG - Consent checkbox already checked
DEBUG - Found 14 date columns
DEBUG - Checking row for category: 準中型車ＡＭ
```

### If Slot Found

```
INFO - ✓ Found available slot: 準中型車ＡＭ on 01/20 (Tue)
INFO - Available slot detected: 準中型車ＡＭ on 01/20 (Tue)
INFO - Starting booking flow for 準中型車ＡＭ on 01/20 (Tue)
DEBUG - Clicking slot element
DEBUG - Waiting for time selection page
DEBUG - Selecting first available time
DEBUG - Clicking reservation button
INFO - Booking completed in 2.34 seconds
INFO - Booking successful! Stopping monitoring.
```

### If No Slots Available

```
DEBUG - Check #1: No slots available
DEBUG - Refreshing page for check #2
DEBUG - Check #2: Looking for available slots...
DEBUG - Check #2: No slots available
...
INFO - Monitoring active - checked 12 times
```

## Stopping the System

Press `Ctrl+C` to stop:

```
^C
INFO - Received keyboard interrupt
INFO - Stop requested
INFO - Cleaning up resources
INFO - Stopping browser
INFO - Shutdown complete
```

## Production Mode

Once tested, update `.env` for production:

```bash
# Use your actual target categories
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ

# Run in background
HEADLESS=true

# Disable test mode
TEST_MODE=false

# Reduce logging
LOG_LEVEL=INFO
```

Then run:

```bash
python main.py
```

## Troubleshooting

### "Configuration errors: TELEGRAM_BOT_TOKEN is required"
- Add your Telegram bot token to `.env`
- Get it from @BotFather on Telegram

### "Could not find agreement checkbox"
- Website structure may have changed
- Check logs/navigation_error.png for screenshot
- Update selectors in `src/browser_manager.py`

### "No available slots found" (but you see slots on website)
- Check if category name matches exactly
- Run with `LOG_LEVEL=DEBUG` to see details
- Verify consent checkbox is checked

### Browser doesn't open
- Check if Playwright is installed: `playwright install chromium`
- Try running with `HEADLESS=false`

### "Timeout waiting for facility selection page"
- Network might be slow
- Increase timeout in `src/browser_manager.py`
- Check internet connection

## Logs

All logs are saved to:
- `logs/booking_system.log` - Full log file
- Console output - Real-time status

## Support

Check these files for more details:
- `README.md` - Full documentation
- `SLOT_DETECTION_UPDATE.md` - Technical details
- `IMPLEMENTATION_SUMMARY.md` - What was implemented
- `TESTING.md` - Testing guide

---

**Ready to book your driving test!** 🚗
