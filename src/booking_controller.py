"""Main controller for the booking system."""
import asyncio
import signal
from typing import Optional
from src.config import Config
from src.browser_manager import BrowserManager
from src.slot_detector import SlotDetector, AvailableSlot
from src.booking_handler import BookingHandler
from src.telegram_notifier import TelegramNotifier
from src.error_handler import handle_network_error, handle_page_parsing_error, handle_booking_error
from src.logger import get_logger


class BookingController:
    """Orchestrates the monitoring loop and booking flow."""
    
    def __init__(self, config: Config):
        """
        Initialize booking controller.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = get_logger()
        self.running = False
        self.browser_manager: Optional[BrowserManager] = None
        self.slot_detector: Optional[SlotDetector] = None
        self.booking_handler: Optional[BookingHandler] = None
        self.telegram_notifier: Optional[TelegramNotifier] = None
    
    async def start(self) -> None:
        """Start the booking system."""
        self.logger.info("Starting JP Driving License Auto-Booking System")
        self.logger.info(f"Target categories: {self.config.target_categories}")
        self.logger.info(f"Test mode: {self.config.test_mode}")
        self.logger.info(f"Refresh interval: {self.config.refresh_interval} seconds")
        
        # Set up signal handlers for graceful shutdown
        self._setup_signal_handlers()
        
        # Initialize components
        self.browser_manager = BrowserManager(
            headless=self.config.headless,
            user_email=self.config.user_email,
            user_password=self.config.user_password
        )
        self.telegram_notifier = TelegramNotifier(
            bot_token=self.config.telegram_bot_token,
            chat_id=self.config.telegram_chat_id
        )
        
        try:
            # Start browser
            await self.browser_manager.start()
            
            # Login first
            await self.browser_manager.login()
            
            # Navigate to facility page
            page = await self.browser_manager.navigate_to_facility_page()
            
            # Initialize detector and handler
            self.slot_detector = SlotDetector(page, self.config.target_categories)
            self.booking_handler = BookingHandler(page)
            
            # Start monitoring loop
            self.running = True
            await self._monitoring_loop()
        
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt")
        except Exception as e:
            self.logger.critical(f"Fatal error: {e}", exc_info=True)
            raise
        finally:
            await self._cleanup()
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop that checks for available slots."""
        self.logger.info("Starting monitoring loop")
        self.logger.info(f"Will check for slots every {self.config.refresh_interval} seconds")
        
        refresh_count = 0
        last_status_log = 0
        
        while self.running:
            try:
                refresh_count += 1
                
                # Log periodic status (every 60 seconds)
                if refresh_count - last_status_log >= (60 // self.config.refresh_interval):
                    self.logger.info(f"Monitoring active - checked {refresh_count} times")
                    last_status_log = refresh_count
                
                # Check for available slots
                self.logger.debug(f"Check #{refresh_count}: Looking for available slots...")
                available_slot = await self.slot_detector.check_availability()
                
                if available_slot:
                    await self._handle_available_slot(available_slot)
                    # If booking was successful, loop will stop (self.running = False)
                    # If booking failed, continue monitoring
                else:
                    self.logger.debug(f"Check #{refresh_count}: No slots available")
                
                # Wait for refresh interval before next check
                await asyncio.sleep(self.config.refresh_interval)
                
                # Refresh the page to get latest data
                self.logger.debug(f"Refreshing page for check #{refresh_count + 1}")
                await self.browser_manager.refresh_page()
                
                # Wait a moment for page to load
                await asyncio.sleep(1)
            
            except Exception as e:
                await self._handle_error(e)
                # Wait before retrying
                await asyncio.sleep(self.config.refresh_interval)
    
    async def _handle_available_slot(self, slot: AvailableSlot) -> None:
        """
        Handle an available slot by attempting to book it.
        
        Args:
            slot: Available slot to book
        """
        self.logger.info(
            f"Available slot detected: {slot.slot_info.category} on {slot.slot_info.date}"
        )
        
        try:
            # Attempt booking
            result = await self.booking_handler.complete_booking(slot)
            
            # Send notification
            await self.telegram_notifier.send_booking_success(result)
            
            if result.success:
                self.logger.info("=" * 60)
                self.logger.info("🎉 RESERVATION LOCKED SUCCESSFULLY!")
                self.logger.info("=" * 60)
                self.logger.info(f"Category: {result.category}")
                self.logger.info(f"Date: {result.date}")
                self.logger.info(f"Time: {result.time}")
                self.logger.info("=" * 60)
                self.logger.info("⚠️  IMPORTANT: Browser will remain open")
                self.logger.info("📝 Please complete the remaining form fields manually")
                self.logger.info("🔔 Telegram notification has been sent")
                self.logger.info("=" * 60)
                self.logger.info("")
                self.logger.info("Press Ctrl+C when you're done to close the browser")
                
                # Stop monitoring but keep browser open
                self.running = False
                
                # Wait indefinitely until user presses Ctrl+C
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    self.logger.info("User requested shutdown")
            else:
                self.logger.warning("Booking failed, continuing monitoring")
        
        except Exception as e:
            await handle_booking_error(
                e,
                slot.slot_info.category,
                slot.slot_info.date
            )
    
    async def _handle_error(self, error: Exception) -> None:
        """
        Handle errors during monitoring.
        
        Args:
            error: Error that occurred
        """
        error_type = type(error).__name__
        
        # Categorize and handle different error types
        if "network" in str(error).lower() or "timeout" in str(error).lower():
            await handle_network_error(error, self.config.refresh_interval)
        elif "element" in str(error).lower() or "selector" in str(error).lower():
            await handle_page_parsing_error(error)
        else:
            self.logger.error(f"Unexpected error in monitoring loop: {error}", exc_info=True)
    
    async def _cleanup(self) -> None:
        """Clean up resources."""
        self.logger.info("Cleaning up resources")
        
        if self.browser_manager:
            await self.browser_manager.stop()
        
        self.logger.info("Shutdown complete")
    
    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def stop(self) -> None:
        """Stop the monitoring loop."""
        self.logger.info("Stop requested")
        self.running = False
