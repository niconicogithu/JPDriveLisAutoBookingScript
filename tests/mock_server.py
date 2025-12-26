"""Mock server for integration testing."""
from flask import Flask, render_template_string
import threading
import time

app = Flask(__name__)

# Mock HTML for facility selection page
FACILITY_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>施設予約 - Kanagawa e-Shinsei</title>
</head>
<body>
    <h1>施設予約</h1>
    <table class="rsv_table">
        <thead>
            <tr>
                <th>日付</th>
                <th>普通車</th>
                <th>準中型車</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2025-12-25</td>
                <td class="am">
                    {% if available_regular_am %}
                    <a href="/reserve/facilitySelect_decide?slot=regular_am">○</a>
                    {% else %}
                    <span>×</span>
                    {% endif %}
                </td>
                <td class="pm">
                    {% if available_regular_pm %}
                    <a href="/reserve/facilitySelect_decide?slot=regular_pm">○</a>
                    {% else %}
                    <span>×</span>
                    {% endif %}
                </td>
                <td class="am">
                    {% if available_semi_am %}
                    <a href="/reserve/facilitySelect_decide?slot=semi_am">○</a>
                    {% else %}
                    <span>×</span>
                    {% endif %}
                </td>
            </tr>
        </tbody>
    </table>
</body>
</html>
"""

# Mock HTML for time selection page
TIME_SELECTION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>時間選択 - Kanagawa e-Shinsei</title>
</head>
<body>
    <h1>時間選択</h1>
    <form method="post" action="/reserve/confirm">
        <input type="radio" name="time" value="09:00" checked> 09:00<br>
        <input type="radio" name="time" value="10:00"> 10:00<br>
        <input type="radio" name="time" value="11:00"> 11:00<br>
        <button type="submit">予約</button>
    </form>
</body>
</html>
"""

# Mock HTML for confirmation page
CONFIRMATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>予約完了 - Kanagawa e-Shinsei</title>
</head>
<body>
    <h1>予約が完了しました</h1>
    <p>予約番号: 12345</p>
</body>
</html>
"""


@app.route('/140007-u/reserve/facilitySelect_dateTrans')
def facility_select():
    """Mock facility selection page."""
    # Simulate availability (can be controlled via query params)
    available_regular_am = True
    available_regular_pm = False
    available_semi_am = True
    
    return render_template_string(
        FACILITY_PAGE_HTML,
        available_regular_am=available_regular_am,
        available_regular_pm=available_regular_pm,
        available_semi_am=available_semi_am
    )


@app.route('/reserve/facilitySelect_decide')
def time_selection():
    """Mock time selection page."""
    return render_template_string(TIME_SELECTION_HTML)


@app.route('/reserve/confirm', methods=['POST'])
def confirm_booking():
    """Mock booking confirmation page."""
    return render_template_string(CONFIRMATION_HTML)


class MockServer:
    """Mock server for testing."""
    
    def __init__(self, port=5000):
        self.port = port
        self.thread = None
        self.server = None
    
    def start(self):
        """Start the mock server in a background thread."""
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        time.sleep(1)  # Give server time to start
    
    def _run(self):
        """Run the Flask app."""
        app.run(port=self.port, debug=False, use_reloader=False)
    
    def stop(self):
        """Stop the mock server."""
        # Flask doesn't have a clean shutdown method in this setup
        # In production tests, use a proper WSGI server
        pass


if __name__ == '__main__':
    # Run mock server for manual testing
    app.run(port=5000, debug=True)
