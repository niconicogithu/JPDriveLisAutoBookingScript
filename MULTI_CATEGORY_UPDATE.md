# Multi-Category and Two-Month Navigation Update

## Overview
Updated the system to:
1. Navigate to the **second month** (click "1か月後" button twice)
2. Support **multiple categories** simultaneously (e.g., 普通車ＡＭ AND 普通車ＰＭ)
3. Book the **first available slot** from any target category

## Changes Made

### 1. Updated `src/browser_manager.py`

**Navigation Flow Changed:**
```python
Old: Click "1か月後" once → First month
New: Click "1か月後" twice → Second month (2 months ahead)
```

**Implementation:**
```python
# First click
await button.click()
await page.wait_for_timeout(2000)
await page.wait_for_load_state("networkidle")

# Second click
await button.click()
await page.wait_for_timeout(2000)
await page.wait_for_load_state("networkidle")
```

**Console Output:**
```
INFO - Clicking '1か月後' button twice to reach second month
INFO - ✓ Clicked '1か月後' button (1st time)
INFO - ✓ Clicked '1か月後' button (2nd time)
INFO - ✓ Successfully navigated to facility selection page (2 months ahead)
```

### 2. Updated `.env` Configuration

**Multiple Categories Support:**
```bash
# Old (single category)
TARGET_CATEGORIES=準中型車ＡＭ

# New (multiple categories)
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
```

**How It Works:**
- System checks ALL specified categories
- Books the FIRST available slot found
- Categories are checked in order (left to right)

**Examples:**
```bash
# Single category
TARGET_CATEGORIES=普通車ＡＭ

# Two categories (AM or PM)
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ

# Three categories (any of these)
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ,準中型車ＡＭ

# Multiple vehicle types
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ,準中型車ＡＭ,準中型車ＰＭ
```

### 3. Slot Detection Logic (Already Implemented)

**Multi-Category Detection:**
```python
for row in rows:
    category_text = get_category_name(row)
    
    # Check if this category is in our target list
    if category_text not in self.target_categories:
        continue  # Skip this category
    
    # Check for available slots in this category
    available_cells = find_available_slots(row)
    
    if available_cells:
        # Found an available slot!
        return first_available_slot
```

**Priority:**
- Categories are checked in the order they appear in the table
- First available slot wins
- No preference between categories

## Complete Flow

### 1. Login
```
Navigate to login page
→ Enter email and password
→ Click login button
→ ✓ Login successful
```

### 2. Navigate to Second Month
```
Navigate to initial page
→ Click "1か月後" (1st time)
→ Wait for page load
→ Click "1か月後" (2nd time)
→ Wait for page load
→ ✓ Arrive at second month booking page
```

### 3. Monitor Multiple Categories
```
Check consent checkbox
→ Look for available slots in:
  - 普通車ＡＭ
  - 普通車ＰＭ
→ Find first available slot
→ Book immediately
```

### 4. Complete Booking
```
Click available slot
→ Select time
→ Click "予約する"
→ Click "同意する"
→ ✓ Reservation locked
```

## Configuration Examples

### Scenario 1: Only Morning Slots
```bash
TARGET_CATEGORIES=普通車ＡＭ
```
- Only books morning (AM) slots
- Ignores afternoon (PM) slots

### Scenario 2: Morning OR Afternoon
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
```
- Books either morning or afternoon
- Whichever is available first

### Scenario 3: Multiple Vehicle Types
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ,準中型車ＡＭ,準中型車ＰＭ
```
- Books any of these categories
- Maximum flexibility

### Scenario 4: Specific Preference
```bash
TARGET_CATEGORIES=普通車ＡＭ,準中型車ＡＭ
```
- Only morning slots
- Either vehicle type

## Expected Console Output

```
INFO - Starting JP Driving License Auto-Booking System
INFO - Target categories: ['普通車ＡＭ', '普通車ＰＭ']
INFO - Starting browser (headless=False)
INFO - Navigating to login page
INFO - ✓ Login successful
INFO - Navigating to initial page
INFO - Clicking '1か月後' button twice to reach second month
INFO - ✓ Clicked '1か月後' button (1st time)
INFO - ✓ Clicked '1か月後' button (2nd time)
INFO - ✓ Successfully navigated to facility selection page (2 months ahead)
INFO - Starting monitoring loop
INFO - Will check for slots every 5 seconds
DEBUG - Check #1: Looking for available slots...
INFO - Checking consent checkbox
INFO - Consent checkbox successfully checked
DEBUG - Found 14 date columns
DEBUG - Checking row for category: 普通車ＡＭ
DEBUG - Checking row for category: 普通車ＰＭ
DEBUG - Found 2 available slots for 普通車ＰＭ
INFO - ✓ Found available slot: 普通車ＰＭ on 02/15 (Sat)
INFO - Available slot detected: 普通車ＰＭ on 02/15 (Sat)
INFO - Starting booking flow for 普通車ＰＭ on 02/15 (Sat)
...
```

## Timeline Comparison

### Old Behavior (1 Month Ahead)
```
Today: December 24, 2025
Click "1か月後" once
→ Shows: January 2026 slots
```

### New Behavior (2 Months Ahead)
```
Today: December 24, 2025
Click "1か月後" twice
→ Shows: February 2026 slots
```

## Advantages

### 1. More Availability
- Second month typically has more open slots
- Less competition from other users
- Better chance of getting preferred dates

### 2. Flexibility
- Can specify multiple categories
- System books whichever is available first
- No need to choose between AM/PM beforehand

### 3. Efficiency
- One configuration works for multiple scenarios
- No need to restart for different categories
- Automatic selection of first available

## Testing

### Test Configuration
```bash
# In .env file
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
```

### Run System
```bash
python main.py
```

### Verify
1. ✓ Browser opens
2. ✓ Login successful
3. ✓ Clicks "1か月後" twice
4. ✓ Arrives at second month page
5. ✓ Checks both 普通車ＡＭ and 普通車ＰＭ
6. ✓ Books first available slot
7. ✓ Telegram notification sent

## Important Notes

### Category Order
- Categories are checked in the order specified
- First available slot is booked immediately
- No preference between categories

### Booking Priority
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
```
- If both have slots on same date:
  - System books whichever appears first in the table
  - Usually determined by table row order
  - Not by configuration order

### Single Booking
- System books ONE slot only
- Stops monitoring after successful booking
- Cannot book multiple slots simultaneously

## Troubleshooting

### "Could not find '1か月後' button for second click"
- First click may have failed
- Page may not have loaded
- Check logs and screenshot

### "No available slots found" (but you see slots)
- Check category names match exactly
- Verify categories in `.env` are correct
- Check console for which categories are being checked

### Wrong month displayed
- Verify both clicks succeeded
- Check console logs for confirmation
- Look for "2 months ahead" message

## Files Modified

1. `src/browser_manager.py` - Added second "1か月後" click
2. `.env` - Updated TARGET_CATEGORIES to multiple
3. `.env.example` - Added multi-category examples

---

**Date:** December 24, 2025
**Status:** ✅ Complete and tested
**Features:** 
- ✅ Navigate to second month (2 months ahead)
- ✅ Support multiple categories simultaneously
- ✅ Book first available slot from any category
