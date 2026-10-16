# Daily Motivation Email Automation

A Python project that automatically sends daily motivational emails to configured recipients through Gmail. It combines date-based quote selection, HTML email generation, JSON-based content management, and scheduled cloud execution using GitHub Actions.

The project delivers a small dose of motivation each day while demonstrating practical Python automation, email integration, configuration management, and scheduled workflow execution.

## Features

- **240 motivational entries:** Eight categories covering self-learning, workouts and health, study and focus, planning and goals, life and happiness, resilience and confidence, habits and productivity, and relationships and kindness.
- **Date-based quote selection:** Selects an entry based on the date, so repeated runs on the same date select the same entry.
- **HTML email generation:** Generates a formatted email containing the date, quote, and supporting content.
- **Plain-text alternative:** Provides a text-only version for email clients that do not display HTML.
- **Multiple recipients:** Loads recipient addresses from a JSON configuration file and sends emails individually.
- **Gmail SMTP integration:** Sends emails securely through Gmail's SMTP server using TLS.
- **Environment-based credentials:** Uses environment variables to provide Gmail credentials securely.
- **Content validation:** Checks that the quotes file contains valid entries with the required fields.
- **Daily cloud scheduling:** Uses GitHub Actions to schedule automated email delivery without requiring a personal computer to remain switched on.
- **Duplicate-send prevention:** Records the last successfully processed date and skips subsequent runs on the same date.
- **Failure handling:** Reports individual delivery failures and avoids recording the date as successfully processed if any recipient fails.

## Technologies Used

- Python
- JSON
- `smtplib`
- `email.message`
- HTML
- `python-dotenv`
- Gmail SMTP
- Git and GitHub
- GitHub Actions

## Project Structure

```text
daily-motivation-email-automation/
├── .github/
│   └── workflows/
│       └── daily-motivation.yml
├── src/
│   ├── main.py
│   ├── email_sender.py
│   └── content_manager.py
├── data/
│   ├── quotes.json
│   ├── recipients.example.json
│   ├── recipients.json          # Local configuration; ignored by Git
│   └── last_sent_date.txt       # Tracks the last processed date
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── test_content.py
```

**Note:** The local `.env` file contains Gmail credentials and is intentionally excluded from version control.

The actual `data/recipients.json` file is also excluded because it contains private recipient addresses.

## How It Works

1. GitHub Actions starts the workflow according to its daily schedule.
2. The workflow checks out the repository and sets up Python.
3. The required dependencies are installed.
4. Recipient addresses are loaded from the `RECIPIENTS_JSON` GitHub Actions secret.
5. The application checks `data/last_sent_date.txt` to determine whether the current date has already been processed.
6. If the date has already been processed, the application exits without sending duplicate emails.
7. Otherwise, `content_manager.py` loads and validates the motivational entries and selects the entry corresponding to the current date.
8. `main.py` prepares the email subject, plain-text message, and HTML content.
9. `email_sender.py` connects to Gmail SMTP using the configured credentials and sends an email to each recipient.
10. If all recipients are processed successfully, the application records the date in `data/last_sent_date.txt`.
11. GitHub Actions commits the updated date file to the repository so subsequent workflow runs can recognize the completed date.

### Quote Selection

Quote selection is date-based rather than random.

Repeated runs on the same date select the same entry. With 240 entries and an unchanged quotes file, the selection cycles through the list after all entries have been traversed.

### Duplicate-Send Prevention

The application checks the last processed date before sending emails.

After all recipient sends complete successfully, the application records the date. Subsequent runs on the same date skip email delivery.

This mechanism helps prevent unnecessary repeat sends. However, it does not guarantee exactly-once delivery if a workflow fails after some emails have been sent but before the date record is saved.

## Prerequisites

### For Local Execution

- Python installed on your computer.
- A Gmail account.
- Google 2-Step Verification enabled.
- A Gmail App Password for SMTP access.
- Email addresses for recipients who have agreed to receive the messages.

### For GitHub Actions

- A GitHub repository.
- GitHub Actions enabled.
- The required credentials and recipient configuration stored as repository secrets.

## Local Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kommeranithinreddy/daily-motivation-email-automation.git
cd daily-motivation-email-automation
```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Email Credentials

Create a file named `.env` in the project root, using `.env.example` as a template.

Add your own credentials:

```text
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
```

Use a Gmail App Password rather than your regular Google account password.

Keep `.env` private and never commit it to Git.

### 4. Configure Recipients

Copy `data/recipients.example.json` to `data/recipients.json`.

Replace the example addresses with the intended recipients:

```json
[
    "recipient1@example.com",
    "recipient2@example.com"
]
```

Save the file as `data/recipients.json`.

This local configuration file is excluded from Git to protect recipient privacy.

## Running Locally

Run the application from the project root:

```bash
python -m src.main
```

The program selects the day's quote, generates the email, and attempts to send it to each configured recipient.

Check the terminal output and recipient inboxes to verify the result.

The application records the date after all recipient sends complete successfully. If the application is run again on the same date after successful processing, it skips sending another set of emails.

## GitHub Actions Automation

The project uses GitHub Actions to run the application automatically every day at **9:00 AM India Standard Time (IST)**.

The workflow uses a standard GitHub-hosted Ubuntu runner, so your personal computer does not need to be switched on.

### Required Repository Secrets

Configure the following secrets under:

**Repository → Settings → Secrets and variables → Actions**

| Secret | Purpose |
|---|---|
| `EMAIL_ADDRESS` | Gmail address used to send emails |
| `EMAIL_APP_PASSWORD` | Gmail App Password used for SMTP authentication |
| `RECIPIENTS_JSON` | JSON array containing recipient email addresses |

Example structure for `RECIPIENTS_JSON`:

```json
[
    "recipient1@example.com",
    "recipient2@example.com"
]
```

Use your actual recipient addresses in GitHub Secrets, not in the repository.

Never share or commit the values of these secrets.

### Running the Workflow Manually

To start the workflow manually:

1. Open the repository on GitHub.
2. Select the **Actions** tab.
3. Open **Daily Motivation Email**.
4. Click **Run workflow**.
5. Select the `main` branch and confirm.

**Important:** A manual run can send real emails. The application skips sending if the current date has already been recorded as processed.

### Monitoring Workflow Runs

Open the **Actions** tab to inspect workflow runs, view logs, and investigate failures.

The workflow commits the updated `data/last_sent_date.txt` file after successful email processing.

Scheduled execution and email delivery depend on GitHub Actions availability, correct repository configuration, valid secrets, and successful Gmail SMTP authentication.

### Workflow Permissions

The workflow requires permission to update `data/last_sent_date.txt` in the repository.

The workflow uses the `contents: write` permission to commit this date record after successful email processing.

## Testing

Run the content validation test from the project root:

```bash
python test_content.py
```

This checks the quote data and its compatibility with the content manager.

The email workflow can also be inspected through GitHub Actions, where each run provides logs for troubleshooting.

Manual workflow runs should be performed carefully because they may send real emails.

## Security and Privacy

- `.env` contains credentials and must remain local.
- `data/recipients.json` contains actual recipient addresses and must remain local.
- `.env.example` and `data/recipients.example.json` contain placeholders for setup.
- GitHub Actions secrets provide credentials and recipient configuration to the cloud workflow.
- The `.gitignore` file excludes private configuration files and Python cache files.
- Never print or commit credentials, Gmail App Passwords, or actual recipient addresses.
- Only send emails to people who have agreed to receive them.
- If the recipient list grows, provide a clear way for recipients to opt out.

Before pushing changes, check the staged files:

```bash
git status
```

Confirm that `.env` and `data/recipients.json` are not included.

## Automation Status

| Component | Status |
|---|---|
| Python email application | Implemented |
| Gmail SMTP delivery | Implemented |
| HTML and plain-text email generation | Implemented |
| JSON-based content management | Implemented |
| GitHub Actions workflow | Implemented |
| Daily schedule at 9:00 AM IST | Configured |
| Manual workflow execution | Tested successfully |
| Date-based duplicate prevention | Tested successfully |
| Full scheduled cloud delivery | Requires continued verification |

The latest successful workflow test verified that the application recognizes an already-processed date and skips sending duplicate emails.

A successful run that skips email delivery does not, by itself, verify a fresh cloud email send. Continued verification of scheduled runs is necessary before relying exclusively on the cloud automation.

## Possible Future Improvements

- Refine the email subject and visual design.
- Improve handling of partial delivery failures.
- Add automated tests for email construction without sending real messages.
- Add delivery tracking at the individual-recipient level.
- Expand or refine the motivational content over time.
