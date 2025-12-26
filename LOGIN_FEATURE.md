# Login Feature Implementation

## Overview
Added automatic login functionality to the booking system. The system now logs in to e-kanagawa before starting the booking process.

## Changes Made

### 1. Updated `.env` Configuration
Added login credentials:
```bash
# Login Credentials
USER_EMAIL=niconicocsc@gmail.com
USER_PASSWORD=Cbf26266
```

### 2. Updated `src/config.py`
**Added Fields:**
- `user_email: str` - Email address for login
- `user_password: str` - Password for login

**Updated Validation:**
- Checks that `USER_EMAIL` is provided
- Checks that `USER_PASSWORD` is provided

### 3. Updated `src/browser_manager.py`
**Added Login URL:**
```python
LOGIN_URL = "https://dshinsei.e-kanagawa.lg.jp/140007-u/profile/userLogin"
```

**Updated Constructor:**
- Now accepts `user_email` and `user_password` parameters
- Stores credentials for login

**New Method: `login()`**
Performs automatic login:
1. Navigates to login page
2. Finds email input field (`input#userLoginForm.userId`)
3. Enters email address
4. Finds password input field (`input#userLoginForm.userPasswd`)
5. Enters password
6. Clicks login button (`input[type="submit"][value="ログイン"]`)
7. Waits for navigation
8. Verifies login success
9. Takes screenshot if login fails

### 4. Updated `src/booking_controller.py`
**Updated Initialization:**
- Passes email and password to BrowserManager

**Updated Start Flow:**
```python
1. Start browser
2. Login (NEW!)
3. Navigate to facility page
4. Start monitoring
```

## Login Flow

### Step 1: Navigate to Login Page
```
https://dshinsei.e-kanagawa.lg.jp/140007-u/profile/userLogin
```

### Step 2: Fill Login Form
**Email Field:**
- ID: `userLoginForm.userId`
- Name: `userId`
- Type: `text`
- Value: `niconicocsc@gmail.com`

**Password Field:**
- ID: `userLoginForm.userPasswd`
- Name: `userPasswd`
- Type: `password`
- Value: `Cbf26266`

### Step 3: Submit Form
**Login Button:**
- Type: `submit`
- Value: `ログイン`
- Action: `../profile/userLogin_login`

### Step 4: Verify Success
- Waits for page load
- Checks if still on login page (indicates failure)
- Looks for error messages
- Confirms successful login

## HTML Structure

### Login Form
```html
<dl class="c-input">
  <dt class="c-input__title">
    <label for="userLoginForm.userId">利用者ID（メールアドレス）</label>
  </dt>
  <dd class="c-input__item">
    <input id="userLoginForm.userId" 
           name="userId" 
           class="input-470" 
           type="text" 
           value="" 
           size="48" 
           maxlength="256">
  </dd>
</dl>

<dl class="c-input">
  <dt class="c-input__title">
    <label for="userLoginForm.userPasswd">パスワード</label>
  </dt>
  <dd class="c-input__item">
    <input id="userLoginForm.userPasswd" 
           name="userPasswd" 
           class="input-470" 
           type="password" 
           value="" 
           size="50" 
           maxlength="50">
  </dd>
</dl>

<div class="c-btn--submit_2 c-label--submit_2">
  <input type="submit" 
         class="c-btn_2 button-outline" 
         onclick="formSubmit(this.form, '../profile/userLogin_login');return false;" 
         value="ログイン">
</div>
```

## Complete Booking Flow (Updated)

### 1. Login ✅ (NEW!)
- Navigate to login page
- Enter email and password
- Click login button
- Verify success

### 2. Navigate to Facility Page ✅
- Go to initial page
- Click "1か月後" button
- Arrive at facility selection page

### 3. Monitor for Slots ✅
- Check consent checkbox
- Look for available slots
- Refresh every 5 seconds

### 4. Book Slot ✅
- Click available slot
- Select time
- Click "予約する"
- Click "同意する"

### 5. Complete Form ✅
- Browser stays open
- User fills remaining fields
- User submits form

## Expected Console Output

```
INFO - Starting JP Driving License Auto-Booking System
INFO - Target categories: ['準中型車ＡＭ']
INFO - Starting browser (headless=False)
INFO - Navigating to login page: https://dshinsei.e-kanagawa.lg.jp/140007-u/profile/userLogin
DEBUG - Looking for email input field
DEBUG - Entering email: niconicocsc@gmail.com
DEBUG - Looking for password input field
DEBUG - Entering password
DEBUG - Looking for login button
INFO - Clicking login button
INFO - ✓ Login successful
INFO - Navigating to initial page: https://...
INFO - Clicked '1か月後' button
INFO - Successfully navigated to facility selection page
INFO - Starting monitoring loop
...
```

## Error Handling

### Login Fails
- Takes screenshot: `logs/login_error.png`
- Logs error message
- Raises exception
- System stops

### Invalid Credentials
- Error message displayed
- Screenshot saved
- User notified

### Network Issues
- Timeout after 10 seconds
- Error logged
- Screenshot saved

## Security Notes

### Credentials Storage
- Stored in `.env` file
- Not committed to git (in `.gitignore`)
- Only loaded at runtime

### Password Handling
- Entered directly into password field
- Not logged in console
- Not visible in screenshots

### Session Management
- Login session maintained throughout booking
- No need to re-login
- Session expires after booking complete

## Testing

### Test Login
```bash
python main.py
```

### Expected Behavior
1. Browser opens
2. Navigates to login page
3. Fills email and password
4. Clicks login button
5. Successfully logs in
6. Continues to booking flow

### Verify Success
- Console shows: "✓ Login successful"
- Browser navigates away from login page
- No error messages
- Booking flow continues

## Troubleshooting

### "Could not find email input field"
- Check if page structure changed
- Verify selector: `input#userLoginForm.userId`
- Check browser screenshot

### "Could not find password input field"
- Check if page structure changed
- Verify selector: `input#userLoginForm.userPasswd`
- Check browser screenshot

### "Login failed: Still on login page"
- Check credentials in `.env`
- Verify email and password are correct
- Check for error messages on page

### "Login failed: [error message]"
- Read error message for details
- Common issues:
  - Invalid email/password
  - Account locked
  - Network issues

## Configuration

### Required in `.env`
```bash
USER_EMAIL=your_email@example.com
USER_PASSWORD=your_password
```

### Validation
- System checks both fields are provided
- Exits with error if missing
- Shows clear error message

## Files Modified

1. `.env` - Added login credentials
2. `src/config.py` - Added email/password fields
3. `src/browser_manager.py` - Added login method
4. `src/booking_controller.py` - Added login step

---

**Date:** December 24, 2025
**Status:** ✅ Complete and ready for testing
**Security:** Credentials stored securely in .env file
