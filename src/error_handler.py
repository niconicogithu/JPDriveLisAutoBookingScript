"""Error handling and retry logic."""
import asyncio
from typing import Callable, TypeVar, Any
from src.logger import get_logger

T = TypeVar('T')

# Retry configuration
MAX_RETRIES = 3
INITIAL_DELAY = 5  # seconds
BACKOFF_FACTOR = 2


async def retry_with_backoff(
    operation: Callable[[], Any],
    max_retries: int = MAX_RETRIES,
    initial_delay: float = INITIAL_DELAY,
    backoff_factor: float = BACKOFF_FACTOR,
    operation_name: str = "operation"
) -> Any:
    """
    Retry an async operation with exponential backoff.
    
    Args:
        operation: Async function to retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay on each retry
        operation_name: Name of operation for logging
    
    Returns:
        Result of the operation
    
    Raises:
        Exception: If all retries are exhausted
    """
    logger = get_logger()
    
    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"{operation_name} failed after {max_retries} attempts: {e}")
                raise
            
            delay = initial_delay * (backoff_factor ** attempt)
            logger.warning(
                f"{operation_name} failed (attempt {attempt + 1}/{max_retries}): {e}. "
                f"Retrying in {delay} seconds..."
            )
            await asyncio.sleep(delay)


async def handle_network_error(error: Exception, retry_delay: float = 5.0) -> None:
    """
    Handle network errors with logging and delay.
    
    Args:
        error: The network error that occurred
        retry_delay: Delay before retry in seconds
    """
    logger = get_logger()
    logger.warning(f"Network error: {error}. Retrying in {retry_delay} seconds...")
    await asyncio.sleep(retry_delay)


async def handle_page_parsing_error(error: Exception) -> None:
    """
    Handle page parsing errors with logging.
    
    Args:
        error: The parsing error that occurred
    """
    logger = get_logger()
    logger.warning(f"Page parsing error: {error}. Continuing to next refresh cycle...")


async def handle_booking_error(error: Exception, category: str, date: str) -> None:
    """
    Handle booking flow errors with detailed logging.
    
    Args:
        error: The booking error that occurred
        category: Booking category
        date: Booking date
    """
    logger = get_logger()
    logger.error(
        f"Booking failed for {category} on {date}: {error}. "
        "Resuming monitoring..."
    )
