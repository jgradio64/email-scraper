# Email Notification Scraper

This Python application retrieves recent emails from an IMAP server (Gmail or Yahoo), parses their subject lines, and forwards them to a mobile phone via email-to-text (SMTP). The tool is intended as a lightweight notification system for critical updates (e.g., account activity or billing alerts) that would otherwise be missed due to lack of native SMS support.
Project Structure
* `main.py`: Entry point for the program. Loads environment variables, initiates email retrieval and forwarding.
* `email_retriever.py`: Handles connection to the IMAP server using `imaplib`, filters emails by date, and extracts subject lines.
* `notification_sender.py`: Uses Python’s `smtplib` to send parsed messages to a mobile device via email-to-text gateway.
* `helper_functions.py`: Utility functions for date range building, encoding fixes (e.g., UTF-8 decoding), and other parsing tasks.

# Scripts
* `setup.sh`: Creates a virtual environment and installs dependencies.
* `run.sh`: Activates the environment and runs the main script.

# Tech Stack
* Python 3
* `imaplib`, `email`, `smtplib`, `json` (standard library)
* Bash for environment setup and execution
* Gmail and Yahoo IMAP/SMTP servers (API-like usage)
