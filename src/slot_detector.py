"""Slot detection logic for available booking slots."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from playwright.async_api import Page, ElementHandle
from src.logger import get_logger
from src.selectors import (
    CONSENT_CHECKBOX,
    SLOT_TABLE,
    DATE_HEADER_CELLS,
    CATEGORY_ROW_PREFIX,
    SLOT_CELLS,
    AVAILABLE_SLOT_LINK,
    CATEGORY_NAME_CELL,
)


@dataclass
class SlotInfo:
    """Information about a booking slot."""
    category: str  # e.g., "普通車ＡＭ", "準中型車ＡＭ"
    date: str  # e.g., "01/20 (Tue)"
    element: ElementHandle  # The clickable <a> element


@dataclass
class AvailableSlot:
    """An available booking slot with detection metadata."""
    slot_info: SlotInfo
    detected_at: datetime


class SlotDetector:
    """Detects available time slots on the facility selection page."""
    
    def __init__(self, page: Page, target_categories: List[str]):
        """
        Initialize slot detector.
        
        Args:
            page: Playwright page object
            target_categories: List of categories to monitor (e.g., ["準中型車ＡＭ", "普通車ＡＭ"])
        """
        self.page = page
        self.target_categories = target_categories
        self.logger = get_logger()
    
    async def ensure_consent_checked(self) -> bool:
        """
        Ensure the consent checkbox is checked.
        
        The checkbox is hidden and wrapped in a label, so we need to click the label.
        
        Returns:
            True if checkbox is checked (or was successfully checked), False otherwise
        """
        try:
            # First check if checkbox exists
            checkbox = await self.page.query_selector(CONSENT_CHECKBOX)
            if not checkbox:
                self.logger.warning("Consent checkbox not found")
                return False
            
            # Check if already checked
            is_checked = await checkbox.is_checked()
            
            if not is_checked:
                self.logger.info("Checking consent checkbox")
                
                # The checkbox is hidden, so we need to click the label instead
                label = await self.page.query_selector(f"label[for='reserveCaution']")
                
                if label:
                    # Click the label (which will check the hidden checkbox)
                    await label.click()
                    self.logger.debug("Clicked consent checkbox label")
                else:
                    # Fallback: try to force check the checkbox
                    await checkbox.evaluate("el => el.checked = true")
                    # Trigger change event
                    await checkbox.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")
                    self.logger.debug("Force-checked consent checkbox")
                
                # Wait a moment for any JavaScript to process
                await self.page.wait_for_timeout(500)
                
                # Verify it's checked
                is_checked = await checkbox.is_checked()
                if is_checked:
                    self.logger.info("Consent checkbox successfully checked")
                else:
                    self.logger.error("Failed to check consent checkbox")
                    return False
            else:
                self.logger.debug("Consent checkbox already checked")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking consent checkbox: {e}")
            return False
    
    async def check_availability(self) -> Optional[AvailableSlot]:
        """
        Check for available slots in target categories.
        
        First ensures consent checkbox is checked, then looks for available slots
        (green circles with class 'tdSelect enable') in the target categories.
        
        Returns:
            AvailableSlot if found, None otherwise
        """
        self.logger.debug(f"Checking availability for categories: {self.target_categories}")
        
        try:
            # Ensure consent is checked first
            if not await self.ensure_consent_checked():
                self.logger.warning("Cannot check availability - consent checkbox issue")
                return None
            
            # Get date headers to map column index to date
            date_headers = await self._get_date_headers()
            if not date_headers:
                self.logger.warning("Could not find date headers")
                return None
            
            self.logger.debug(f"Found {len(date_headers)} date columns")
            
            # Find all category rows
            rows = await self.page.query_selector_all(CATEGORY_ROW_PREFIX)
            
            for row in rows:
                # Get the category name from this row
                category_cell = await row.query_selector(CATEGORY_NAME_CELL)
                if not category_cell:
                    continue
                
                category_text = await category_cell.inner_text()
                category_text = category_text.strip()
                
                # Check if this row matches any of our target categories
                if category_text not in self.target_categories:
                    continue
                
                self.logger.debug(f"Checking row for category: {category_text}")
                
                # Get all available slot cells in this row
                available_cells = await row.query_selector_all(SLOT_CELLS["available"])
                
                if available_cells:
                    self.logger.debug(f"Found {len(available_cells)} available slots for {category_text}")
                    
                    # Check each available cell
                    for cell in available_cells:
                        try:
                            # Find the clickable link inside the cell
                            link = await cell.query_selector(AVAILABLE_SLOT_LINK)
                            
                            if link:
                                # Get the column index to determine the date
                                # We need to count which cell this is in the row
                                all_cells = await row.query_selector_all("td")
                                cell_index = -1
                                
                                for i, c in enumerate(all_cells):
                                    if await c.evaluate("(el, target) => el === target", cell):
                                        cell_index = i
                                        break
                                
                                if cell_index >= 0 and cell_index < len(date_headers):
                                    date = date_headers[cell_index]
                                    
                                    self.logger.info(f"✓ Found available slot: {category_text} on {date}")
                                    
                                    slot_info = SlotInfo(
                                        category=category_text,
                                        date=date,
                                        element=link
                                    )
                                    
                                    return AvailableSlot(
                                        slot_info=slot_info,
                                        detected_at=datetime.now()
                                    )
                        except Exception as e:
                            self.logger.debug(f"Error checking cell: {e}")
                            continue
            
            self.logger.debug("No available slots found")
            return None
            
        except Exception as e:
            self.logger.error(f"Error checking availability: {e}", exc_info=True)
            return None
    
    async def _get_date_headers(self) -> List[str]:
        """
        Get the date strings from the table header.
        
        Returns:
            List of date strings (e.g., ["01/18 (Sun)", "01/19 (Mon)", ...])
        """
        try:
            date_cells = await self.page.query_selector_all(DATE_HEADER_CELLS)
            dates = []
            
            for cell in date_cells:
                # Get the text content and clean it up
                text = await cell.inner_text()
                # Remove extra whitespace and newlines
                text = " ".join(text.split())
                dates.append(text)
            
            return dates
            
        except Exception as e:
            self.logger.error(f"Error getting date headers: {e}")
            return []
