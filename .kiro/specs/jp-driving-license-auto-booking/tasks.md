# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create Python project with proper directory structure (src/, tests/, logs/)
  - Set up pyproject.toml or requirements.txt with Playwright, python-telegram-bot, python-dotenv, aiohttp, pytest, hypothesis
  - Initialize git repository with .gitignore for .env, logs/, __pycache__
  - Install Playwright browsers (chromium)
  - _Requirements: 7.1, 7.5_

- [ ]* 1.1 Write property test for project structure
  - **Property 1: System initialization navigates to correct URL**
  - **Validates: Requirements 1.1**

- [x] 2. Implement Configuration Manager
  - Create Config dataclass with all required fields (telegram_bot_token, telegram_chat_id, target_categories, refresh_interval, headless, test_mode)
  - Implement Config.load() to read from environment variables and .env file
  - Implement Config.validate() to check required fields and valid values
  - Add error messages for missing or invalid configuration
  - _Requirements: 5.1, 5.4, 5.5, 8.1, 8.2, 8.4, 8.5_

- [ ]* 2.1 Write property test for configuration loading
  - **Property 17: Configuration loading**
  - **Validates: Requirements 5.1**

- [ ]* 2.2 Write property test for configuration validation
  - **Property 19: Configuration validation on startup**
  - **Validates: Requirements 5.4**

- [ ]* 2.3 Write property test for invalid configuration handling
  - **Property 20: Invalid configuration handling**
  - **Validates: Requirements 5.5**

- [ ]* 2.4 Write property test for credential loading
  - **Property 28: Credential loading from environment**
  - **Validates: Requirements 8.1, 8.2**

- [ ]* 2.5 Write property test for missing credentials error
  - **Property 29: Missing credentials error messaging**
  - **Validates: Requirements 8.4**

- [ ]* 2.6 Write property test for .env file support
  - **Property 30: .env file support**
  - **Validates: Requirements 8.5**

- [x] 3. Implement logging system
  - Set up Python logging with rotating file handler
  - Configure log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Implement timestamped log entries
  - Implement log rotation after 24 hours or 100MB
  - _Requirements: 6.4, 6.5_

- [ ]* 3.1 Write property test for timestamped logging
  - **Property 24: Timestamped logging**
  - **Validates: Requirements 6.4**

- [ ]* 3.2 Write property test for log rotation
  - **Property 25: Log rotation after 24 hours**
  - **Validates: Requirements 6.5**

- [x] 4. Implement Browser Manager
  - Create BrowserManager class with async start() and stop() methods
  - Implement Playwright browser initialization with headless/headed mode support
  - Implement navigate_to_facility_page() to load the target URL
  - Implement proper browser cleanup in stop() method
  - Add context manager support for automatic cleanup
  - _Requirements: 1.1, 7.2, 7.3, 7.5_

- [ ]* 4.1 Write property test for browser mode configuration
  - **Property 26: Browser mode configuration**
  - **Validates: Requirements 7.2, 7.3**

- [ ]* 4.2 Write property test for browser cleanup
  - **Property 27: Browser cleanup on termination**
  - **Validates: Requirements 7.5**

- [x] 5. Implement Slot Detector
  - Create SlotInfo and AvailableSlot dataclasses
  - Implement SlotDetector class with check_availability() method
  - Implement _is_slot_clickable() to determine if element is clickable
  - Implement _extract_slot_info() to get category and date from element
  - Add support for all three categories (普通車ＡＭ, 普通車ＰＭ, 準中型車ＡＭ)
  - _Requirements: 1.3, 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ]* 5.1 Write property test for category detection
  - **Property 6: Category detection completeness**
  - **Validates: Requirements 2.1, 2.2, 2.3**

- [ ]* 5.2 Write property test for slot classification
  - **Property 8: Slot availability classification**
  - **Validates: Requirements 2.5**

- [ ]* 5.3 Write property test for page parsing
  - **Property 3: Page parsing completeness**
  - **Validates: Requirements 1.3**

- [x] 6. Implement Booking Handler
  - Create BookingResult dataclass
  - Implement BookingHandler class with complete_booking() method
  - Implement _click_slot() to click on circular element
  - Implement _wait_for_time_selection_page() to wait for page load
  - Implement _select_first_available_time() to choose first time slot
  - Implement _click_reservation_button() to complete booking
  - Add timing tracking to ensure completion within 10 seconds
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 6.1 Write property test for booking action trigger
  - **Property 9: Availability triggers booking action**
  - **Validates: Requirements 3.1**

- [ ]* 6.2 Write property test for page load waiting
  - **Property 10: Page load waiting**
  - **Validates: Requirements 3.2**

- [ ]* 6.3 Write property test for time selection
  - **Property 11: First available time selection**
  - **Validates: Requirements 3.3**

- [ ]* 6.4 Write property test for booking flow completion
  - **Property 12: Booking flow completion**
  - **Validates: Requirements 3.4**

- [ ]* 6.5 Write property test for booking performance
  - **Property 13: Booking flow performance**
  - **Validates: Requirements 3.5**

- [x] 7. Implement Telegram Notifier
  - Create TelegramNotifier class with send_booking_success() method
  - Implement _format_message() to create notification text with category, date, time
  - Implement send_error_notification() for error alerts
  - Add error handling for Telegram API failures (log and continue)
  - Use python-telegram-bot library for API calls
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 7.1 Write property test for notification trigger
  - **Property 14: Successful booking triggers notification**
  - **Validates: Requirements 4.1**

- [ ]* 7.2 Write property test for message completeness
  - **Property 15: Notification message completeness**
  - **Validates: Requirements 4.2, 4.3, 4.4**

- [ ]* 7.3 Write property test for Telegram failure resilience
  - **Property 16: Telegram failure resilience**
  - **Validates: Requirements 4.5**

- [x] 8. Implement error handling and retry logic
  - Implement retry_with_backoff() function with exponential backoff
  - Add network error handling with 5-second retry delay
  - Add page parsing error handling (log and continue)
  - Add booking flow error handling (log and resume monitoring)
  - Ensure all errors are logged with appropriate levels
  - _Requirements: 1.5, 6.1, 6.2, 6.3_

- [ ]* 8.1 Write property test for network error retry
  - **Property 5: Network error retry behavior**
  - **Validates: Requirements 1.5**

- [ ]* 8.2 Write property test for page load failure recovery
  - **Property 21: Page load failure recovery**
  - **Validates: Requirements 6.1**

- [ ]* 8.3 Write property test for missing element handling
  - **Property 22: Missing element graceful handling**
  - **Validates: Requirements 6.2**

- [ ]* 8.4 Write property test for booking failure recovery
  - **Property 23: Booking failure recovery**
  - **Validates: Requirements 6.3**

- [x] 9. Implement Main Controller
  - Create BookingController class with start() method
  - Implement _monitoring_loop() with 5-second refresh interval
  - Implement _handle_available_slot() to trigger booking flow
  - Implement _handle_error() for error logging and recovery
  - Add mode-specific category filtering (test mode vs production mode)
  - Add graceful shutdown handling (SIGINT, SIGTERM)
  - _Requirements: 1.2, 1.4, 2.4, 5.2, 5.3_

- [ ]* 9.1 Write property test for refresh interval timing
  - **Property 2: Refresh interval timing**
  - **Validates: Requirements 1.2**

- [ ]* 9.2 Write property test for monitoring persistence
  - **Property 4: Monitoring loop persistence**
  - **Validates: Requirements 1.4**

- [ ]* 9.3 Write property test for detection latency
  - **Property 7: Detection latency bound**
  - **Validates: Requirements 2.4**

- [ ]* 9.4 Write property test for mode-specific filtering
  - **Property 18: Mode-specific category filtering**
  - **Validates: Requirements 5.2, 5.3**

- [x] 10. Create main entry point
  - Create main.py with async main() function
  - Load configuration and validate
  - Initialize all components (BrowserManager, SlotDetector, BookingHandler, TelegramNotifier, BookingController)
  - Start monitoring loop
  - Handle keyboard interrupt for graceful shutdown
  - Add command-line argument support for overriding config
  - _Requirements: All_

- [x] 11. Add page element selectors
  - Inspect the actual website to identify correct CSS selectors
  - Create SELECTORS dictionary with all required selectors
  - Test selectors against live website
  - Document selector structure in code comments
  - _Requirements: 1.3, 2.1, 2.2, 2.3, 3.1, 3.3, 3.4_

- [x] 12. Create example configuration files
  - Create .env.example with placeholder values
  - Create README.md with setup instructions
  - Document how to get Telegram bot token and chat ID
  - Add usage examples for test mode and production mode
  - Document troubleshooting common issues
  - _Requirements: 8.1, 8.2, 8.5_

- [x] 13. Checkpoint - Ensure all tests pass
  - Run all unit tests and verify they pass
  - Run all property-based tests and verify they pass
  - Fix any failing tests
  - Ask the user if questions arise

- [x] 14. Integration testing with mock website
  - Create simple Flask/FastAPI mock server simulating booking website
  - Test complete flow from detection to booking with mock
  - Test error scenarios (network failures, missing elements)
  - Verify Telegram notifications are sent correctly
  - _Requirements: All_

- [x] 15. Manual testing with real website (test mode)
  - Configure for test mode (準中型車ＡＭ only)
  - Run script against real website in headed mode
  - Verify detection works correctly
  - Verify booking flow completes successfully
  - Verify Telegram notification is received
  - _Requirements: All_

- [x] 16. Add deployment documentation
  - Document how to run as background process (nohup, systemd)
  - Document how to monitor logs
  - Document how to stop the script gracefully
  - Add example systemd service file
  - Document resource requirements (CPU, memory, disk)
  - _Requirements: 6.4, 6.5_

- [x] 17. Final checkpoint - Production readiness
  - Verify all tests pass
  - Verify configuration validation works
  - Verify error handling and recovery works
  - Verify logging and log rotation works
  - Verify Telegram notifications work
  - Ask the user if questions arise
