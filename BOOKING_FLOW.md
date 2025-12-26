# Booking Flow Documentation

This document describes the complete booking flow on the Kanagawa e-Shinsei website.

## Complete Booking Flow

### Step 1: Initial Agreement Page

**URL:** `https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/offerList_detail?tempSeq=50909&accessFrom=offerList`

**Actions Required:**
1. Check the agreement checkbox (上記内容に同意する)
2. Click the "1か月後" button

**Implementation:** `src/browser_manager.py` - `navigate_to_facility_page()`

### Step 2: Facility Selection Page

**URL:** `https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_dateTrans?movePage=oneMonthLater`

**Actions Required:**
1. Monitor the page for available slots
2. Refresh every 5 seconds
3. Detect clickable slots in target categories:
   - 普通車ＡＭ (Regular Car AM)
   - 普通車ＰＭ (Regular Car PM)
   - 準中型車ＡＭ (Semi-medium Car AM)

**Implementation:** `src/slot_detector.py` - `check_availability()`

### Step 3: Slot Selection

**Actions Required:**
1. Click on the available slot (circular element or link)
2. Wait for navigation to time selection page

**Implementation:** `src/booking_handler.py` - `_click_slot()`

### Step 4: Time Selection Page

**URL:** `https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_decide`

**Actions Required:**
1. Wait for page to fully load
2. Select the first available time slot (radio button or link)
3. Click the reservation button (予約)

**Implementation:** `src/booking_handler.py` - `_select_first_available_time()` and `_click_reservation_button()`

### Step 5: Confirmation

**Actions Required:**
1. Verify booking was successful
2. Send Telegram notification with booking details

**Implementation:** `src/telegram_notifier.py` - `send_booking_success()`

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Agreement Page                                      │
│ https://dshinsei.e-kanagawa.lg.jp/.../offerList_detail     │
│                                                             │
│ Actions:                                                    │
│ 1. Check "上記内容に同意する" checkbox                        │
│ 2. Click "1か月後" button                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Facility Selection Page (Monitoring Loop)          │
│ https://dshinsei.e-kanagawa.lg.jp/.../facilitySelect_...   │
│                                                             │
│ Actions:                                                    │
│ 1. Check for available slots every 5 seconds               │
│ 2. Detect clickable elements for target categories         │
│ 3. When slot found → proceed to Step 3                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Click Available Slot                               │
│                                                             │
│ Actions:                                                    │
│ 1. Click on the circular element or link                   │
│ 2. Wait for navigation                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Time Selection Page                                │
│ https://dshinsei.e-kanagawa.lg.jp/.../facilitySelect_decide│
│                                                             │
│ Actions:                                                    │
│ 1. Wait for page load                                      │
│ 2. Select first available time (radio button)             │
│ 3. Click "予約" button                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Confirmation & Notification                        │
│                                                             │
│ Actions:                                                    │
│ 1. Verify booking success                                  │
│ 2. Send Telegram notification                              │
│ 3. Stop monitoring                                         │
└─────────────────────────────────────────────────────────────┘
```

## Error Handling

### Network Errors
- **Retry:** Wait 5 seconds and retry
- **Max Retries:** 3 attempts with exponential backoff
- **Logging:** Log error details

### Page Load Errors
- **Retry:** Refresh and try again
- **Continue:** Don't crash, continue monitoring
- **Screenshot:** Save screenshot for debugging

### Element Not Found
- **Log:** Log warning
- **Continue:** Continue to next refresh cycle
- **Screenshot:** Save screenshot if in debug mode

### Booking Flow Errors
- **Log:** Log detailed error
- **Resume:** Resume monitoring for next available slot
- **Notify:** Send error notification via Telegram (optional)

## Timing Requirements

- **Initial Navigation:** < 10 seconds
- **Refresh Interval:** 5 seconds (configurable)
- **Slot Detection:** < 1 second
- **Complete Booking Flow:** < 10 seconds
- **Telegram Notification:** < 5 seconds

## Selectors to Verify

When testing, verify these selectors match the actual website:

### Agreement Page
- Checkbox: `input[type='checkbox']` with text containing "同意"
- Button: Element with text "1か月後"

### Facility Selection Page
- Table: `table.rsv_table` or similar
- Date cells: First column of each row
- Category labels: Text containing "普通車", "準中型車"
- AM/PM cells: Cells with class `am` or `pm`
- Available slots: Clickable links or elements (not disabled)

### Time Selection Page
- Radio buttons: `input[type='radio']`
- Time options: Radio buttons with time values
- Reservation button: Button or input with text "予約"

## Testing the Flow

### Manual Testing

1. **Test Agreement Page:**
   ```bash
   source venv/bin/activate
   python main.py --test-mode --headed
   ```
   - Watch browser navigate to agreement page
   - Verify checkbox is checked
   - Verify "1か月後" button is clicked
   - Verify navigation to facility page

2. **Test Slot Detection:**
   - Let system run and monitor logs
   - Check if slots are detected correctly
   - Verify only target categories are monitored

3. **Test Booking Flow:**
   - Wait for available slot (or manually create one for testing)
   - Watch complete booking flow
   - Verify time selection works
   - Verify reservation button is clicked

### Debugging

If any step fails:

1. **Check logs:**
   ```bash
   tail -f logs/booking_system.log
   ```

2. **Check screenshots:**
   - Error screenshots saved to `logs/navigation_error.png`

3. **Run in headed mode:**
   ```bash
   python main.py --test-mode --headed --log-level DEBUG
   ```

4. **Inspect elements:**
   - Open DevTools (F12)
   - Inspect actual HTML structure
   - Update selectors in code if needed

## Configuration

### Test Mode
```bash
TARGET_CATEGORIES=準中型車ＡＭ
TEST_MODE=true
HEADLESS=false
```

### Production Mode
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
TEST_MODE=false
HEADLESS=true
```

## Important Notes

1. **Agreement Step:** The system now handles the initial agreement page automatically
2. **Refresh Strategy:** After each refresh, the system goes through the agreement flow again
3. **Selector Verification:** You MUST verify selectors match the actual website
4. **Test First:** Always test with 準中型車ＡＭ before production use
5. **Monitor Logs:** Keep an eye on logs for any errors or warnings

## Troubleshooting

### "Could not find agreement checkbox"
- The checkbox selector may be different
- Inspect the page and update selectors in `src/browser_manager.py`

### "Could not find '1か月後' button"
- The button text or selector may be different
- Check if button is actually present on the page
- Update selectors in `src/browser_manager.py`

### Navigation timeout
- Network may be slow
- Increase timeout in `navigate_to_facility_page()`
- Check if URL pattern matches

### Slots not detected
- Verify you're on the correct page
- Check table structure matches selectors
- Update selectors in `src/slot_detector.py`

## Next Steps

1. Test the updated navigation flow
2. Verify all selectors match the website
3. Test complete booking flow end-to-end
4. Deploy to production once verified
