# Quick Reference Card

## Essential Commands

```bash
# Activate virtual environment (ALWAYS DO THIS FIRST!)
source venv/bin/activate

# Test mode (visible browser, test category only)
python main.py --test-mode --headed

# Production mode (background, real categories)
python main.py --headless

# View logs in real-time
tail -f logs/booking_system.log

# Stop (foreground)
Ctrl+C

# Stop (background)
pkill -f main.py
```

## Booking Flow

1. **Agreement Page** → Check checkbox + Click "1か月後"
2. **Facility Page** → Monitor for available slots (refresh every 5s)
3. **Slot Found** → Click available slot
4. **Time Selection** → Select first time + Click "予約"
5. **Notification** → Telegram message sent

## Configuration (.env)

```bash
# Required
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Categories
TARGET_CATEGORIES=準中型車ＡＭ          # Test mode
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ  # Production

# Settings
REFRESH_INTERVAL=5
HEADLESS=false  # Test: false, Production: true
TEST_MODE=true  # Test: true, Production: false
LOG_LEVEL=INFO
```

## URLs

- **Initial:** https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/offerList_detail?tempSeq=50909&accessFrom=offerList
- **Facility:** https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_dateTrans?movePage=oneMonthLater
- **Time Selection:** https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_decide

## Categories

- `普通車ＡＭ` - Regular Car AM
- `普通車ＰＭ` - Regular Car PM
- `準中型車ＡＭ` - Semi-medium Car AM (for testing)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: pip` | Use `pip3` or activate venv |
| `No module named 'playwright'` | Activate venv: `source venv/bin/activate` |
| Configuration errors | Edit `.env` file with your credentials |
| Browser won't start | Run: `playwright install chromium` |
| No slots detected | Normal if none available, verify selectors |
| Telegram not working | Check token/chat ID, start chat with bot |
| Navigation fails | Check agreement checkbox/button selectors |

## Files to Check

- **Selectors:** `src/slot_detector.py`, `src/browser_manager.py`, `src/booking_handler.py`
- **Selector Reference:** `SELECTORS_REFERENCE.md` - Verified HTML and selectors
- **Config:** `.env`
- **Logs:** `logs/booking_system.log`
- **Screenshots:** `logs/navigation_error.png` (on errors)

## Documentation

- **NEXT_STEPS.md** - Complete setup guide
- **BOOKING_FLOW.md** - Detailed flow documentation
- **TESTING.md** - Testing procedures
- **README.md** - Full documentation
- **DEPLOYMENT.md** - Production deployment

## Telegram Bot Setup

1. Search `@BotFather` on Telegram
2. Send `/newbot`
3. Get token
4. Start chat with your bot
5. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
6. Get chat ID from response

## Test Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Telegram bot configured
- [ ] `.env` file edited
- [ ] Test mode runs successfully
- [ ] Agreement page navigation works
- [ ] Facility page loads
- [ ] Slot detection works
- [ ] Selectors verified
- [ ] Telegram notification received

## Production Checklist

- [ ] All tests passed
- [ ] Selectors verified with real website
- [ ] `.env` updated for production
- [ ] Running in headless mode
- [ ] Logs being monitored
- [ ] Telegram notifications working
- [ ] Error handling tested

## Emergency Stop

```bash
# Find process
ps aux | grep main.py

# Kill process
kill <PID>

# Or force kill
pkill -9 -f main.py
```

## Log Levels

- **DEBUG** - Detailed information (testing)
- **INFO** - Normal operations (production)
- **WARNING** - Recoverable errors
- **ERROR** - Serious errors
- **CRITICAL** - Fatal errors

## Support

Need help? Check:
1. Logs: `tail -f logs/booking_system.log`
2. Run in headed mode: `python main.py --test-mode --headed`
3. Check documentation files
4. Verify selectors match website
