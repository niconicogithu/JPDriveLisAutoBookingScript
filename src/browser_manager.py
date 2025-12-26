"""Browser management using Playwright."""
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page, Playwright
from src.logger import get_logger


class BrowserManager:
    """Manages Playwright browser lifecycle and navigation."""
    
    # Login page
    LOGIN_URL = "https://dshinsei.e-kanagawa.lg.jp/140007-u/profile/userLogin"
    # Initial page with agreement checkbox
    INITIAL_URL = "https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/offerList_detail?tempSeq=50909&accessFrom=offerList"
    # Final facility selection page
    FACILITY_URL = "https://dshinsei.e-kanagawa.lg.jp/140007-u/reserve/facilitySelect_dateTrans?movePage=oneMonthLater"
    
    def __init__(self, headless: bool = True, user_email: str = "", user_password: str = ""):
        """
        Initialize browser manager.
        
        Args:
            headless: Whether to run browser in headless mode
            user_email: Email address for login
            user_password: Password for login
        """
        self.headless = headless
        self.user_email = user_email
        self.user_password = user_password
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.logger = get_logger()
    
    async def start(self) -> None:
        """Start the browser and create a new page."""
        self.logger.info(f"Starting browser (headless={self.headless})")
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        
        self.logger.debug("Browser started successfully")
    
    async def login(self) -> None:
        """
        Login to e-kanagawa system.
        
        Navigates to login page, enters email and password, and submits the form.
        
        Raises:
            RuntimeError: If browser is not started or login fails
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.logger.info(f"Navigating to login page: {self.LOGIN_URL}")
        await self.page.goto(self.LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
        
        try:
            # Find and fill email field
            self.logger.debug("Looking for email input field")
            email_input = await self.page.query_selector('input#userLoginForm\\.userId')
            
            if not email_input:
                # Try alternative selectors
                email_input = await self.page.query_selector('input[name="userId"]')
            
            if email_input:
                self.logger.debug(f"Entering email: {self.user_email}")
                await email_input.fill(self.user_email)
            else:
                raise Exception("Could not find email input field")
            
            # Find and fill password field
            self.logger.debug("Looking for password input field")
            password_input = await self.page.query_selector('input#userLoginForm\\.userPasswd')
            
            if not password_input:
                # Try alternative selectors
                password_input = await self.page.query_selector('input[name="userPasswd"]')
            
            if password_input:
                self.logger.debug("Entering password")
                await password_input.fill(self.user_password)
            else:
                raise Exception("Could not find password input field")
            
            # Find and click login button
            self.logger.debug("Looking for login button")
            login_button = await self.page.query_selector('input[type="submit"][value="ログイン"]')
            
            if not login_button:
                # Try alternative selectors
                login_button = await self.page.query_selector('input[type="submit"]')
            
            if login_button:
                self.logger.info("Clicking login button")
                await login_button.click()
                
                # Wait for navigation after login (reduced wait time)
                await self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                
                # Check if login was successful by looking for logout button or user info
                # The logged-in page should have "ログアウト" button
                await self.page.wait_for_timeout(2000)
                
                # Check if we're still on login page (login failed)
                current_url = self.page.url
                if "userLogin" in current_url and "login" in current_url.lower():
                    # Check for error messages
                    error_msg = await self.page.query_selector('.errorMessage, .error, .alert')
                    if error_msg:
                        error_text = await error_msg.inner_text()
                        raise Exception(f"Login failed: {error_text}")
                    else:
                        raise Exception("Login failed: Still on login page")
                
                self.logger.info("✓ Login successful")
            else:
                raise Exception("Could not find login button")
                
        except Exception as e:
            self.logger.error(f"Error during login: {e}")
            # Take a screenshot for debugging
            try:
                await self.page.screenshot(path="logs/login_error.png")
                self.logger.info("Screenshot saved to logs/login_error.png")
            except:
                pass
            raise
    
    async def stop(self) -> None:
        """Stop the browser and clean up resources."""
        self.logger.info("Stopping browser")
        
        if self.page:
            await self.page.close()
            self.page = None
        
        if self.browser:
            await self.browser.close()
            self.browser = None
        
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
        
        self.logger.debug("Browser stopped successfully")
    
    async def navigate_to_facility_page(self) -> Page:
        """
        Navigate to the facility selection page.
        This involves:
        1. Loading the initial page
        2. Clicking the "1か月後" button ONCE to navigate to facility selection page
        3. Checking the agreement checkbox (上記内容に同意する) on facility page
        
        Returns:
            The page object after navigation
        
        Raises:
            RuntimeError: If browser is not started
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.logger.info(f"Navigating to initial page: {self.INITIAL_URL}")
        await self.page.goto(self.INITIAL_URL, wait_until="domcontentloaded", timeout=30000)
        
        try:
            # Step 1: Click the "1か月後" button ONCE to get to facility selection page
            self.logger.info("Clicking '1か月後' button to navigate to facility selection page")
            
            # Button selectors
            button_selectors = [
                "input[type='button'][value='1か月後＞']",
                "input[type='button'][title='1か月後に進む']",
                "input[type='button'][onclick*='oneMonthLater']",
                "input[type='button'].button[value*='1か月後']",
                "input[type='button'][value*='1か月後']",
                "button:has-text('1か月後')",
                "a:has-text('1か月後')",
            ]
            
            # Click button to navigate to facility selection page
            button_found = False
            for selector in button_selectors:
                try:
                    button = await self.page.query_selector(selector)
                    if button:
                        self.logger.debug(f"Found '1か月後' button with selector: {selector}")
                        await button.click()
                        button_found = True
                        self.logger.info("✓ Clicked '1か月後' button")
                        
                        # Wait for page to navigate
                        await self.page.wait_for_timeout(1000)
                        await self.page.wait_for_url("**/facilitySelect_dateTrans**", timeout=10000)
                        await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                        break
                except Exception as e:
                    self.logger.debug(f"Button selector {selector} failed: {e}")
                    continue
            
            if not button_found:
                raise Exception("Could not find '1か月後' button")
            
            self.logger.info("✓ Arrived at facility selection page")
            
            # Step 2: Check the agreement checkbox (上記内容に同意する)
            self.logger.debug("Looking for agreement checkbox on facility page")
            
            # Try multiple possible selectors for the checkbox
            checkbox_selectors = [
                "input[type='checkbox']",
                "input[name*='agree']",
                "input[id*='agree']",
                "#agree",
            ]
            
            checkbox_found = False
            for selector in checkbox_selectors:
                try:
                    checkbox = await self.page.query_selector(selector)
                    if checkbox:
                        # Check if this is the agreement checkbox by looking at nearby text
                        parent = await checkbox.evaluate_handle("el => el.parentElement")
                        parent_text = await parent.inner_text() if parent else ""
                        
                        if "同意" in parent_text or "agree" in parent_text.lower():
                            self.logger.debug(f"Found agreement checkbox with selector: {selector}")
                            await checkbox.check()
                            checkbox_found = True
                            self.logger.info("✓ Agreement checkbox checked")
                            break
                except Exception as e:
                    self.logger.debug(f"Checkbox selector {selector} failed: {e}")
                    continue
            
            if not checkbox_found:
                self.logger.warning("Could not find agreement checkbox, attempting to continue anyway")
            
            self.logger.info("✓ Ready to start monitoring for available slots")
            
        except Exception as e:
            self.logger.error(f"Error during navigation flow: {e}")
            # Take a screenshot for debugging
            try:
                await self.page.screenshot(path="logs/navigation_error.png")
                self.logger.info("Screenshot saved to logs/navigation_error.png")
            except:
                pass
            raise
        
        return self.page
    
    async def get_page(self) -> Page:
        """
        Get the current page object.
        
        Returns:
            The current page object
        
        Raises:
            RuntimeError: If browser is not started
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        return self.page
    
    async def refresh_page(self) -> Page:
        """
        Refresh the current page.
        Used for monitoring loop - just refreshes the facility page.
        
        Returns:
            The page object after refresh
        
        Raises:
            RuntimeError: If browser is not started
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.logger.debug("Refreshing page")
        await self.page.reload(wait_until="networkidle")
        
        return self.page
    
    async def __aenter__(self):
        """Context manager entry."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.stop()
