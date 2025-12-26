# Quick Start Guide

Get the booking system running in 5 minutes.

## Option 1: Automated Setup (Recommended)

```bash
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Install Playwright browsers
- Create .env configuration file

Then edit your `.env` file with your credentials.

## Option 2: Manual Setup

### 1. Install Dependencies (2 minutes)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

## 2. Configure Telegram Bot (2 minutes)

### Get Bot Token
1. Open Telegram, search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy the bot token

### Get Chat ID
1. Start a chat with your bot (send any message)
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find `"chat":{"id":123456789}` in the response
4. Copy the chat ID

## 3. Create Configuration (1 minute)

```bash
cp .env.example .env
```

Edit `.env`:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
TARGET_CATEGORIES=準中型車ＡＭ
HEADLESS=false
TEST_MODE=true
```

## 4. Run the System

**Important:** Always activate the virtual environment first!

```bash
source venv/bin/activate
```

### Test Mode (Visible Browser)
```bash
python3 main.py --test-mode --headed
```

Watch the browser window and logs. Press Ctrl+C to stop.

### Production Mode (Background)
```bash
python3 main.py --headless
```

Monitor logs:
```bash
tail -f logs/booking_system.log
```

## That's It! 🎉

The system is now monitoring for available slots and will:
- ✅ Automatically book when slots become available
- ✅ Send you a Telegram notification
- ✅ Handle errors and retry automatically

## Next Steps

- Read [TESTING.md](TESTING.md) for detailed testing
- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Read [README.md](README.md) for full documentation

## Troubleshooting

**"Configuration errors"**
- Make sure you created `.env` file
- Check your bot token and chat ID are correct

**"No module named 'playwright'"**
- Run: `pip install -r requirements.txt`

**"Browser doesn't start"**
- Run: `playwright install chromium`

**"No slots detected"**
- This is normal if no slots are available
- The system will keep monitoring

## Quick Commands

```bash
# Start in test mode (visible)
python3 main.py --test-mode --headed

# Start in production (background)
python3 main.py --headless

# View logs
tail -f logs/booking_system.log

# Stop (if running in foreground)
Ctrl+C

# Stop (if running in background)
pkill -f main.py
```

## Support

- Full documentation: [README.md](README.md)
- Testing guide: [TESTING.md](TESTING.md)
- Deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Production checklist: [CHECKLIST.md](CHECKLIST.md)
