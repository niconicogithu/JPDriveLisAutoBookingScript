# Requirements Document

## Introduction

This system automates the process of booking driving license test appointments on the Kanagawa e-Shinsei website (https://dshinsei.e-kanagawa.lg.jp). The system continuously monitors available time slots and automatically reserves them when they become available, with Telegram notifications for successful bookings.

## Glossary

- **System**: The automated booking script
- **Target Website**: The Kanagawa e-Shinsei driving license reservation website
- **Time Slot**: A specific date and time period (AM/PM) available for driving test appointments
- **Booking Categories**: 普通車ＡＭ (Regular Car AM), 普通車ＰＭ (Regular Car PM), 準中型車ＡＭ (Semi-medium Car AM)
- **User**: The person running the automated booking script
- **Telegram Bot**: The notification service that alerts the User of successful bookings

## Requirements

### Requirement 1

**User Story:** As a user, I want the system to continuously monitor the reservation website, so that I don't miss any available time slots.

#### Acceptance Criteria

1. WHEN the system starts, THE System SHALL load the initial agreement page at https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/offerList_detail?tempSeq=50909&accessFrom=offerList
2. WHEN the agreement page loads, THE System SHALL check the agreement checkbox (上記内容に同意する)
3. WHEN the checkbox is checked, THE System SHALL click the "1か月後" button
4. WHEN the button is clicked, THE System SHALL navigate to the facility selection page at https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_dateTrans?movePage=oneMonthLater
5. THE System SHALL refresh the facility selection page every 5 seconds to check for new availability
6. WHEN a refresh occurs, THE System SHALL parse the page content to identify available time slots
7. THE System SHALL continue monitoring until manually stopped by the User
8. WHEN the system encounters a network error, THE System SHALL retry the request after 5 seconds

### Requirement 2

**User Story:** As a user, I want the system to detect when specific booking categories become available, so that it can automatically reserve them.

#### Acceptance Criteria

1. WHEN the system checks the page, THE System SHALL identify clickable elements for 普通車ＡＭ (Regular Car AM)
2. WHEN the system checks the page, THE System SHALL identify clickable elements for 普通車ＰＭ (Regular Car PM)
3. WHEN the system checks the page, THE System SHALL identify clickable elements for 準中型車ＡＭ (Semi-medium Car AM)
4. WHEN a target booking category becomes clickable, THE System SHALL detect it within one refresh cycle
5. THE System SHALL distinguish between available (clickable) and unavailable (non-clickable) time slots

### Requirement 3

**User Story:** As a user, I want the system to automatically click on available time slots and proceed through the booking process, so that I can secure a reservation quickly.

#### Acceptance Criteria

1. WHEN an available time slot is detected, THE System SHALL click on the corresponding circular element
2. WHEN the time selection page loads at https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_decide, THE System SHALL wait for the page to fully load
3. WHEN the time selection page is loaded, THE System SHALL select the first available time slot
4. WHEN a time slot is selected, THE System SHALL click the reservation button (予約) at the bottom of the page
5. THE System SHALL complete the entire booking flow within 10 seconds of detecting availability

### Requirement 4

**User Story:** As a user, I want to receive Telegram notifications when a reservation is successfully made, so that I'm immediately aware of the booking.

#### Acceptance Criteria

1. WHEN a reservation is successfully completed, THE System SHALL send a Telegram message to the User
2. THE Telegram message SHALL include the booking category (e.g., 普通車ＡＭ)
3. THE Telegram message SHALL include the reservation date
4. THE Telegram message SHALL include the reservation time
5. WHEN the Telegram API is unavailable, THE System SHALL log the notification failure and continue operation

### Requirement 5

**User Story:** As a user, I want to configure which booking categories to monitor, so that I can test the system or target specific time slots.

#### Acceptance Criteria

1. THE System SHALL support a configuration file or command-line arguments for specifying target booking categories
2. WHEN testing, THE System SHALL allow monitoring only 準中型車ＡＭ (Semi-medium Car AM)
3. WHEN in production mode, THE System SHALL monitor both 普通車ＡＭ and 普通車ＰＭ
4. THE System SHALL validate the configuration on startup
5. WHEN invalid configuration is provided, THE System SHALL display an error message and exit

### Requirement 6

**User Story:** As a user, I want the system to handle errors gracefully, so that it continues running even when issues occur.

#### Acceptance Criteria

1. WHEN a page load fails, THE System SHALL log the error and retry after 5 seconds
2. WHEN an element is not found on the page, THE System SHALL log the error and continue to the next refresh cycle
3. WHEN the booking process fails, THE System SHALL log the failure details and resume monitoring
4. THE System SHALL maintain a log file with timestamps for all operations and errors
5. WHEN the system runs for more than 24 hours, THE System SHALL rotate log files to prevent excessive disk usage

### Requirement 7

**User Story:** As a developer, I want the system to use a headless browser automation tool, so that it can interact with the dynamic JavaScript-based website.

#### Acceptance Criteria

1. THE System SHALL use Playwright or Selenium for browser automation
2. THE System SHALL support running in headless mode for production use
3. THE System SHALL support running in headed mode for debugging and testing
4. WHEN running in test mode, THE System SHALL allow visual inspection of the automation process
5. THE System SHALL properly close browser instances when the script terminates

### Requirement 8

**User Story:** As a user, I want to configure my Telegram bot credentials securely, so that my API keys are not exposed in the code.

#### Acceptance Criteria

1. THE System SHALL read Telegram bot token from an environment variable or configuration file
2. THE System SHALL read Telegram chat ID from an environment variable or configuration file
3. THE System SHALL not include credentials in the source code
4. WHEN credentials are missing, THE System SHALL display a clear error message
5. THE System SHALL support a .env file for local development configuration
