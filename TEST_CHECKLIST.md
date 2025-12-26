# Test Checklist - JP Driving License Auto-Booking

## Pre-Test Verification ✅

- [x] Virtual environment activated
- [x] Dependencies installed
- [x] Playwright browsers installed
- [x] `.env` configured with Telegram credentials
- [x] `HEADLESS=false` (browser visible for testing)
- [x] `TARGET_CATEGORIES=準中型車ＡＭ`

## Test Execution

### Start the System
```bash
python main.py
```

Or use the test script:
```bash
./test_run.sh
```

## What to Watch For

### 1. Browser Launch ✓
- [ ] Browser window opens
- [ ] Navigates to initial page
- [ ] Console shows: "Starting browser (headless=False)"

### 2. Initial Navigation ✓
- [ ] Finds agreement checkbox (or continues without it)
- [ ] Clicks "1か月後" button
- [ ] Navigates to facility selection page
- [ ] Console shows: "Successfully navigated to facility selection page"

### 3. Consent Checkbox ✓
- [ ] Automatically checks "上記内容に同意する"
- [ ] Console shows: "Consent checkbox successfully checked"
- [ ] Checkbox is visibly checked in browser

### 4. Slot Detection ✓
- [ ] System checks for available slots
- [ ] Console shows: "Check #N: Looking for available slots..."
- [ ] Finds date headers (14 columns)
- [ ] Checks 準中型車ＡＭ row
- [ ] Detects available slots (green circles)

### 5. Slot Found ✓
- [ ] Console shows: "✓ Found available slot: 準中型車ＡＭ on XX/XX (Day)"
- [ ] Console shows: "Available slot detected"
- [ ] Console shows: "Starting booking flow"

### 6. Time Selection Page ✓
- [ ] Browser navigates to time selection page
- [ ] Console shows: "✓ Time selection page loaded"
- [ ] System selects first available time checkbox
- [ ] Console shows: "✓ Selected time: ..."
- [ ] Time checkbox is visibly checked in browser

### 7. Reserve Button ✓
- [ ] System clicks "予約する" button
- [ ] Console shows: "✓ Clicked '予約する' button"
- [ ] Browser navigates to next page

### 8. Procedure Explanation Page ✓
- [ ] Browser shows procedure explanation page
- [ ] Console shows: "✓ Procedure explanation page loaded"
- [ ] System clicks "同意する" button
- [ ] Console shows: "✓ Clicked '同意する' button - Reservation is now locked!"

### 9. Success Message ✓
- [ ] Console shows success banner:
```
============================================================
🎉 RESERVATION LOCKED SUCCESSFULLY!
============================================================
Category: 準中型車ＡＭ
Date: XX/XX (Day)
Time: ...
============================================================
⚠️  IMPORTANT: Browser will remain open
📝 Please complete the remaining form fields manually
🔔 Telegram notification has been sent
============================================================

Press Ctrl+C when you're done to close the browser
```

### 10. Telegram Notification ✓
- [ ] Telegram notification received
- [ ] Message shows:
  - 🎉 予約ロック成功！
  - Category, Date, Time
  - Instructions in Japanese
  - Reminder to complete form

### 11. Browser State ✓
- [ ] Browser remains open
- [ ] Shows form page for user to complete
- [ ] System waits (doesn't close)

### 12. Manual Completion
- [ ] User can fill remaining form fields
- [ ] User can submit the form
- [ ] User receives confirmation email

### 13. Shutdown ✓
- [ ] User presses Ctrl+C
- [ ] Console shows: "User requested shutdown"
- [ ] Console shows: "Cleaning up resources"
- [ ] Console shows: "Stopping browser"
- [ ] Console shows: "Shutdown complete"
- [ ] Browser closes cleanly

## Expected Console Output

```
INFO - ============================================================
INFO - JP Driving License Auto-Booking System
INFO - ============================================================
INFO - Starting JP Driving License Auto-Booking System
INFO - Target categories: ['準中型車ＡＭ']
INFO - Test mode: True
INFO - Refresh interval: 5 seconds
INFO - Starting browser (headless=False)
INFO - Navigating to initial page: https://...
INFO - Clicked '1か月後' button
INFO - Successfully navigated to facility selection page
INFO - Starting monitoring loop
INFO - Will check for slots every 5 seconds
DEBUG - Check #1: Looking for available slots...
INFO - Checking consent checkbox
INFO - Consent checkbox successfully checked
DEBUG - Found 14 date columns
DEBUG - Checking row for category: 準中型車ＡＭ
DEBUG - Found 3 available slots for 準中型車ＡＭ
INFO - ✓ Found available slot: 準中型車ＡＭ on 01/20 (Tue)
INFO - Available slot detected: 準中型車ＡＭ on 01/20 (Tue)
INFO - Starting booking flow for 準中型車ＡＭ on 01/20 (Tue)
DEBUG - Clicking slot element
DEBUG - Waiting for time selection page
INFO - ✓ Time selection page loaded
DEBUG - Selecting first available time
INFO - ✓ Selected time: 準中型車ＡＭの08時30分の予約選択
DEBUG - Clicking '予約する' button
INFO - ✓ Clicked '予約する' button
DEBUG - Waiting for procedure explanation page
INFO - ✓ Procedure explanation page loaded
DEBUG - Clicking '同意する' button
INFO - ✓ Clicked '同意する' button - Reservation is now locked!
INFO - ✓ Reservation locked successfully in 3.15 seconds
INFO - Browser will remain open for you to complete the remaining form fields
INFO - Telegram notification sent successfully
INFO - ============================================================
INFO - 🎉 RESERVATION LOCKED SUCCESSFULLY!
INFO - ============================================================
INFO - Category: 準中型車ＡＭ
INFO - Date: 01/20 (Tue)
INFO - Time: 準中型車ＡＭの08時30分の予約選択
INFO - ============================================================
INFO - ⚠️  IMPORTANT: Browser will remain open
INFO - 📝 Please complete the remaining form fields manually
INFO - 🔔 Telegram notification has been sent
INFO - ============================================================
INFO - 
INFO - Press Ctrl+C when you're done to close the browser
```

## Troubleshooting

### Issue: "Consent checkbox not found"
- Check if page structure changed
- Verify selector: `input#reserveCaution`
- System should continue anyway

### Issue: "No available slots found"
- Normal if no slots available
- System will keep checking every 5 seconds
- Wait for slots to appear

### Issue: "Timeout waiting for time selection page"
- Network might be slow
- System should continue anyway
- Check browser to see if page loaded

### Issue: "Could not find time selection element"
- Check if page structure changed
- Verify checkboxes with class `checkbox_hide`
- Check logs for details

### Issue: "Could not find '予約する' button"
- Check if button selector changed
- Verify button has onclick="showWarningPossibleCntOver()"
- Check browser DevTools

### Issue: "Could not find '同意する' button"
- Check if button selector changed
- Verify button has value="同意する"
- Check browser DevTools

### Issue: Browser closes immediately
- Should NOT happen anymore
- System should wait for Ctrl+C
- Check booking_controller.py

## Success Criteria

✅ All steps complete without errors
✅ Reservation is locked
✅ Telegram notification received
✅ Browser stays open
✅ User can complete form
✅ Clean shutdown with Ctrl+C

## Test Results

**Date:** _____________
**Time:** _____________
**Result:** ⬜ Pass / ⬜ Fail

**Notes:**
_____________________________________________
_____________________________________________
_____________________________________________

**Issues Found:**
_____________________________________________
_____________________________________________
_____________________________________________

**Screenshots:**
- [ ] Facility selection page
- [ ] Time selection page
- [ ] Procedure explanation page
- [ ] Final form page
- [ ] Telegram notification

---

**Ready to test!** Run `python main.py` and follow this checklist.
