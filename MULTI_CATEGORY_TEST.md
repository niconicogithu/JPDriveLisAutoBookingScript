# Multi-Category Test Guide

## 🎯 New Features to Test

1. **Navigate to 2nd month** - Clicks "1か月後" twice
2. **Multiple categories** - Checks 普通車ＡＭ AND 普通車ＰＭ
3. **First available wins** - Books whichever is available first

## Configuration

### Check `.env` File
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
```

## Start Testing

```bash
python main.py
```

## What to Watch For

### 1. Login ✓
```
INFO - Navigating to login page
INFO - ✓ Login successful
```

### 2. Navigate to Initial Page ✓
```
INFO - Navigating to initial page
```

### 3. First "1か月後" Click ✓
```
INFO - Clicking '1か月後' button twice to reach second month
INFO - ✓ Clicked '1か月後' button (1st time)
```
**In Browser:** Calendar advances one month

### 4. Second "1か月後" Click ✓
```
INFO - ✓ Clicked '1か月後' button (2nd time)
```
**In Browser:** Calendar advances another month (2 months total)

### 5. Arrival Confirmation ✓
```
INFO - ✓ Successfully navigated to facility selection page (2 months ahead)
```

### 6. Multi-Category Monitoring ✓
```
INFO - Target categories: ['普通車ＡＭ', '普通車ＰＭ']
DEBUG - Checking row for category: 普通車ＡＭ
DEBUG - Checking row for category: 普通車ＰＭ
```

### 7. Slot Detection ✓
```
INFO - ✓ Found available slot: 普通車ＰＭ on 02/15 (Sat)
```
**Note:** Could be either ＡＭ or ＰＭ, whichever is available first

### 8. Booking Flow ✓
```
INFO - Starting booking flow for 普通車ＰＭ on 02/15 (Sat)
INFO - ✓ Time selection page loaded
INFO - ✓ Selected time: ...
INFO - ✓ Clicked '予約する' button
INFO - ✓ Clicked '同意する' button
INFO - ✓ Reservation locked successfully
```

## Visual Verification

### In Browser Window

**Step 1: Initial Page**
- Shows current month calendar

**Step 2: After 1st Click**
- Calendar shows next month
- URL contains `movePage=oneMonthLater`

**Step 3: After 2nd Click**
- Calendar shows month after next (2 months ahead)
- URL still contains `movePage=oneMonthLater`

**Step 4: Monitoring**
- Both 普通車ＡＭ and 普通車ＰＭ rows visible
- System checks both for available slots (green circles)

**Step 5: Booking**
- Clicks first available slot (could be either category)
- Proceeds through booking flow

## Success Indicators

✅ Console shows: "Clicked '1か月後' button (1st time)"
✅ Console shows: "Clicked '1か月後' button (2nd time)"
✅ Console shows: "2 months ahead"
✅ Console shows both categories being checked
✅ Books first available slot from either category
✅ Telegram notification sent

## Test Scenarios

### Scenario 1: Only AM Available
```
Result: Books 普通車ＡＭ
Console: "Found available slot: 普通車ＡＭ on XX/XX"
```

### Scenario 2: Only PM Available
```
Result: Books 普通車ＰＭ
Console: "Found available slot: 普通車ＰＭ on XX/XX"
```

### Scenario 3: Both Available
```
Result: Books whichever appears first in table
Console: "Found available slot: 普通車ＡＭ on XX/XX"
or
Console: "Found available slot: 普通車ＰＭ on XX/XX"
```

### Scenario 4: Neither Available
```
Result: Continues monitoring
Console: "Check #N: No slots available"
Console: "Refreshing page for check #N+1"
```

## Troubleshooting

### Only One "1か月後" Click
**Symptom:** Shows only 1 month ahead
**Check:** Console should show TWO click messages
**Fix:** Verify button selector is correct

### Wrong Categories Checked
**Symptom:** Checks wrong categories
**Check:** `.env` file TARGET_CATEGORIES setting
**Fix:** Update to `普通車ＡＭ,普通車ＰＭ`

### Doesn't Book Available Slot
**Symptom:** Sees slot but doesn't book
**Check:** Category name must match exactly
**Fix:** Verify category names in console logs

### Books Wrong Category
**Symptom:** Books category not in list
**Check:** `.env` configuration
**Fix:** Ensure only desired categories listed

## Expected Timeline

```
0:00 - Start system
0:05 - Login complete
0:10 - Navigate to initial page
0:12 - First "1か月後" click
0:15 - Second "1か月後" click
0:18 - Arrive at 2nd month page
0:20 - Start monitoring
0:20+ - Check every 5 seconds
When found - Book immediately (3-5 seconds)
```

## Configuration Examples

### Test with Single Category
```bash
TARGET_CATEGORIES=普通車ＡＭ
```
**Expected:** Only checks AM slots

### Test with Multiple Categories
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
```
**Expected:** Checks both, books first available

### Test with Many Categories
```bash
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ,準中型車ＡＭ,準中型車ＰＭ
```
**Expected:** Maximum flexibility

## Verification Checklist

- [ ] Browser opens
- [ ] Login successful
- [ ] Navigate to initial page
- [ ] First "1か月後" click (see calendar advance)
- [ ] Second "1か月後" click (see calendar advance again)
- [ ] Console shows "2 months ahead"
- [ ] Console shows both categories being checked
- [ ] System detects available slot
- [ ] Books first available (AM or PM)
- [ ] Telegram notification received
- [ ] Browser stays open for form completion

## Success Criteria

✅ Navigates to 2nd month (not 1st)
✅ Checks multiple categories simultaneously
✅ Books first available slot
✅ Complete booking flow works
✅ Telegram notification sent

---

**Ready to test!** Run `python main.py` and verify all steps. 🚀
