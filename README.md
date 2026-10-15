# Daily Motivation Email Automation

A Python project that sends daily motivational emails to configured recipients through Gmail. Each email includes a motivational quote, a short message, and a cream-and-gold HTML newsletter design with a plain-text alternative.

The project is designed to share a small dose of positivity and encouragement while demonstrating practical Python automation, JSON-based content management, email delivery, and environment-based configuration.

## Features

- **240 motivational entries:** Eight categories covering self-learning, workouts and health, study and focus, planning and goals, life and happiness, resilience and confidence, habits and productivity, and relationships and kindness.
- **Date-based quote selection:** Selects an entry based on the current date, so repeated runs on the same day select the same entry.
- **HTML newsletter:** Generates a formatted email with a cream-and-gold design, date, quote, author, and daily message.
- **Plain-text alternative:** Includes a plain-text version for email clients that do not display HTML.
- **Multiple recipients:** Reads recipient addresses from a JSON configuration file and sends each email separately.
- **Gmail SMTP:** Sends email through Gmail's SMTP server using TLS.
- **Environment-based credentials:** Loads the Gmail address and App Password from a local `.env` file.
- **Content validation:** Checks that the quotes file contains valid entries with the required text fields.

## Technologies Used

- Python
- JSON
- `smtplib` and `email.message`
- HTML
- `python-dotenv`
- Gmail SMTP

## Project Structure

```text
daily-motivation-email-automation/
├── src/
│   ├── main.py
│   ├── email_sender.py
│   └── content_manager.py
├── data/
│   ├── quotes.json
│   ├── recipients.example.json
│   └── recipients.json          # Local file; ignored by Git
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── test_content.py
```

The local `.env` file is also required for sending emails, but it is intentionally excluded from the repository.

## How It Works

1. `content_manager.py` loads and validates the motivational entries from `data/quotes.json`.
2. It selects an entry using the current date.
3. `main.py` creates the email subject, plain-text message, and HTML newsletter.
4. The application loads recipient addresses from `data/recipients.json`.
5. `email_sender.py` connects to Gmail SMTP, starts TLS, signs in with the configured credentials, and sends the message to each recipient.
6. The application prints the result of each sending attempt in the terminal.

The quote selection is date-based rather than random. Running the program multiple times on the same date selects the same entry. With 240 entries and an unchanged file, the index advances through the list daily and cycles after the full list has been traversed.

## Prerequisites

- Python installed on your computer.
- A Gmail account.
- Google 2-Step Verification enabled and a Gmail App Password for SMTP access.
- Email addresses for recipients who have agreed to receive the messages.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/kommeranithinreddy/daily-motivation-email-automation.git
cd daily-motivation-email-automation
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure email credentials

Create a file named `.env` in the project root. Use `.env.example` as a template and add your own values:

```text
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
```

Use a Gmail App Password, not your regular Google account password. Keep `.env` private and never commit it to Git.

### 4. Configure recipients

Copy `data/recipients.example.json` to `data/recipients.json`.

Replace the example addresses with the addresses of your intended recipients:

```json
[
    "recipient1@example.com",
    "recipient2@example.com"
]
```

Save the file as `data/recipients.json`. This local file is excluded from Git so that real recipient addresses are not published.

## Usage

Run the application from the project root:

```bash
python -m src.main
```

The program selects the day's quote, builds the newsletter, and attempts to send an email to each configured recipient. Check the terminal output and recipient inboxes to verify the result.

**Note:** Running the program more than once on the same day can send the same day's email again. The current version does not keep a delivery log or prevent duplicate sends.

## Testing

Run the content validation test from the project root:

```bash
python test_content.py
```

This checks the quote data and its compatibility with the content manager. The application has also been manually tested by sending emails to the configured recipients.

## Security and Privacy

- `.env` contains credentials and must remain local.
- `data/recipients.json` contains actual recipient addresses and must remain local.
- `.env.example` and `data/recipients.example.json` contain placeholders for setup.
- The `.gitignore` file excludes the private configuration files and Python cache files.
- Only send messages to people who have agreed to receive them. If the recipient list grows, provide a clear way for recipients to opt out.

Before pushing changes, check the staged files with `git status` and confirm that `.env` and `data/recipients.json` are not included.

## Automation Status

The application currently runs when started manually. Scheduling it to run daily with Windows Task Scheduler is the next planned step; automatic scheduling and recovery behavior have not yet been configured or verified.

## Possible Future Improvements

- Configure and test daily execution with Windows Task Scheduler.
- Add delivery logging and duplicate-send prevention if needed.
- Add safer automated tests for email construction without sending real emails.
- Expand or refine the motivational content over time.
