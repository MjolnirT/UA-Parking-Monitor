# UA Parking Monitor

An automated tool to monitor and notify users when parking permits become available at the University of Arizona.

## Description

This script continuously monitors the UA parking permit website for available garage parking permits. When a desired permit becomes available, it automatically sends an email notification to the user.

## Features

- Automated login with NetID support
- Two-factor authentication handling
- Real-time monitoring of specific garage permits
- Email notifications when permits become available
- Screenshot logging of permit availability status
- Configurable refresh intervals

## Prerequisites

- Python 3.7+
- Playwright
- SMTP server access (currently configured for Mailgun)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/UA-Parking-Monitor.git
cd UA-Parking-Monitor
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

## Configuration

Before running the script, you need to configure the following variables in `main.py`:

1. Authentication details:
```python
netid = "your_netid"  # Your UA NetID
password = "your_password"  # Your UA password
```

2. Permit preferences:
```python
permit_category = "Garage Parking Permits"
permit_name = "2024-2025 Garage Specific"
permit_locations = ["(SEC) Second Street Garage : General"]
```

3. Email notification settings:
```python
smtp_server = 'smtp_server'
smtp_port = 587
smtp_username = 'your_smtp_mailbox@example.com'
smtp_password = 'smtp_password'
from_address = 'your_smtp_mailbox@example.com'
to_address = 'receiver_mailbox@example.com'
```

## Usage

Run the script using:
```bash
python main.py
```

The script will:
1. Open a browser window (visible by default)
2. Log in to the UA parking portal
3. Monitor selected permit types
4. Send email notifications when permits become available
5. Take screenshots for logging purposes

## Screenshots

Screenshots are saved in the `log` directory with timestamps in the format: `garage_YYYY-MM-DD_HH-MM-SS.png`

## Notes

- The script uses a invisible browser window by default (headless=True)
- Default refresh interval is set to 60 seconds
- After finding an available permit, the script waits for 15 minutes before continuing
- Email notifications are sent through Mailgun SMTP server

## Security Notice

- Never commit your credentials to version control
- Keep your SMTP credentials secure
- Consider using environment variables for sensitive information

## Contributing

Feel free to submit issues and enhancement requests!