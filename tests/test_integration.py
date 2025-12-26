"""Integration tests with mock server."""
import pytest
import asyncio
from tests.mock_server import MockServer


@pytest.fixture(scope="module")
def mock_server():
    """Start mock server for testing."""
    server = MockServer(port=5555)
    server.start()
    yield server
    server.stop()


@pytest.mark.asyncio
async def test_mock_server_running(mock_server):
    """Test that mock server is accessible."""
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:5555/140007-u/reserve/facilitySelect_dateTrans"
        async with session.get(url) as response:
            assert response.status == 200
            text = await response.text()
            assert "施設予約" in text


# Note: Full integration tests would require:
# 1. Modifying BrowserManager to use mock server URL
# 2. Testing complete booking flow
# 3. Verifying Telegram notifications (with mock)
# These are marked as optional in the task list
