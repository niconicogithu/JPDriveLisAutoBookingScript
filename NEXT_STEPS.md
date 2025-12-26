# ✅ Installation Complete!

Your JP Driving License Auto-Booking System is now installed and ready to configure.

## What Was Installed

✅ Virtual environment created (`venv/`)
✅ All Python dependencies installed
✅ Playwright Chromium browser installed
✅ Configuration file created (`.env`)

## Next Steps

### 1. Configure Your Telegram Bot (Required)

You need to set up a Telegram bot to receive notifications:

#### Get Bot Token:
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot` command
4. Follow the instructions
5. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Get Chat ID:
1. Start a chat with your new bot (send any message)
2. Visit this URL in your browser (replace `<YOUR_BOT_TOKEN>` with your actual token):
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. Look for `"chat":{"id":123456789}` in the response
4. Copy the chat ID number

### 2. Edit Configuration File

Open the `.env` file and add your credentials:

```bash
nano .env
```

Or use any text editor. Update these lines:

```bash
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
TELEGRAM_CHAT_ID=your_actual_chat_id_here
```

Save and close the file.

### 3. Test the System

**Always activate the virtual environment first:**

```bash
source venv/bin/activate
```

**Run in test mode (visible browser):**

```bash
python main.py --test-mode --headed
```

This will:
- Open a visible browser window
- Navigate to the agreement page
- Check the agreement checkbox automatically
- Click the "1か月後" button
- Navigate to the booking page
- Start monitoring for available slots
- Show detailed logs

**Watch for:**
- ✅ "Starting JP Driving License Auto-Booking System"
- ✅ Browser opens and navigates to the website
- ✅ "Monitoring active" messages every minute
- ⚠️ Any error messages about selectors

**Stop the system:**
- Press `Ctrl+C` in the terminal

### 4. Verify Selectors (Important!)

The CSS selectors in the code are based on assumptions. You MUST verify they match the actual website:

1. While the system is running in headed mode, open the browser DevTools (F12)
2. Inspect the table structure on the booking page
3. Check if the selectors in `src/slot_detector.py` match the actual HTML
4. Update selectors if needed

Common things to check:
- Table class name (currently expecting `rsv_table`)
- How categories are labeled (普通車, 準中型車)
- How AM/PM slots are distinguished
- What makes a slot clickable vs unavailable

### 5. Production Deployment (After Testing)

Once everything works in test mode:

1. Update `.env` for production:
   ```bash
   TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
   HEADLESS=true
   TEST_MODE=false
   ```

2. Run in production mode:
   ```bash
   source venv/bin/activate
   python main.py --headless
   ```

3. Monitor logs:
   ```bash
   tail -f logs/booking_system.log
   ```

## Quick Commands Reference

```bash
# Activate virtual environment (always do this first!)
source venv/bin/activate

# Test mode (visible browser, detailed logs)
python main.py --test-mode --headed

# Production mode (background, headless)
python main.py --headless

# View logs in real-time
tail -f logs/booking_system.log

# Stop the system (if running in foreground)
Ctrl+C

# Stop the system (if running in background)
pkill -f main.py

# Deactivate virtual environment
deactivate
```

## Troubleshooting

### "Configuration errors: TELEGRAM_BOT_TOKEN is required"
- Make sure you edited the `.env` file
- Check that your bot token and chat ID are correct (no quotes needed)

### "No module named 'playwright'"
- Make sure you activated the virtual environment: `source venv/bin/activate`
- You should see `(venv)` in your terminal prompt

### Browser doesn't open
- Make sure Playwright browsers are installed: `playwright install chromium`
- Check system dependencies (usually automatic on macOS)

### No slots detected
- This is normal if no slots are actually available
- The system will keep monitoring
- Verify selectors match the website structure

### Telegram notification not received
- Verify your bot token is correct
- Make sure you started a chat with your bot
- Test the bot token with curl:
  ```bash
  curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
  ```

## Documentation

- **QUICKSTART.md** - Quick setup guide
- **README.md** - Complete documentation
- **TESTING.md** - Detailed testing procedures
- **DEPLOYMENT.md** - Production deployment guide
- **CHECKLIST.md** - Production readiness checklist

## Support

If you encounter issues:
1. Check the logs: `tail -f logs/booking_system.log`
2. Run in headed mode to see what's happening
3. Review the documentation files
4. Check that selectors match the website structure

## Ready to Start?

```bash
# 1. Edit configuration
nano .env

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run in test mode
python main.py --test-mode --headed
```

Good luck with your driving test booking! 🚗✨
