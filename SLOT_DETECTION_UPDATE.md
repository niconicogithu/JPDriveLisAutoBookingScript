# Slot Detection Update - Implementation Complete

## Overview
Updated the slot detection system based on actual HTML structure from the Kanagawa e-Shinsei facility selection page.

## Changes Made

### 1. Updated `src/selectors.py`
Complete rewrite based on actual HTML structure:

**Key Selectors:**
- `CONSENT_CHECKBOX`: `input#reserveCaution[type='checkbox']` - Must be checked before selecting slots
- `SLOT_TABLE`: `table#TBL.time--table` - Main calendar table
- `DATE_HEADER_CELLS`: Date column headers (format: "01/18 (Sun)")
- `CATEGORY_ROW_PREFIX`: `tr[id^='height_auto_']` - Rows for each 予約枠名

**Slot Cell States:**
- Available: `td.time--table.time--th--date.tdSelect.enable` (green circle, clickable)
- Unavailable: `td.time--table.time--th--date.disable` (red X)
- Out of period: `td.time--table.time--th--date.time--cell--tri.none` (gray dash)

**SVG Icons for Visual Identification:**
- Available: `svg[aria-label='予約可能']` (green circle ○)
- Unavailable: `svg[aria-label='空き無']` (red X ×)
- Out of period: `svg[aria-label='時間外']` (gray dash －)
- Selected: `svg[aria-label='選択中']` (checkmark ✓)

### 2. Rewrote `src/slot_detector.py`
Complete implementation of slot detection logic:

**New Features:**
- `ensure_consent_checked()`: Automatically checks the consent checkbox before slot detection
- `check_availability()`: Detects available slots by:
  1. Ensuring consent checkbox is checked
  2. Getting date headers from table
  3. Finding rows matching target categories
  4. Looking for cells with class `tdSelect enable`
  5. Extracting clickable link elements
  6. Mapping column index to date
- `_get_date_headers()`: Extracts date strings from table headers

**Detection Logic:**
1. Finds all rows with `id^='height_auto_'`
2. Checks if row category matches target categories (e.g., "準中型車ＡＭ")
3. Finds all cells with class `tdSelect enable` (available slots)
4. Extracts the clickable `<a>` element inside each available cell
5. Maps cell position to date from header row
6. Returns first available slot found

### 3. Updated `src/booking_controller.py`
Improved monitoring loop:

**Changes:**
- Better logging with periodic status updates (every 60 seconds)
- Added check counter for better tracking
- Added 1-second wait after page refresh for stability
- Improved debug logging for each check cycle

### 4. Updated `src/config.py`
Expanded valid categories based on HTML:

**Valid Categories:**
- 普通車ＡＭ / 普通車ＰＭ (Regular car AM/PM)
- 準中型車ＡＭ / 準中型車ＰＭ (Semi-medium car AM/PM)
- 大型車ＡＭ / 大型車ＰＭ (Large car AM/PM)
- 大型特殊車ＡＭ / 大型特殊車ＰＭ (Large special car AM/PM)
- けん引車ＡＭ / けん引車ＰＭ (Towing car AM/PM)
- 大型二輪車ＡＭ / 大型二輪車ＰＭ (Large motorcycle AM/PM)

## HTML Structure Understanding

### Table Structure
```html
<table id="TBL" class="time--table">
  <tbody>
    <!-- Header row with dates -->
    <tr id="height_headday">
      <td class="time--table time--th--date bordernone">
        <span>01/20<br>(Tue)</span>
      </td>
      ...
    </tr>
    
    <!-- Category row (e.g., 準中型車ＡＭ) -->
    <tr id="height_auto_準中型車ＡＭ">
      <th class="time--table time--th main_color">準中型車ＡＭ</th>
      
      <!-- Available slot -->
      <td class="time--table time--th--date bordernone tdSelect enable" 
          onclick="selectDate('FC00023', '20260120', '1', this);">
        <a class="enable nooutline" href="#">
          <span class="sr-only">準中型車ＡＭは2026年01月20日</span>
          <svg aria-label="予約可能">...</svg> <!-- Green circle -->
        </a>
      </td>
      
      <!-- Unavailable slot -->
      <td class="time--table time--th--date bordernone disable">
        <svg aria-label="空き無">...</svg> <!-- Red X -->
      </td>
      
      <!-- Out of period slot -->
      <td class="time--table time--th--date bordernone time--cell--tri none">
        <svg aria-label="時間外">...</svg> <!-- Gray dash -->
      </td>
    </tr>
  </tbody>
</table>
```

### Consent Checkbox
```html
<input id="reserveCaution" 
       name="reserveCaution" 
       class="checkbox-input" 
       type="checkbox" 
       value="true">
```

## Testing

### Current Configuration (.env)
```
TARGET_CATEGORIES=準中型車ＡＭ
REFRESH_INTERVAL=5
HEADLESS=false
TEST_MODE=true
```

### How to Test
1. Run the system: `python main.py`
2. System will:
   - Navigate to facility selection page
   - Check consent checkbox automatically
   - Look for available slots in 準中型車ＡＭ category
   - Refresh every 5 seconds
   - Log status every 60 seconds
   - Click slot when found and send Telegram notification

### Expected Behavior
- Console shows: "Check #N: Looking for available slots..."
- If slot found: "✓ Found available slot: 準中型車ＡＭ on 01/20 (Tue)"
- If no slots: "Check #N: No slots available"
- Every 60 seconds: "Monitoring active - checked N times"

## Next Steps

1. **Test the implementation:**
   - Run with `HEADLESS=false` to watch the browser
   - Verify consent checkbox is checked automatically
   - Verify slot detection works correctly
   - Verify page refresh works

2. **Monitor for issues:**
   - Check logs for any errors
   - Verify dates are extracted correctly
   - Verify category matching works

3. **Production deployment:**
   - Set `HEADLESS=true` for background operation
   - Set `TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ` for actual booking
   - Adjust `REFRESH_INTERVAL` as needed (recommend 5-10 seconds)

## Files Modified
- `src/selectors.py` - Complete rewrite with actual selectors
- `src/slot_detector.py` - Complete rewrite with proper detection logic
- `src/booking_controller.py` - Improved monitoring loop
- `src/config.py` - Expanded valid categories

---

**Updated:** December 24, 2025
**Status:** Implementation complete, ready for testing
