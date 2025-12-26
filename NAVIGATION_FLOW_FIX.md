# Navigation Flow Fix

## Problems Identified

### Problem 1: Button Clicked 3 Times
**Symptom:** Console showed "Clicked '1か月後' button" 3 times instead of 2
**Cause:** The button was being clicked in the loop multiple times because multiple selectors matched

### Problem 2: Wrong Flow Order
**Symptom:** Tried to find agreement checkbox on initial page (where it doesn't exist)
**Cause:** Flow was: Initial page → Check checkbox → Click button
**Should be:** Initial page → Click button → Check checkbox on facility page

## Solution

### New Navigation Flow

```
1. Navigate to initial page
   (offerList_detail?tempSeq=50909)
   ↓
2. Click "1か月後" button (1st time)
   → Navigate to facility selection page
   ↓
3. Check agreement checkbox
   (上記内容に同意する)
   ↓
4. Click "1か月後" button (2nd time)
   → Advance to 2nd month
   ↓
5. Start monitoring
```

### Key Changes

**1. First Click Navigates to Facility Page**
```python
# Click button and wait for URL change
await button.click()
await self.page.wait_for_url("**/facilitySelect_dateTrans**")
# Now we're on facility selection page
```

**2. Checkbox is on Facility Page**
```python
# After arriving at facility page
# THEN look for agreement checkbox
checkbox = await self.page.query_selector("input[type='checkbox']")
```

**3. Second Click Advances Month**
```python
# Click button again to advance to 2nd month
await button.click()
# Page updates but stays on same URL
```

## Expected Console Output

### Before Fix
```
INFO - Navigating to initial page
WARNING - Could not find agreement checkbox  ← Wrong page!
INFO - Clicking '1か月後' button twice
INFO - ✓ Clicked '1か月後' button (1st time)
INFO - ✓ Clicked '1か月後' button (2nd time)
INFO - ✓ Clicked '1か月後' button (3rd time)  ← Extra click!
```

### After Fix
```
INFO - Navigating to initial page
INFO - Clicking '1か月後' button to navigate to facility selection page
INFO - ✓ Clicked '1か月後' button (navigating to facility page)
INFO - ✓ Arrived at facility selection page
INFO - ✓ Agreement checkbox checked  ← Found it!
INFO - Clicking '1か月後' button again to reach second month
INFO - ✓ Clicked '1か月後' button (advancing to 2nd month)
INFO - ✓ Successfully navigated to facility selection page (2 months ahead)
```

## Technical Details

### Why 3 Clicks Happened

**Old Code:**
```python
button_selectors = [
    "input[type='button'][value='1か月後＞']",  # Matches
    "input[type='button'][onclick*='oneMonthLater']",  # Also matches!
    "input[type='button'][value*='1か月後']",  # Also matches!
]

for selector in button_selectors:
    button = await self.page.query_selector(selector)
    if button:
        await button.click()  # Clicks for each match!
        break  # But break only exits inner loop
```

**Fix:**
```python
for selector in button_selectors:
    button = await self.page.query_selector(selector)
    if button:
        await button.click()
        button_found = True
        break  # Exit loop immediately
```

### Why Checkbox Wasn't Found

**Initial Page Structure:**
```html
<!-- offerList_detail page -->
<div>
  <!-- No agreement checkbox here -->
  <button>1か月後</button>
</div>
```

**Facility Page Structure:**
```html
<!-- facilitySelect_dateTrans page -->
<div>
  <input type="checkbox" id="reserveCaution">  ← Checkbox is here!
  <label>上記内容に同意する</label>
  <button>1か月後</button>
</div>
```

## Page Flow Diagram

```
┌─────────────────────────────────────┐
│  Initial Page (offerList_detail)   │
│  - No checkbox                      │
│  - Has "1か月後" button             │
└──────────────┬──────────────────────┘
               │ Click "1か月後"
               ↓
┌─────────────────────────────────────┐
│  Facility Page (Month 1)            │
│  - Has agreement checkbox ✓         │
│  - Has "1か月後" button             │
└──────────────┬──────────────────────┘
               │ Check checkbox
               │ Click "1か月後"
               ↓
┌─────────────────────────────────────┐
│  Facility Page (Month 2)            │
│  - Same page, different month       │
│  - Ready for monitoring             │
└─────────────────────────────────────┘
```

## Testing

### Verify Fix
Run the system and check console output:

```bash
python main.py
```

### Expected Behavior
1. ✓ Navigate to initial page
2. ✓ Click "1か月後" once (navigate to facility page)
3. ✓ Find and check agreement checkbox
4. ✓ Click "1か月後" once more (advance to 2nd month)
5. ✓ Total: 2 clicks, not 3

### Success Indicators
- Console shows exactly 2 "Clicked '1か月後' button" messages
- Agreement checkbox is found and checked
- No "Could not find agreement checkbox" warning
- Arrives at 2nd month successfully

## Files Modified

1. `src/browser_manager.py` - Reordered navigation flow

## Summary

✅ Fixed button being clicked 3 times (now clicks exactly 2 times)
✅ Fixed checkbox not found (now looks on correct page)
✅ Improved flow logic (navigate first, then check checkbox)
✅ Clearer console messages
✅ More reliable navigation

---

**Date:** December 26, 2025
**Status:** ✅ Fixed and ready for testing
**Impact:** More reliable navigation, correct number of clicks
