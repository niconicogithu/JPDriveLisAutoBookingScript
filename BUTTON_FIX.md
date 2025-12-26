# Button Selector Fix

## Issue

The "1か月後" button was not being clicked properly.

## Root Cause

The button value contains a full-width "＞" character (not a regular ">"), which wasn't being matched by the generic selectors.

**Actual HTML:**
```html
<input type="button" 
       value="1か月後＞" 
       title="1か月後に進む" 
       aria-label="1か月後のカレンダーページへ" 
       onclick="nextDate('oneMonthLater');" 
       class="button">
```

## Solution

Updated `src/browser_manager.py` with more specific selectors that match the actual HTML:

```python
button_selectors = [
    "input[type='button'][value='1か月後＞']",  # Exact match with full-width >
    "input[type='button'][title='1か月後に進む']",  # Match by title
    "input[type='button'][onclick*='oneMonthLater']",  # Match by onclick
    "input[type='button'].button[value*='1か月後']",  # Match by class and partial value
    "input[type='button'][value*='1か月後']",  # Partial match (fallback)
    # ... other fallbacks
]
```

## Priority Order

1. **Exact value match** - Most specific, includes full-width >
2. **Title attribute** - Unique identifier
3. **Onclick function** - Matches the JavaScript function
4. **Class + partial value** - Combines class and text
5. **Partial value** - Fallback for variations

## Testing

Test the fix:

```bash
source venv/bin/activate
python main.py --test-mode --headed --log-level DEBUG
```

**Expected logs:**
```
DEBUG - Looking for '1か月後' button
DEBUG - Found '1か月後' button with selector: input[type='button'][value='1か月後＞']
INFO - Clicked '1か月後' button
DEBUG - Waiting for facility selection page to load
INFO - Successfully navigated to facility selection page
```

## Key Learnings

1. **Full-width characters matter** - Japanese sites use full-width punctuation (＞ vs >)
2. **Exact matches are better** - More reliable than partial matches
3. **Multiple attributes** - Use title, onclick, class for robustness
4. **Always verify HTML** - Don't assume structure, inspect actual elements

## Files Changed

- `src/browser_manager.py` - Updated button selectors
- `SELECTORS_REFERENCE.md` - Created with verified HTML
- `BUTTON_FIX.md` - This document

## Next Steps

1. Test the button click works
2. Verify navigation completes
3. Continue with slot detection testing
4. Document other verified selectors in `SELECTORS_REFERENCE.md`

## Status

✅ **Fixed** - Button selector updated with exact HTML match

---

**Date:** December 24, 2025
**Issue:** Button not clicked
**Solution:** Exact selector with full-width character
**Status:** Ready for testing
