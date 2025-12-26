#!/usr/bin/env python3
"""
JP Driving License Auto-Booking System

Main entry point for the automated booking system.
"""
import asyncio
import argparse
import sys
from src.config import Config
from src.logger import setup_logger
from src.booking_controller import BookingController


async def main() -> None:
    """Main entry point."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="JP Driving License Auto-Booking System"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (overrides .env)"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser in headed mode (overrides .env)"
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (overrides .env)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set log level (overrides .env)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = Config.load()
        
        # Apply command-line overrides
        if args.headless:
            config.headless = True
        if args.headed:
            config.headless = False
        if args.test_mode:
            config.test_mode = True
        if args.log_level:
            config.log_level = args.log_level
        
        # Validate configuration
        config.validate()
    
    except Exception as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Set up logging
    logger = setup_logger(config.log_level)
    logger.info("=" * 60)
    logger.info("JP Driving License Auto-Booking System")
    logger.info("=" * 60)
    
    # Create and start controller
    controller = BookingController(config)
    
    try:
        await controller.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
