# Quick Test Guide

## 🚀 Start Testing

```bash
python main.py
```

## 👀 What You Should See

### 1. Browser Opens
- Window appears
- Navigates to booking site

### 2. Auto-Navigation
- Clicks "1か月後" button
- Goes to facility selection page

### 3. Consent Checkbox
- ✅ Automatically checked
- "上記内容に同意する"

### 4. Monitoring
- Checks every 5 seconds
- Logs: "Check #N: Looking for available slots..."

### 5. Slot Found! 🎯
- Logs: "✓ Found available slot: 準中型車ＡＭ on XX/XX"
- Automatically clicks the slot

### 6. Time Selection
- Selects first available time
- Clicks "予約する"

### 7. Procedure Page
- Clicks "同意する"
- Locks reservation

### 8. Success! 🎉
```
============================================================
🎉 RESERVATION LOCKED SUCCESSFULLY!
============================================================
⚠️  IMPORTANT: Browser will remain open
📝 Please complete the remaining form fields manually
============================================================
Press Ctrl+C when you're done to close the browser
```

### 9. Telegram Notification 📱
- Check your phone
- Should receive notification with details

### 10. Complete Form
- Fill remaining fields in browser
- Submit the form

### 11. Close
- Press `Ctrl+C` in terminal
- Browser closes

## ⚠️ Important

- **Don't close browser manually** - Wait for form completion
- **Check Telegram** - Notification confirms success
- **Fill form quickly** - Reservation may expire
- **Press Ctrl+C** - Only after form is submitted

## 🐛 If Something Goes Wrong

### No slots found
- Normal! System keeps checking
- Wait for slots to appear

### Error messages
- Check logs in console
- Screenshot saved to `logs/`
- System usually continues anyway

### Browser closes too early
- Shouldn't happen anymore
- Report if it does

## ✅ Success Indicators

1. ✓ Consent checkbox checked
2. ✓ Slot detected and clicked
3. ✓ Time selected
4. ✓ "予約する" clicked
5. ✓ "同意する" clicked
6. ✓ Telegram notification received
7. ✓ Browser stays open
8. ✓ Form ready to complete

## 📊 Expected Timeline

- **0-30s:** Browser starts and navigates
- **0-5min:** Finds available slot (depends on availability)
- **3-5s:** Completes booking flow
- **Instant:** Telegram notification
- **User time:** Complete form manually
- **Instant:** Ctrl+C to close

---

**Ready? Run:** `python main.py` 🚀
