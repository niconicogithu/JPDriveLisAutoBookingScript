# Production Readiness Checklist

Use this checklist before deploying the system to production.

## ✅ Configuration

- [ ] `.env` file created from `.env.example`
- [ ] `TELEGRAM_BOT_TOKEN` set with valid token
- [ ] `TELEGRAM_CHAT_ID` set with valid chat ID
- [ ] `TARGET_CATEGORIES` configured correctly
  - Test mode: `準中型車ＡＭ`
  - Production: `普通車ＡＭ,普通車ＰＭ`
- [ ] `REFRESH_INTERVAL` set (recommended: 5 seconds)
- [ ] `HEADLESS` set to `true` for production
- [ ] `TEST_MODE` set appropriately
- [ ] `LOG_LEVEL` set (recommended: INFO for production)

## ✅ Dependencies

- [ ] Python 3.9+ installed
- [ ] All packages installed: `pip install -r requirements.txt`
- [ ] Playwright browsers installed: `playwright install chromium`
- [ ] System dependencies installed (for Linux servers)

## ✅ Testing

- [ ] Configuration validation passes
- [ ] System starts without errors
- [ ] Browser navigates to correct URL
- [ ] Page structure matches selectors
- [ ] Slot detection works (tested in headed mode)
- [ ] Booking flow completes successfully (if slots available)
- [ ] Telegram notifications received
- [ ] Error handling works (network errors, missing elements)
- [ ] Graceful shutdown works (Ctrl+C)

## ✅ Selectors Verification

- [ ] Inspected actual website HTML structure
- [ ] Updated `src/slot_detector.py` selectors if needed
- [ ] Updated `src/booking_handler.py` selectors if needed
- [ ] Tested selectors with real website
- [ ] Documented any selector changes

## ✅ Logging

- [ ] Logs directory created
- [ ] Log rotation configured (100MB, 7 backups)
- [ ] Logs contain timestamps
- [ ] Log levels appropriate for production
- [ ] Can monitor logs: `tail -f logs/booking_system.log`

## ✅ Security

- [ ] `.env` file not committed to version control
- [ ] `.gitignore` includes `.env`, `logs/`, `__pycache__/`
- [ ] File permissions set correctly (`chmod 600 .env`)
- [ ] Credentials stored securely
- [ ] No sensitive data in logs

## ✅ Deployment

- [ ] Deployment method chosen (nohup, systemd, screen, tmux)
- [ ] Service file configured (if using systemd)
- [ ] Service starts automatically on boot (if desired)
- [ ] Can start/stop service reliably
- [ ] Can monitor service status

## ✅ Monitoring

- [ ] Can view real-time logs
- [ ] Can search logs for errors
- [ ] Health check script created (optional)
- [ ] Monitoring alerts configured (optional)
- [ ] Disk space monitoring in place

## ✅ Backup

- [ ] `.env` file backed up securely
- [ ] Backup strategy for logs (optional)
- [ ] Recovery procedure documented

## ✅ Documentation

- [ ] README.md reviewed
- [ ] TESTING.md reviewed
- [ ] DEPLOYMENT.md reviewed
- [ ] Team members trained (if applicable)

## ✅ Final Verification

Run through this final test:

1. **Start the system:**
   ```bash
   python3 main.py --test-mode --headed --log-level DEBUG
   ```

2. **Verify startup:**
   - [ ] No configuration errors
   - [ ] Browser opens
   - [ ] Navigates to correct URL
   - [ ] Logs show "Monitoring active"

3. **Verify monitoring:**
   - [ ] Page refreshes every 5 seconds
   - [ ] Slot detection runs
   - [ ] Logs show detection attempts

4. **Verify error handling:**
   - [ ] Disconnect network briefly
   - [ ] System logs error and retries
   - [ ] System resumes after reconnection

5. **Verify shutdown:**
   - [ ] Press Ctrl+C
   - [ ] Browser closes cleanly
   - [ ] Logs show "Shutdown complete"

6. **Production test:**
   ```bash
   python3 main.py --headless
   ```
   - [ ] Runs in background
   - [ ] Logs being written
   - [ ] Can monitor with `tail -f logs/booking_system.log`

## 🚀 Ready for Production

Once all items are checked:

1. Update `.env` for production:
   ```bash
   TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
   HEADLESS=true
   TEST_MODE=false
   LOG_LEVEL=INFO
   ```

2. Deploy using chosen method:
   ```bash
   # Option 1: nohup
   nohup python3 main.py --headless > output.log 2>&1 &
   
   # Option 2: systemd
   sudo systemctl start booking-system
   
   # Option 3: screen
   screen -S booking
   python3 main.py --headless
   # Ctrl+A, D to detach
   ```

3. Monitor for first hour:
   ```bash
   tail -f logs/booking_system.log
   ```

4. Verify Telegram notifications work

5. Set up monitoring alerts (optional)

## 📝 Notes

- Document any issues encountered
- Document any selector changes made
- Keep this checklist updated
- Share learnings with team

## ⚠️ Important Reminders

- Test mode uses `準中型車ＡＭ` only
- Production mode uses `普通車ＡＭ,普通車ＰＭ`
- System will stop after successful booking
- Monitor logs regularly for errors
- Website structure may change - update selectors as needed
- Respect website rate limits (5-second refresh is conservative)

## 🆘 Emergency Contacts

- Telegram Bot: @BotFather
- Website: https://dshinsei.e-kanagawa.lg.jp
- Support: [Add your support contact]

---

**Last Updated:** [Date]
**Reviewed By:** [Name]
**Production Deployment Date:** [Date]
