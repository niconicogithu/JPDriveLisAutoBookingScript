"""Test that all modules can be imported successfully."""
import pytest


def test_import_config():
    """Test importing config module."""
    from src.config import Config
    assert Config is not None


def test_import_logger():
    """Test importing logger module."""
    from src.logger import setup_logger, get_logger
    assert setup_logger is not None
    assert get_logger is not None


def test_import_browser_manager():
    """Test importing browser manager module."""
    from src.browser_manager import BrowserManager
    assert BrowserManager is not None


def test_import_slot_detector():
    """Test importing slot detector module."""
    from src.slot_detector import SlotDetector, SlotInfo, AvailableSlot
    assert SlotDetector is not None
    assert SlotInfo is not None
    assert AvailableSlot is not None


def test_import_booking_handler():
    """Test importing booking handler module."""
    from src.booking_handler import BookingHandler, BookingResult
    assert BookingHandler is not None
    assert BookingResult is not None


def test_import_telegram_notifier():
    """Test importing telegram notifier module."""
    from src.telegram_notifier import TelegramNotifier
    assert TelegramNotifier is not None


def test_import_error_handler():
    """Test importing error handler module."""
    from src.error_handler import retry_with_backoff
    assert retry_with_backoff is not None


def test_import_booking_controller():
    """Test importing booking controller module."""
    from src.booking_controller import BookingController
    assert BookingController is not None
