# Login Test Guide

## 🔐 Login Feature Added!

The system now automatically logs in before starting the booking process.

## Configuration

### Check `.env` File
Make sure these are set:
```bash
USER_EMAIL=niconicocsc@gmail.com
USER_PASSWORD=Cbf26266
```

## Test the Login

### Start the System
```bash
python main.py
```

## What You'll See

### 1. Browser Starts
```
INFO - Starting browser (headless=False)
```

### 2. Navigate to Login Page
```
INFO - Navigating to login page: https://dshinsei.e-kanagawa.lg.jp/140007-u/profile/userLogin
```

### 3. Fill Login Form
```
DEBUG - Looking for email input field
DEBUG - Entering email: niconicocsc@gmail.com
DEBUG - Looking for password input field
DEBUG - Entering password
```

### 4. Click Login Button
```
DEBUG - Looking for login button
INFO - Clicking login button
```

### 5. Login Success! ✅
```
INFO - ✓ Login successful
```

### 6. Continue to Booking
```
INFO - Navigating to initial page: https://...
INFO - Clicked '1か月後' button
INFO - Successfully navigated to facility selection page
INFO - Starting monitoring loop
```

## Visual Verification

### In Browser Window
1. **Login page appears** - Shows email and password fields
2. **Fields auto-fill** - Email and password entered automatically
3. **Login button clicks** - Form submits
4. **Page changes** - Navigates away from login page
5. **User logged in** - Should see user name in header

## Success Indicators

✅ Console shows: "✓ Login successful"
✅ Browser navigates away from login page
✅ No error messages
✅ Booking flow continues normally

## If Login Fails

### Check Console
Look for error messages:
```
ERROR - Error during login: [error message]
INFO - Screenshot saved to logs/login_error.png
```

### Check Screenshot
Open `logs/login_error.png` to see what went wrong

### Common Issues

**"Could not find email input field"**
- Page structure may have changed
- Check if login page loaded correctly

**"Could not find password input field"**
- Page structure may have changed
- Check if login page loaded correctly

**"Login failed: Still on login page"**
- Invalid credentials
- Check email and password in `.env`
- Verify account is active

**"Login failed: [error message]"**
- Read the error message
- Common causes:
  - Wrong email/password
  - Account locked
  - Network issues

## Troubleshooting

### Verify Credentials
1. Open `.env` file
2. Check `USER_EMAIL=niconicocsc@gmail.com`
3. Check `USER_PASSWORD=Cbf26266`
4. No extra spaces or quotes

### Test Manually
1. Open browser
2. Go to: https://dshinsei.e-kanagawa.lg.jp/140007-u/profile/userLogin
3. Enter email: niconicocsc@gmail.com
4. Enter password: Cbf26266
5. Click login
6. Verify it works

### Check Logs
```bash
tail -f logs/booking_system.log
```

## Complete Flow

```
1. Start System
   ↓
2. Open Browser
   ↓
3. Navigate to Login Page
   ↓
4. Fill Email & Password
   ↓
5. Click Login Button
   ↓
6. ✓ Login Successful
   ↓
7. Navigate to Booking Page
   ↓
8. Start Monitoring
   ↓
9. Find Available Slot
   ↓
10. Complete Booking
```

## Security Notes

- Credentials stored in `.env` (not in git)
- Password not shown in console
- Session maintained throughout booking
- No need to re-login

## Ready to Test!

Run the system and watch for:
1. Login page loads
2. Form auto-fills
3. Login succeeds
4. Booking flow starts

**Command:** `python main.py`

---

**Expected Time:** Login takes 3-5 seconds
**Success Rate:** Should work every time with correct credentials
**Next Step:** After login, system proceeds to booking automatically
