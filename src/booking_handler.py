"""Booking flow handler for completing reservations."""
import time
from dataclasses import dataclass
from typing import Optional
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from src.slot_detector import AvailableSlot
from src.logger import get_logger


@dataclass
class BookingResult:
    """Result of a booking attempt."""
    success: bool
    category: str
    date: str
    time: str
    error_message: Optional[str] = None


class BookingHandler:
    """Handles the booking flow once an available slot is detected."""
    
    # Expected URLs in the booking flow
    TIME_SELECTION_URL = "**/facilitySelect_decide**"
    PROCEDURE_EXPLANATION_URL = "**/offerDetail_initDisplay**"
    
    MAX_BOOKING_TIME = 15  # seconds
    
    def __init__(self, page: Page):
        """
        Initialize booking handler.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.logger = get_logger()
    
    async def complete_booking(self, slot: AvailableSlot) -> BookingResult:
        """
        Complete the booking flow for an available slot.
        
        Flow:
        1. Click the slot → Navigate to time selection page
        2. Select first available time checkbox
        3. Click "予約する" button → Navigate to procedure explanation page
        4. Click "同意する" button → Lock the reservation
        5. Return success (browser stays open for user to complete form)
        
        Args:
            slot: Available slot to book
        
        Returns:
            BookingResult with success status and details
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Starting booking flow for {slot.slot_info.category} on {slot.slot_info.date}")
            
            # Step 1: Click the slot
            await self._click_slot(slot.slot_info.element)
            
            # Step 2: Wait for time selection page
            await self._wait_for_time_selection_page()
            
            # Step 3: Select first available time
            selected_time = await self._select_first_available_time()
            
            # Step 4: Click "予約する" button
            await self._click_reserve_button()
            
            # Step 5: Wait for procedure explanation page
            await self._wait_for_procedure_explanation_page()
            
            # Step 6: Click "同意する" button to lock the reservation
            await self._click_agree_button()
            
            elapsed_time = time.time() - start_time
            self.logger.info(f"✓ Reservation locked successfully in {elapsed_time:.2f} seconds")
            self.logger.info("Browser will remain open for you to complete the remaining form fields")
            
            return BookingResult(
                success=True,
                category=slot.slot_info.category,
                date=slot.slot_info.date,
                time=selected_time,
            )
        
        except Exception as e:
            elapsed_time = time.time() - start_time
            error_msg = f"Booking failed after {elapsed_time:.2f} seconds: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            
            return BookingResult(
                success=False,
                category=slot.slot_info.category,
                date=slot.slot_info.date,
                time="",
                error_message=error_msg,
            )
    
    async def _click_slot(self, element) -> None:
        """
        Click on the slot element.
        
        Args:
            element: Element to click
        """
        self.logger.debug("Clicking slot element")
        await element.click()
        await self.page.wait_for_timeout(1000)
    
    async def _wait_for_time_selection_page(self) -> None:
        """Wait for the time selection page to load."""
        self.logger.debug("Waiting for time selection page")
        
        try:
            # Wait for URL to change to time selection page
            await self.page.wait_for_url(self.TIME_SELECTION_URL, timeout=10000)
            await self.page.wait_for_load_state("networkidle", timeout=10000)
            
            self.logger.info("✓ Time selection page loaded")
        except PlaywrightTimeoutError:
            self.logger.warning("Timeout waiting for time selection page, continuing anyway")
    
    async def _select_first_available_time(self) -> str:
        """
        Select the first available time slot checkbox.
        
        The time selection page has checkboxes with class "checkbox_hide" and IDs like:
        - reserveTimeCheck_2_6 (準中型車ＡＭの08時30分)
        
        Returns:
            Selected time as string
        """
        self.logger.debug("Selecting first available time")
        
        try:
            # Find all time selection checkboxes
            # They have class "checkbox_hide" and are inside td elements with class "enable"
            checkboxes = await self.page.query_selector_all('input[type="checkbox"].checkbox_hide')
            
            if not checkboxes:
                self.logger.warning("No time checkboxes found")
                return "Unknown"
            
            # Find the first checkbox that is inside an enabled cell
            for checkbox in checkboxes:
                # Check if the parent td has class "enable"
                parent_td = await checkbox.evaluate_handle("el => el.closest('td')")
                if parent_td:
                    class_name = await parent_td.get_attribute("class")
                    if class_name and "enable" in class_name:
                        # This is an available time slot
                        checkbox_id = await checkbox.get_attribute("id")
                        
                        # Get the label text for this checkbox
                        label = await self.page.query_selector(f'label[for="{checkbox_id}"]')
                        if label:
                            time_text = await label.inner_text()
                            time_text = time_text.strip()
                        else:
                            time_text = "Unknown time"
                        
                        # Click the checkbox (or its parent td which is clickable)
                        await parent_td.click()
                        
                        self.logger.info(f"✓ Selected time: {time_text}")
                        
                        # Wait a moment for any JavaScript
                        await self.page.wait_for_timeout(500)
                        
                        return time_text
            
            # If no enabled checkbox found, just click the first one
            first_checkbox = checkboxes[0]
            checkbox_id = await first_checkbox.get_attribute("id")
            label = await self.page.query_selector(f'label[for="{checkbox_id}"]')
            if label:
                time_text = await label.inner_text()
            else:
                time_text = "First available"
            
            # Try to click the parent td
            parent_td = await first_checkbox.evaluate_handle("el => el.closest('td')")
            if parent_td:
                await parent_td.click()
            else:
                # Fallback: force check the checkbox
                await first_checkbox.evaluate("el => el.checked = true")
            
            self.logger.info(f"✓ Selected time: {time_text}")
            return time_text
            
        except Exception as e:
            self.logger.error(f"Error selecting time: {e}", exc_info=True)
            return "Unknown"
    
    async def _click_reserve_button(self) -> None:
        """Click the '予約する' button on time selection page."""
        self.logger.debug("Clicking '予約する' button")
        
        try:
            # The button has onclick="showWarningPossibleCntOver();"
            button = await self.page.query_selector('button[onclick*="showWarningPossibleCntOver"]')
            
            if not button:
                # Fallback: try to find by text
                button = await self.page.query_selector('button:has-text("予約する")')
            
            if button:
                await button.click()
                self.logger.info("✓ Clicked '予約する' button")
                await self.page.wait_for_timeout(1000)
            else:
                raise Exception("Could not find '予約する' button")
                
        except Exception as e:
            self.logger.error(f"Error clicking reserve button: {e}")
            raise
    
    async def _wait_for_procedure_explanation_page(self) -> None:
        """Wait for the procedure explanation page to load."""
        self.logger.debug("Waiting for procedure explanation page")
        
        try:
            # Wait for URL to change to procedure explanation page
            await self.page.wait_for_url(self.PROCEDURE_EXPLANATION_URL, timeout=10000)
            await self.page.wait_for_load_state("networkidle", timeout=10000)
            
            self.logger.info("✓ Procedure explanation page loaded")
        except PlaywrightTimeoutError:
            self.logger.warning("Timeout waiting for procedure explanation page, continuing anyway")
    
    async def _click_agree_button(self) -> None:
        """Click the '同意する' button on procedure explanation page to lock the reservation."""
        self.logger.debug("Clicking '同意する' button")
        
        try:
            # The button has onclick="formSubmit(this.form, 'offerDetail_mailto')"
            # and value="同意する"
            button = await self.page.query_selector('input[type="submit"][value="同意する"]')
            
            if not button:
                # Fallback: try to find by ID
                button = await self.page.query_selector('input#ok')
            
            if button:
                await button.click()
                self.logger.info("✓ Clicked '同意する' button - Reservation is now locked!")
                
                # Wait for the page to process
                await self.page.wait_for_timeout(2000)
            else:
                raise Exception("Could not find '同意する' button")
                
        except Exception as e:
            self.logger.error(f"Error clicking agree button: {e}")
            raise
