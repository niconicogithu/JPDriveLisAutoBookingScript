# Manual Testing Guide

This guide walks through manual testing of the booking system with the real website.

## Prerequisites

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Set up your `.env` file with valid credentials:
```bash
cp .env.example .env
# Edit .env with your Telegram bot token and chat ID
```

## Test Mode Configuration

For initial testing, use these settings in `.env`:

```bash
TELEGRAM_BOT_TOKEN=your_actual_bot_token
TELEGRAM_CHAT_ID=your_actual_chat_id
TARGET_CATEGORIES=準中型車ＡＭ
REFRESH_INTERVAL=5
HEADLESS=false
TEST_MODE=true
LOG_LEVEL=DEBUG
```

## Manual Testing Steps

### Step 1: Verify Configuration

```bash
python3 main.py --test-mode --headed --log-level DEBUG
```

Expected behavior:
- System starts without configuration errors
- Browser window opens (visible)
- Logs show "Starting JP Driving License Auto-Booking System"
- Logs show target categories: `['準中型車ＡＭ']`

### Step 2: Verify Navigation

Watch the browser window:
- Should navigate to: https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/offerList_detail?tempSeq=50909&accessFrom=offerList
- Should check the agreement checkbox (上記内容に同意する)
- Should click the "1か月後" button
- Should navigate to: https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_dateTrans?movePage=oneMonthLater
- Page should load completely
- Logs should show "Navigating to initial page"
- Logs should show "Agreement checkbox checked"
- Logs should show "Clicked '1か月後' button"
- Logs should show "Successfully navigated to facility selection page"

### Step 3: Verify Slot Detection

Observe the logs:
- Every 5 seconds, should see "Checking availability for categories"
- If no slots available: "No available slots found"
- If slots available: "Found available slot: 準中型車ＡＭ on [date]"

### Step 4: Inspect Page Elements (If Detection Fails)

If the system doesn't detect slots:

1. Open browser DevTools (F12)
2. Inspect the table structure
3. Look for:
   - Table class name (currently expecting `rsv_table`)
   - How dates are displayed
   - How categories are labeled
   - How AM/PM slots are distinguished
   - What makes a slot clickable (link vs disabled)

4. Update selectors in `src/slot_detector.py`:
```python
SELECTORS = {
    "slot_containers": "your_actual_selector",
    "普通車ＡＭ": "your_actual_selector",
    "普通車ＰＭ": "your_actual_selector",
    "準中型車ＡＭ": "your_actual_selector",
}
```

### Step 5: Test Booking Flow (If Slot Detected)

**WARNING: This will attempt a real booking!**

If a slot is detected:
1. Watch the browser perform these actions:
   - Click on the available slot
   - Navigate to time selection page
   - Select first available time
   - Click reservation button (予約)

2. Check logs for:
   - "Starting booking flow"
   - "Clicking slot element"
   - "Waiting for time selection page"
   - "Selecting first available time"
   - "Clicking reservation button"
   - "Booking completed in X seconds"

3. Check Telegram:
   - Should receive notification with booking details
   - Message should include category, date, and time

### Step 6: Test Error Handling

Test network error handling:
1. Disconnect internet briefly
2. Observe logs: "Network error: ... Retrying in 5 seconds..."
3. Reconnect internet
4. System should resume monitoring

Test graceful shutdown:
1. Press Ctrl+C
2. Observe logs: "Received keyboard interrupt"
3. Browser should close cleanly
4. Logs should show "Shutdown complete"

## Troubleshooting

### Selectors Not Working

The website structure may differ from expectations. You need to:

1. Run with headed mode and DEBUG logging
2. Inspect the actual HTML structure
3. Update these files:
   - `src/slot_detector.py` - Update `SELECTORS` dictionary
   - `src/booking_handler.py` - Update button selectors

Common issues:
- Table class name is different
- Category text is different (e.g., spaces, full-width characters)
- AM/PM cells use different classes
- Links have different structure

### No Slots Ever Detected

This is normal if no slots are actually available. To verify detection works:

1. Check the website manually in a browser
2. Confirm there are actually available slots
3. If slots exist but aren't detected, update selectors

### Booking Flow Fails

If detection works but booking fails:

1. Check logs for specific error
2. Common issues:
   - Time selection page URL is different
   - Time selection elements use different selectors
   - Reservation button text or selector is different

3. Update `src/booking_handler.py` with correct selectors

### Telegram Notification Not Received

1. Verify bot token: `curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"`
2. Verify you've started a chat with your bot
3. Check logs for Telegram API errors
4. Test notification manually:
```python
import asyncio
from src.telegram_notifier import TelegramNotifier
from src.booking_handler import BookingResult

async def test():
    notifier = TelegramNotifier("your_token", "your_chat_id")
    result = BookingResult(
        success=True,
        category="準中型車ＡＭ",
        date="2025-12-25",
        time="09:00"
    )
    await notifier.send_booking_success(result)

asyncio.run(test())
```

## Production Testing

Once test mode works, switch to production:

1. Update `.env`:
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
HEADLESS=true
TEST_MODE=false
```

2. Run in background:
```bash
nohup python3 main.py > output.log 2>&1 &
```

3. Monitor logs:
```bash
tail -f logs/booking_system.log
```

## Success Criteria

✅ System starts without errors
✅ Browser navigates to correct URL
✅ Page refreshes every 5 seconds
✅ Slots are detected when available
✅ Booking flow completes successfully
✅ Telegram notification is received
✅ System handles errors gracefully
✅ System shuts down cleanly

## Next Steps

After successful manual testing:
1. Document any selector changes you made
2. Run in production mode with real target categories
3. Set up as a background service (see README.md)
4. Monitor logs regularly
