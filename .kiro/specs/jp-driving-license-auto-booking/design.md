# Design Document

## Overview

The JP Driving License Auto-Booking System is a Python-based automation tool that monitors the Kanagawa e-Shinsei website for available driving test appointments and automatically books them. The system uses Playwright for browser automation, implements a polling mechanism with configurable refresh intervals, and sends Telegram notifications upon successful bookings.

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                     Main Controller                      │
│  (Orchestrates monitoring loop and booking flow)        │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┴────────┬──────────────┬──────────────┐
    │                 │              │              │
┌───▼────┐    ┌──────▼─────┐  ┌────▼─────┐  ┌────▼─────┐
│Browser │    │  Detector  │  │  Booker  │  │Notifier  │
│Manager │    │  (Slot     │  │ (Booking │  │(Telegram)│
│        │    │ Detection) │  │  Flow)   │  │          │
└────────┘    └────────────┘  └──────────┘  └──────────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                    │
            ┌───────▼────────┐
            │  Configuration │
            │   & Logging    │
            └────────────────┘
```

## Components and Interfaces

### 1. Configuration Manager

**Purpose:** Manages application configuration from environment variables and config files.

**Interface:**
```python
class Config:
    telegram_bot_token: str
    telegram_chat_id: str
    target_categories: List[str]  # e.g., ["普通車ＡＭ", "普通車ＰＭ"]
    refresh_interval: int  # seconds
    headless: bool
    test_mode: bool
    
    @classmethod
    def load() -> Config
    def validate() -> None
```

### 2. Browser Manager

**Purpose:** Manages Playwright browser lifecycle and page navigation.

**Interface:**
```python
class BrowserManager:
    def __init__(self, headless: bool)
    async def start() -> None
    async def stop() -> None
    async def navigate_to_facility_page() -> Page
    async def get_page() -> Page
```

### 3. Slot Detector

**Purpose:** Detects available time slots on the facility selection page.

**Interface:**
```python
class SlotDetector:
    def __init__(self, page: Page, target_categories: List[str])
    async def check_availability() -> Optional[AvailableSlot]
    async def _is_slot_clickable(element: ElementHandle) -> bool
    async def _extract_slot_info(element: ElementHandle) -> SlotInfo
```

**Data Models:**
```python
@dataclass
class SlotInfo:
    category: str  # e.g., "普通車ＡＭ"
    date: str
    element: ElementHandle

@dataclass
class AvailableSlot:
    slot_info: SlotInfo
    detected_at: datetime
```

### 4. Booking Handler

**Purpose:** Executes the booking flow once an available slot is detected.

**Interface:**
```python
class BookingHandler:
    def __init__(self, page: Page)
    async def complete_booking(slot: AvailableSlot) -> BookingResult
    async def _click_slot(element: ElementHandle) -> None
    async def _wait_for_time_selection_page() -> None
    async def _select_first_available_time() -> str
    async def _click_reservation_button() -> None
```

**Data Models:**
```python
@dataclass
class BookingResult:
    success: bool
    category: str
    date: str
    time: str
    error_message: Optional[str] = None
```

### 5. Telegram Notifier

**Purpose:** Sends notifications via Telegram Bot API.

**Interface:**
```python
class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str)
    async def send_booking_success(result: BookingResult) -> None
    async def send_error_notification(error: str) -> None
    def _format_message(result: BookingResult) -> str
```

### 6. Main Controller

**Purpose:** Orchestrates the monitoring loop and coordinates all components.

**Interface:**
```python
class BookingController:
    def __init__(self, config: Config)
    async def start() -> None
    async def _monitoring_loop() -> None
    async def _handle_available_slot(slot: AvailableSlot) -> None
    async def _handle_error(error: Exception) -> None
```

## Data Models

### Configuration Schema

```python
# .env file format
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
REFRESH_INTERVAL=5
HEADLESS=true
TEST_MODE=false
```

### Page Element Selectors

```python
SELECTORS = {
    "slot_containers": "selector_for_time_slot_containers",
    "slot_circle": "selector_for_circular_clickable_element",
    "time_options": "selector_for_time_selection_options",
    "reservation_button": "selector_for_reservation_button",
    "category_labels": {
        "普通車ＡＭ": "selector_for_regular_am",
        "普通車ＰＭ": "selector_for_regular_pm",
        "準中型車ＡＭ": "selector_for_semi_medium_am"
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After reviewing all identified properties, I've identified opportunities to consolidate:

- Properties 2.1, 2.2, 2.3 can be combined into a single property about detecting all configured categories
- Properties 4.2, 4.3, 4.4 can be combined into a single property about complete message content
- Properties 5.2 and 5.3 can be combined into a property about mode-specific category filtering
- Properties 7.2 and 7.3 can be combined into a property about browser mode configuration
- Properties 8.1 and 8.2 can be combined into a property about credential loading

This reduces redundancy while maintaining comprehensive coverage.

### Correctness Properties

Property 1: System initialization navigates to correct URL
*For any* valid configuration, starting the system should result in the browser navigating to https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_dateTrans?movePage=oneMonthLater
**Validates: Requirements 1.1**

Property 2: Refresh interval timing
*For any* monitoring cycle, the time between consecutive page refreshes should be 5 seconds (±0.5 seconds tolerance)
**Validates: Requirements 1.2**

Property 3: Page parsing completeness
*For any* valid facility selection page HTML, the parser should identify all slot elements present in the configured categories
**Validates: Requirements 1.3**

Property 4: Monitoring loop persistence
*For any* monitoring session, the system should continue the refresh loop until receiving an explicit stop signal
**Validates: Requirements 1.4**

Property 5: Network error retry behavior
*For any* network error during page load, the system should wait 5 seconds before retrying the request
**Validates: Requirements 1.5**

Property 6: Category detection completeness
*For any* configured target category (普通車ＡＭ, 普通車ＰＭ, 準中型車ＡＭ), when that category has clickable elements on the page, the detector should identify them
**Validates: Requirements 2.1, 2.2, 2.3**

Property 7: Detection latency bound
*For any* change in slot availability, the system should detect the change within one refresh cycle (5 seconds)
**Validates: Requirements 2.4**

Property 8: Slot availability classification
*For any* time slot element on the page, the system should correctly classify it as either available (clickable) or unavailable (non-clickable)
**Validates: Requirements 2.5**

Property 9: Availability triggers booking action
*For any* detected available slot, the system should initiate a click action on the corresponding circular element
**Validates: Requirements 3.1**

Property 10: Page load waiting
*For any* navigation to the time selection page, the system should wait for the page's ready state before attempting to interact with elements
**Validates: Requirements 3.2**

Property 11: First available time selection
*For any* time selection page with multiple available times, the system should select the first available option
**Validates: Requirements 3.3**

Property 12: Booking flow completion
*For any* selected time slot, the system should click the reservation button after selection
**Validates: Requirements 3.4**

Property 13: Booking flow performance
*For any* booking attempt, the entire flow from detection to reservation button click should complete within 10 seconds
**Validates: Requirements 3.5**

Property 14: Successful booking triggers notification
*For any* successfully completed reservation, the system should send a Telegram message
**Validates: Requirements 4.1**

Property 15: Notification message completeness
*For any* booking success notification, the Telegram message should contain the booking category, reservation date, and reservation time
**Validates: Requirements 4.2, 4.3, 4.4**

Property 16: Telegram failure resilience
*For any* Telegram API failure, the system should log the failure and continue monitoring without crashing
**Validates: Requirements 4.5**

Property 17: Configuration loading
*For any* valid configuration source (environment variables or config file), the system should correctly load and parse target booking categories
**Validates: Requirements 5.1**

Property 18: Mode-specific category filtering
*For any* system mode (test or production), the system should monitor only the categories specified for that mode
**Validates: Requirements 5.2, 5.3**

Property 19: Configuration validation on startup
*For any* system startup, configuration validation should occur before beginning the monitoring loop
**Validates: Requirements 5.4**

Property 20: Invalid configuration handling
*For any* invalid configuration, the system should display an error message and exit with a non-zero status code
**Validates: Requirements 5.5**

Property 21: Page load failure recovery
*For any* page load failure, the system should log the error and retry after 5 seconds
**Validates: Requirements 6.1**

Property 22: Missing element graceful handling
*For any* element not found error, the system should log the error and continue to the next refresh cycle without crashing
**Validates: Requirements 6.2**

Property 23: Booking failure recovery
*For any* booking process failure, the system should log the failure details and resume monitoring
**Validates: Requirements 6.3**

Property 24: Timestamped logging
*For any* operation or error, the system should create a log entry with a timestamp
**Validates: Requirements 6.4**

Property 25: Log rotation after 24 hours
*For any* system running continuously for more than 24 hours, log files should be rotated to prevent excessive disk usage
**Validates: Requirements 6.5**

Property 26: Browser mode configuration
*For any* configured browser mode (headless or headed), the system should launch the browser in the specified mode
**Validates: Requirements 7.2, 7.3**

Property 27: Browser cleanup on termination
*For any* system termination (normal or error), all browser instances should be properly closed
**Validates: Requirements 7.5**

Property 28: Credential loading from environment
*For any* system startup, Telegram bot token and chat ID should be loaded from environment variables or configuration file
**Validates: Requirements 8.1, 8.2**

Property 29: Missing credentials error messaging
*For any* missing required credential, the system should display a clear error message indicating which credential is missing
**Validates: Requirements 8.4**

Property 30: .env file support
*For any* .env file present in the project directory, the system should load configuration values from it
**Validates: Requirements 8.5**

## Error Handling

### Error Categories and Responses

1. **Network Errors**
   - Timeout during page load
   - Connection refused
   - DNS resolution failure
   - **Response:** Log error, wait 5 seconds, retry

2. **Page Parsing Errors**
   - Expected element not found
   - Unexpected page structure
   - **Response:** Log error, continue to next refresh cycle

3. **Booking Flow Errors**
   - Click action failed
   - Time selection failed
   - Reservation button not found
   - **Response:** Log detailed error, resume monitoring

4. **Telegram API Errors**
   - API timeout
   - Invalid token
   - Network failure
   - **Response:** Log error, continue operation (don't block booking)

5. **Configuration Errors**
   - Missing required credentials
   - Invalid category names
   - Invalid refresh interval
   - **Response:** Display error message, exit immediately

### Logging Strategy

```python
# Log levels and usage
logging.DEBUG    # Detailed flow information (element selectors, wait times)
logging.INFO     # Normal operations (refresh cycles, slot detection)
logging.WARNING  # Recoverable errors (network timeouts, missing elements)
logging.ERROR    # Serious errors (booking failures, Telegram failures)
logging.CRITICAL # Fatal errors (configuration errors, unrecoverable failures)
```

### Retry Logic

```python
# Exponential backoff for critical operations
MAX_RETRIES = 3
INITIAL_DELAY = 5  # seconds
BACKOFF_FACTOR = 2

async def retry_with_backoff(operation, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = INITIAL_DELAY * (BACKOFF_FACTOR ** attempt)
            await asyncio.sleep(delay)
```

## Testing Strategy

### Unit Testing

Unit tests will verify individual component behavior:

1. **Configuration Manager Tests**
   - Test loading from environment variables
   - Test loading from .env file
   - Test validation of required fields
   - Test handling of missing credentials

2. **Slot Detector Tests**
   - Test detection of available slots with mock HTML
   - Test classification of clickable vs non-clickable elements
   - Test extraction of slot information (category, date)
   - Test handling of malformed HTML

3. **Booking Handler Tests**
   - Test click sequence with mock page objects
   - Test time selection logic
   - Test error handling for missing elements

4. **Telegram Notifier Tests**
   - Test message formatting
   - Test API call construction
   - Test error handling for API failures

### Property-Based Testing

Property-based tests will use Hypothesis (Python) to verify correctness properties across many inputs:

1. **Configuration Property Tests**
   - Generate random valid configurations and verify loading
   - Generate random invalid configurations and verify error handling
   - Test that all valid category combinations are accepted

2. **Timing Property Tests**
   - Verify refresh interval consistency across multiple cycles
   - Verify booking flow completes within time bounds
   - Verify retry delays match expected values

3. **Detection Property Tests**
   - Generate random HTML with available/unavailable slots
   - Verify correct classification across all generated cases
   - Verify all configured categories are detected when present

4. **Error Recovery Property Tests**
   - Generate random error scenarios
   - Verify system continues operation after recoverable errors
   - Verify proper cleanup after fatal errors

### Integration Testing

Integration tests will verify end-to-end behavior:

1. **Mock Website Testing**
   - Create local mock server simulating the booking website
   - Test complete booking flow from detection to reservation
   - Test various availability scenarios

2. **Telegram Integration Testing**
   - Use Telegram Bot API test environment
   - Verify message delivery and formatting
   - Test error handling with simulated API failures

3. **Browser Automation Testing**
   - Test both headless and headed modes
   - Verify proper browser cleanup
   - Test handling of browser crashes

### Test Configuration

```python
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Property-based testing configuration
[hypothesis]
max_examples = 100
deadline = 5000  # 5 seconds per test
```

### Testing Approach

- **Test-Driven Development:** Write tests before implementation for core logic
- **Property-Based Testing:** Use Hypothesis to verify properties hold across many inputs
- **Mock External Dependencies:** Mock Playwright page objects and Telegram API
- **Integration Tests:** Use Docker to run mock website for end-to-end testing
- **Continuous Testing:** Run tests on every commit via CI/CD

## Deployment and Operations

### Environment Setup

```bash
# Required Python version
Python >= 3.9

# Dependencies
playwright>=1.40.0
python-telegram-bot>=20.0
python-dotenv>=1.0.0
aiohttp>=3.9.0

# Playwright browser installation
playwright install chromium
```

### Configuration Files

**.env file:**
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
TARGET_CATEGORIES=普通車ＡＭ,普通車ＰＭ
REFRESH_INTERVAL=5
HEADLESS=true
TEST_MODE=false
LOG_LEVEL=INFO
```

### Running the System

```bash
# Production mode
python main.py

# Test mode (monitors only 準中型車ＡＭ)
TEST_MODE=true TARGET_CATEGORIES=準中型車ＡＭ python main.py

# Debug mode (headed browser, verbose logging)
HEADLESS=false LOG_LEVEL=DEBUG python main.py
```

### Monitoring and Maintenance

1. **Log Monitoring**
   - Logs stored in `logs/` directory
   - Rotated daily or when exceeding 100MB
   - Monitor for ERROR and CRITICAL level messages

2. **Health Checks**
   - System should log "Monitoring active" every 60 seconds
   - Alert if no log activity for 5 minutes
   - Monitor disk space for log files

3. **Performance Metrics**
   - Track average refresh cycle time
   - Track booking flow completion time
   - Monitor memory usage over time

## Security Considerations

1. **Credential Management**
   - Never commit .env file to version control
   - Use environment variables in production
   - Rotate Telegram bot token periodically

2. **Rate Limiting**
   - Respect website's rate limits (5-second refresh is conservative)
   - Implement exponential backoff for errors
   - Add random jitter to avoid detection

3. **Browser Fingerprinting**
   - Use standard user agent
   - Don't modify browser fingerprint excessively
   - Consider rotating user agents if needed

4. **Data Privacy**
   - Don't log sensitive personal information
   - Sanitize URLs in logs (remove query parameters if needed)
   - Secure Telegram chat ID as sensitive data

## Future Enhancements

1. **Multi-User Support**
   - Support multiple Telegram users
   - Per-user configuration for target categories
   - Concurrent booking attempts

2. **Advanced Scheduling**
   - Preferred date/time ranges
   - Blacklist certain dates
   - Priority ordering of categories

3. **Web Dashboard**
   - Real-time monitoring status
   - Historical booking attempts
   - Configuration management UI

4. **Captcha Handling**
   - Integrate captcha solving service if needed
   - Manual captcha notification via Telegram
   - Fallback to manual intervention

5. **Multiple Location Support**
   - Support different prefectures
   - Configurable base URLs
   - Location-specific selectors
