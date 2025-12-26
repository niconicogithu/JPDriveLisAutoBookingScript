# Deployment Guide

This guide covers deploying the booking system for continuous operation.

## Deployment Options

1. **Local Machine** - Run on your personal computer
2. **Cloud Server** - Run on AWS, GCP, Azure, or DigitalOcean
3. **Raspberry Pi** - Run on a low-power device at home

## Prerequisites

- Python 3.9 or higher
- Stable internet connection
- Telegram bot configured
- Tested configuration (see TESTING.md)

## Option 1: Local Machine (macOS/Linux)

### Using nohup

Run the script in the background:

```bash
# Start the system
nohup python3 main.py --headless > output.log 2>&1 &

# Save the process ID
echo $! > booking_system.pid
```

Monitor logs:
```bash
tail -f logs/booking_system.log
```

Stop the system:
```bash
# Get the process ID
PID=$(cat booking_system.pid)

# Send termination signal
kill $PID

# Or force kill if needed
kill -9 $PID
```

### Using screen (Recommended for SSH sessions)

```bash
# Start a screen session
screen -S booking

# Run the system
python3 main.py --headless

# Detach from screen: Press Ctrl+A, then D

# Reattach to screen
screen -r booking

# List all screens
screen -ls

# Kill screen session
screen -X -S booking quit
```

### Using tmux

```bash
# Start a tmux session
tmux new -s booking

# Run the system
python3 main.py --headless

# Detach from tmux: Press Ctrl+B, then D

# Reattach to tmux
tmux attach -t booking

# List all sessions
tmux ls

# Kill session
tmux kill-session -t booking
```

## Option 2: systemd Service (Linux)

### Create Service File

Create `/etc/systemd/system/booking-system.service`:

```ini
[Unit]
Description=JP Driving License Auto-Booking System
After=network.target

[Service]
Type=simple
User=your_username
Group=your_groupname
WorkingDirectory=/path/to/jp-driving-license-auto-booking
Environment="PATH=/path/to/venv/bin:/usr/local/bin:/usr/bin:/bin"

# Load environment variables from .env file
EnvironmentFile=/path/to/jp-driving-license-auto-booking/.env

# Run the main script
ExecStart=/path/to/venv/bin/python3 main.py --headless

# Restart policy
Restart=on-failure
RestartSec=10

# Logging
StandardOutput=append:/path/to/jp-driving-license-auto-booking/logs/systemd.log
StandardError=append:/path/to/jp-driving-license-auto-booking/logs/systemd-error.log

[Install]
WantedBy=multi-user.target
```

### Install and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable booking-system

# Start the service
sudo systemctl start booking-system

# Check status
sudo systemctl status booking-system

# View logs
sudo journalctl -u booking-system -f

# Stop the service
sudo systemctl stop booking-system

# Restart the service
sudo systemctl restart booking-system

# Disable service
sudo systemctl disable booking-system
```

## Option 3: Cloud Server Deployment

### AWS EC2 / DigitalOcean / Linode

1. **Create a server instance:**
   - Ubuntu 22.04 LTS or newer
   - Minimum: 1 vCPU, 1GB RAM
   - Recommended: 2 vCPU, 2GB RAM

2. **Connect via SSH:**
```bash
ssh user@your-server-ip
```

3. **Install dependencies:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install system dependencies for Playwright
sudo apt install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2
```

4. **Clone and setup project:**
```bash
# Clone repository (or upload files)
git clone <your-repo-url>
cd jp-driving-license-auto-booking

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

5. **Configure environment:**
```bash
# Create .env file
cp .env.example .env
nano .env  # Edit with your credentials
```

6. **Set up systemd service** (see Option 2 above)

7. **Configure firewall (optional):**
```bash
# Allow SSH
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable
```

## Option 4: Raspberry Pi

Perfect for 24/7 operation with low power consumption.

### Setup Steps

1. **Install Raspberry Pi OS Lite** (64-bit recommended)

2. **Update system:**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Install dependencies:**
```bash
# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install Chromium dependencies
sudo apt install chromium-browser chromium-codecs-ffmpeg -y
```

4. **Follow cloud server steps 4-6** above

5. **Optimize for Raspberry Pi:**
```bash
# Reduce memory usage in .env
HEADLESS=true
LOG_LEVEL=WARNING
```

## Monitoring and Maintenance

### Log Monitoring

View real-time logs:
```bash
tail -f logs/booking_system.log
```

Search logs for errors:
```bash
grep ERROR logs/booking_system.log
grep CRITICAL logs/booking_system.log
```

View last 100 lines:
```bash
tail -n 100 logs/booking_system.log
```

### Log Rotation

Logs automatically rotate at:
- 100MB file size
- 7 backup files kept

Manual log cleanup:
```bash
# Remove old logs
find logs/ -name "*.log.*" -mtime +7 -delete
```

### Disk Space Monitoring

Check disk usage:
```bash
df -h
du -sh logs/
```

### Health Checks

Create a monitoring script `check_health.sh`:

```bash
#!/bin/bash

LOG_FILE="logs/booking_system.log"
ALERT_EMAIL="your-email@example.com"

# Check if process is running
if ! pgrep -f "main.py" > /dev/null; then
    echo "Booking system is not running!" | mail -s "Alert: Booking System Down" $ALERT_EMAIL
    exit 1
fi

# Check if logs are being written (activity in last 5 minutes)
if [ -f "$LOG_FILE" ]; then
    LAST_LOG=$(find "$LOG_FILE" -mmin -5)
    if [ -z "$LAST_LOG" ]; then
        echo "No log activity in last 5 minutes!" | mail -s "Alert: Booking System Inactive" $ALERT_EMAIL
        exit 1
    fi
fi

echo "System healthy"
```

Add to crontab:
```bash
# Edit crontab
crontab -e

# Add health check every 5 minutes
*/5 * * * * /path/to/check_health.sh
```

### Automatic Restart on Failure

With systemd (already configured in service file):
```ini
Restart=on-failure
RestartSec=10
```

With cron (if using nohup):
```bash
# Edit crontab
crontab -e

# Add restart check every 5 minutes
*/5 * * * * pgrep -f "main.py" || (cd /path/to/project && nohup python3 main.py --headless > output.log 2>&1 &)
```

## Backup and Recovery

### Backup Configuration

```bash
# Backup .env file (securely)
cp .env .env.backup

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

### Recovery

```bash
# Restore configuration
cp .env.backup .env

# Restart service
sudo systemctl restart booking-system
```

## Security Best Practices

1. **Secure credentials:**
   - Never commit `.env` to version control
   - Use environment variables in production
   - Rotate Telegram bot token periodically

2. **Server security:**
   - Keep system updated: `sudo apt update && sudo apt upgrade`
   - Use SSH keys instead of passwords
   - Configure firewall (ufw)
   - Disable root login

3. **Access control:**
   - Use non-root user for running the service
   - Set proper file permissions:
     ```bash
     chmod 600 .env
     chmod 700 logs/
     ```

## Resource Requirements

### Minimum Requirements
- CPU: 1 core
- RAM: 512MB
- Disk: 2GB
- Network: Stable internet connection

### Recommended Requirements
- CPU: 2 cores
- RAM: 1GB
- Disk: 5GB (for logs)
- Network: Stable internet with low latency

### Expected Resource Usage
- CPU: 5-10% average (spikes during page loads)
- RAM: 200-400MB
- Disk: ~10MB/day for logs
- Network: ~1MB/hour

## Troubleshooting Deployment

### Service Won't Start

Check logs:
```bash
sudo journalctl -u booking-system -n 50
```

Common issues:
- Wrong Python path in service file
- Missing environment variables
- Permission issues

### High Memory Usage

Reduce memory usage:
```bash
# In .env
HEADLESS=true
LOG_LEVEL=WARNING
```

Restart service:
```bash
sudo systemctl restart booking-system
```

### Browser Crashes

Install missing dependencies:
```bash
playwright install-deps chromium
```

### Can't Connect to Website

Check network:
```bash
curl -I https://dshinsei.e-kanagawa.lg.jp
```

Check DNS:
```bash
nslookup dshinsei.e-kanagawa.lg.jp
```

## Updating the System

```bash
# Stop the service
sudo systemctl stop booking-system

# Pull latest changes
git pull

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl start booking-system

# Check status
sudo systemctl status booking-system
```

## Uninstalling

```bash
# Stop and disable service
sudo systemctl stop booking-system
sudo systemctl disable booking-system

# Remove service file
sudo rm /etc/systemd/system/booking-system.service

# Reload systemd
sudo systemctl daemon-reload

# Remove project directory
rm -rf /path/to/jp-driving-license-auto-booking
```
