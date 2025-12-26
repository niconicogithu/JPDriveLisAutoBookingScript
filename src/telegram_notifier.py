"""Telegram notification service."""
import aiohttp
from src.booking_handler import BookingResult
from src.logger import get_logger


class TelegramNotifier:
    """Sends notifications via Telegram Bot API."""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        self.logger = get_logger()
    
    async def send_booking_success(self, result: BookingResult) -> None:
        """
        Send a booking success notification.
        
        Args:
            result: Booking result to notify about
        """
        message = self._format_message(result)
        await self._send_message(message)
    
    async def send_error_notification(self, error: str) -> None:
        """
        Send an error notification.
        
        Args:
            error: Error message to send
        """
        message = f"⚠️ Booking System Error\n\n{error}"
        await self._send_message(message)
    
    def _format_message(self, result: BookingResult) -> str:
        """
        Format a booking result into a notification message.
        
        Args:
            result: Booking result to format
        
        Returns:
            Formatted message string
        """
        if result.success:
            message = (
                "🎉 <b>予約ロック成功！</b>\n\n"
                f"📋 <b>Category:</b> {result.category}\n"
                f"📅 <b>Date:</b> {result.date}\n"
                f"⏰ <b>Time:</b> {result.time}\n\n"
                "⚠️ <b>重要：</b>\n"
                "予約はロックされましたが、まだ完了していません。\n\n"
                "📝 <b>次のステップ：</b>\n"
                "1. ブラウザで残りのフォームを入力してください\n"
                "2. すべての情報を入力して送信してください\n"
                "3. 確認メールが届くまで待ってください\n\n"
                "💻 ブラウザは開いたままになっています。\n"
                "今すぐフォームを完成させてください！"
            )
        else:
            message = (
                "❌ <b>予約失敗</b>\n\n"
                f"📋 <b>Category:</b> {result.category}\n"
                f"📅 <b>Date:</b> {result.date}\n"
                f"⚠️ <b>Error:</b> {result.error_message}\n\n"
                "システムは引き続き空き枠を監視します。"
            )
        
        return message
    
    async def _send_message(self, message: str) -> None:
        """
        Send a message via Telegram API.
        
        Args:
            message: Message text to send
        """
        try:
            self.logger.debug(f"Sending Telegram message: {message[:50]}...")
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                }
                
                async with session.post(self.api_url, json=payload, timeout=10) as response:
                    if response.status == 200:
                        self.logger.info("Telegram notification sent successfully")
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Telegram API error: {response.status} - {error_text}")
        
        except aiohttp.ClientError as e:
            self.logger.error(f"Failed to send Telegram notification: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error sending Telegram notification: {e}")
