# Selectors Reference

This document contains the actual HTML elements and their selectors for the Kanagawa e-Shinsei website.

## Agreement Page

**URL:** `https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/offerList_detail?tempSeq=50909&accessFrom=offerList`

### 1か月後 Button

**Actual HTML:**
```html
<input type="button" 
       value="1か月後＞" 
       title="1か月後に進む" 
       aria-label="1か月後のカレンダーページへ" 
       onclick="nextDate('oneMonthLater');" 
       class="button">
```

**Selectors (in order of preference):**
```python
"input[type='button'][value='1か月後＞']"  # Exact match
"input[type='button'][title='1か月後に進む']"  # By title
"input[type='button'][onclick*='oneMonthLater']"  # By onclick
"input[type='button'].button[value*='1か月後']"  # By class + partial value
```

**Implementation:** `src/browser_manager.py` line ~120

### Agreement Checkbox

**Expected HTML:** (To be verified)
```html
<input type="checkbox" ...>
<!-- Near text containing "上記内容に同意する" -->
```

**Selectors:**
```python
"input[type='checkbox']"  # Generic, verified by nearby text
```

**Implementation:** `src/browser_manager.py` line ~90

## Facility Selection Page

**URL:** `https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_dateTrans?movePage=oneMonthLater`

### Table Structure

**Actual HTML Structure:**
```html
<table>
  <thead>
    <tr>
      <th>施設名</th>
      <th>予約名</th>
      <th>02/15 (Sun)</th>
      <th>02/16 (Mon)</th>
      <!-- ... more date columns -->
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>普通車ＡＭ</td>
      <td>×</td>  <!-- Not available -->
      <td>×</td>
      <td>○</td>  <!-- Available! -->
      <!-- ... more cells -->
    </tr>
    <tr>
      <td>準中型車ＡＭ</td>
      <td>-</td>  <!-- No slot -->
      <td>○</td>  <!-- Available! -->
      <td>-</td>
      <!-- ... more cells -->
    </tr>
  </tbody>
</table>
```

**Availability Indicators:**
- **○** (Green circle) = Available slot - CLICKABLE
- **×** (Red X) = Not available
- **-** (Dash) = No slot for this day

**Categories (Row Labels):**
- 普通車ＡＭ (Regular Car AM)
- 普通車ＰＭ (Regular Car PM)
- 準中型車ＡＭ (Semi-medium Car AM)
- 準中型車ＰＭ (Semi-medium Car PM)
- 大型車ＡＭ (Large Car AM)
- 大型車ＰＭ (Large Car PM)
- 中型車ＡＭ (Medium Car AM)
- 中型車ＰＭ (Medium Car PM)
- 大型特殊車ＡＭ (Large Special Car AM)
- 大型特殊車ＰＭ (Large Special Car PM)

**Detection Logic:**
```python
# 1. Find all table rows
rows = await page.query_selector_all("table tbody tr")

# 2. For each row, check if category matches target
category_cell = await row.query_selector("td:first-child")
category_text = await category_cell.inner_text()

# 3. If category matches, check all cells for "○"
cells = await row.query_selector_all("td")
for cell in cells:
    cell_text = await cell.inner_text()
    if "○" in cell_text:
        # Found available slot!
        link = await cell.query_selector("a")
```

**Implementation:** `src/slot_detector.py`

## Time Selection Page

**URL:** `https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_decide`

### Time Radio Buttons

**Expected HTML:** (To be verified)
```html
<input type="radio" name="time" value="09:00">
<input type="radio" name="time" value="10:00">
```

**Selectors:**
```python
"input[type='radio'][name*='time']"
"input[type='radio']"
```

**Implementation:** `src/booking_handler.py` line ~100

### Reservation Button

**Expected HTML:** (To be verified)
```html
<button>予約</button>
<!-- OR -->
<input type="submit" value="予約">
```

**Selectors:**
```python
"button:has-text('予約')"
"input[type='submit'][value*='予約']"
"a:has-text('予約')"
"button[type='submit']"
```

**Implementation:** `src/booking_handler.py` line ~130

## How to Update Selectors

### 1. Identify the Element

Run in headed mode:
```bash
source venv/bin/activate
python main.py --test-mode --headed --log-level DEBUG
```

Open DevTools (F12) and inspect the element.

### 2. Get the HTML

Right-click the element → Copy → Copy outerHTML

### 3. Create Selector

Based on the HTML attributes, create a specific selector:
- Use `[attribute='value']` for exact matches
- Use `[attribute*='value']` for partial matches
- Use `.class` for class names
- Use `#id` for IDs
- Combine multiple attributes for specificity

### 4. Update Code

Add the new selector to the appropriate file:
- Agreement page: `src/browser_manager.py`
- Facility page: `src/slot_detector.py`
- Time selection: `src/booking_handler.py`

### 5. Test

Run in headed mode and verify the selector works:
```bash
python main.py --test-mode --headed --log-level DEBUG
```

Check logs for:
```
DEBUG - Found ... with selector: your_new_selector
```

## Verification Checklist

Use this checklist when verifying selectors:

### Agreement Page
- [ ] Agreement checkbox found and checked
- [ ] "1か月後" button found and clicked
- [ ] Navigation to facility page successful

### Facility Selection Page
- [ ] Table structure matches expectations
- [ ] Date cells identified correctly
- [ ] Category labels found (普通車, 準中型車)
- [ ] AM/PM cells distinguished correctly
- [ ] Available slots detected (clickable links)
- [ ] Unavailable slots ignored (no links or disabled)

### Time Selection Page
- [ ] Radio buttons found
- [ ] First time selected correctly
- [ ] Reservation button found and clicked

## Common Issues

### Button Not Clicked

**Symptoms:**
- Log shows "Found button" but no click
- Navigation doesn't happen

**Causes:**
- Button might be disabled
- JavaScript might prevent click
- Need to wait for button to be enabled

**Solutions:**
- Add wait before click: `await asyncio.sleep(0.5)`
- Check if button is enabled: `await button.is_enabled()`
- Try JavaScript click: `await button.evaluate("el => el.click()")`

### Element Not Found

**Symptoms:**
- Log shows "Could not find..."
- Screenshot shows element is visible

**Causes:**
- Selector doesn't match
- Element in iframe
- Element not loaded yet

**Solutions:**
- Verify selector with DevTools
- Check for iframes: `await page.frame_locator("iframe")`
- Add wait: `await page.wait_for_selector(selector)`

### Wrong Element Selected

**Symptoms:**
- Wrong element clicked
- Unexpected behavior

**Causes:**
- Selector too generic
- Multiple matching elements

**Solutions:**
- Make selector more specific
- Add additional attributes
- Use `:first` or `:nth-child()` if needed

## Testing Selectors

### In Browser Console

```javascript
// Test if selector finds element
document.querySelector("input[type='button'][value='1か月後＞']")

// Test if multiple elements match
document.querySelectorAll("input[type='checkbox']").length

// Test text content
document.querySelector("input[type='button']").value
```

### In Playwright

```python
# Test selector
element = await page.query_selector("your_selector")
if element:
    print("Found!")
    print(await element.get_attribute("value"))
else:
    print("Not found")
```

## Notes

- **Full-width characters:** Japanese sites often use full-width characters (＞ vs >)
- **Exact matches:** Use exact value matches when possible
- **Fallbacks:** Always provide multiple selector options
- **Logging:** Log which selector worked for debugging
- **Screenshots:** Take screenshots on errors for debugging

## Last Updated

- **Date:** December 24, 2025
- **Button Selector:** Verified with actual HTML
- **Other Selectors:** Need verification with actual website

## Next Steps

1. Run system in headed mode
2. Inspect actual HTML for each page
3. Update this document with verified selectors
4. Test each selector works correctly
5. Update code with verified selectors
