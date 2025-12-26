# JP Driving License Auto-Booking System

Automated booking system for Kanagawa e-Shinsei driving license test appointments.

## Features

- 🔄 Continuous monitoring of available time slots
- 🤖 Automatic booking when slots become available
- 📱 Telegram notifications for successful bookings
- 🧪 Test mode for safe testing with 準中型車ＡＭ category
- 🎯 Configurable target categories
- 📝 Comprehensive logging with rotation
- 🔒 Secure credential management via environment variables

## Prerequisites

- Python 3.9 or higher
- Telegram account and bot token

## Setup

### 1. Install Dependencies

**Create a virtual environment (recommended):**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

**Alternative (system-wide, not recommended):**

```bash
pip3 install -r requirements.txt
playwright install chromium
```

### 2. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Save the bot token provided by BotFather
4. Start a chat with your new bot (send any message)
5. Get your chat ID by visiting:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   Look for the `"chat":{"id":...}` field in the response

### 3. Configure Environment Variables

Copy the example configuration file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```bash
# Required: Your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321

# Target categories (comma-separated)
TARGET_CATEGORIES=準中型車ＡＭ

# Other settings
REFRESH_INTERVAL=5
HEADLESS=false
TEST_MODE=true
LOG_LEVEL=INFO
```

## Usage

### Test Mode (Recommended First)

Test the system with 準中型車ＡＭ category only:

```bash
python main.py --test-mode --headed
```

This will:
- Run with visible browser window for debugging
- Monitor only 準中型車ＡＭ category
- Allow you to verify the booking flow works correctly

### Production Mode

Once tested, run in production mode:

```bash
# Activate virtual environment first
source venv/bin/activate

# Run in production
python main.py --headless
```

Or configure `.env` for production:
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
HEADLESS=true
TEST_MODE=false
```

Then run:
```bash
python main.py
```

### Command-Line Options

```bash
python main.py [OPTIONS]

Options:
  --headless          Run browser in headless mode
  --headed            Run browser in headed mode (visible)
  --test-mode         Run in test mode (準中型車ＡＭ only)
  --log-level LEVEL   Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

### Running as Background Process

#### Using nohup (Linux/macOS)

```bash
nohup python main.py --headless > output.log 2>&1 &
```

#### Using systemd (Linux)

Create `/etc/systemd/system/booking-system.service`:

```ini
[Unit]
Description=JP Driving License Auto-Booking System
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python main.py --headless
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable booking-system
sudo systemctl start booking-system
sudo systemctl status booking-system
```

## Configuration Options

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather | Required | `123456789:ABC...` |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Required | `987654321` |
| `TARGET_CATEGORIES` | Categories to monitor (comma-separated) | Required | `普通車ＡＭ,普通車ＰＭ` |
| `REFRESH_INTERVAL` | Seconds between checks | `5` | `5` |
| `HEADLESS` | Run browser in headless mode | `true` | `true` or `false` |
| `TEST_MODE` | Enable test mode | `false` | `true` or `false` |
| `LOG_LEVEL` | Logging verbosity | `INFO` | `DEBUG`, `INFO`, `WARNING` |

### Valid Categories

- `普通車ＡＭ` - Regular Car AM
- `普通車ＰＭ` - Regular Car PM
- `準中型車ＡＭ` - Semi-medium Car AM

## Monitoring

### Logs

Logs are stored in the `logs/` directory:
- `booking_system.log` - Current log file
- Automatically rotated when reaching 100MB
- Up to 7 backup files kept

### Log Levels

- `DEBUG` - Detailed information for debugging
- `INFO` - Normal operation messages
- `WARNING` - Recoverable errors (network issues, missing elements)
- `ERROR` - Serious errors (booking failures)
- `CRITICAL` - Fatal errors requiring intervention

### Checking Status

Monitor the log file in real-time:
```bash
tail -f logs/booking_system.log
```

The system logs "Monitoring active" every minute to confirm it's running.

## Troubleshooting

### "Configuration errors: TELEGRAM_BOT_TOKEN is required"

Make sure you've created a `.env` file with your credentials. Copy from `.env.example`:
```bash
cp .env.example .env
```

### "Could not find reservation button"

The website structure may have changed. You need to:
1. Run in headed mode: `python main.py --headed`
2. Inspect the website elements using browser DevTools
3. Update selectors in `src/slot_detector.py` and `src/booking_handler.py`

### Browser doesn't start

Install Playwright browsers:
```bash
playwright install chromium
```

### No slots detected

This is normal - the system will keep monitoring. Make sure:
- You're monitoring the correct categories
- The website is accessible
- Check logs for any errors

### Telegram notifications not received

1. Verify your bot token and chat ID are correct
2. Make sure you've started a chat with your bot
3. Check logs for Telegram API errors
4. Test your bot token:
   ```bash
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
   ```

## Development

### Running Tests

```bash
pytest
```

### Project Structure

```
.
├── main.py                 # Entry point
├── src/
│   ├── config.py          # Configuration management
│   ├── logger.py          # Logging setup
│   ├── browser_manager.py # Browser automation
│   ├── slot_detector.py   # Slot detection logic
│   ├── booking_handler.py # Booking flow
│   ├── telegram_notifier.py # Telegram notifications
│   ├── booking_controller.py # Main controller
│   ├── error_handler.py   # Error handling
│   └── selectors.py       # CSS selectors
├── tests/                 # Test files
├── logs/                  # Log files
├── .env                   # Your configuration (not in git)
├── .env.example          # Example configuration
└── requirements.txt      # Python dependencies
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your Telegram bot token secure
- Rotate your bot token periodically
- The `.gitignore` file is configured to exclude sensitive files

## Legal Disclaimer

This tool is for educational purposes. Make sure you comply with the website's terms of service. Use responsibly and at your own risk.

## License

MIT License - See LICENSE file for details
