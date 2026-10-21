<div align="center">

# Daily Motivation Email Automation

**A scheduled, configuration-driven email automation system built with
Python, Gmail SMTP, GitHub Actions, and secure repository secrets.**

Deliver a daily motivational quote and reflection to a configurable list
of recipients---without keeping a personal computer running.

</div>

------------------------------------------------------------------------

## Overview

Daily Motivation Email Automation is a Python application that selects a
motivational entry based on the current date, builds an HTML email with
a plain-text alternative, and sends it to configured recipients through
Gmail SMTP.

The project brings together content management, email composition,
credential handling, delivery safeguards, and cloud-based execution.
GitHub Actions provides the execution environment, while a
processing-date record helps prevent repeated sends for the same India
Standard Time (IST) date.

Motivational content is stored separately from application logic, local
configuration files are excluded from version control, and cloud
credentials and recipient configuration are supplied through GitHub
Actions repository secrets.

## Key Features

-   **240 motivational entries** organized across eight themes:
    self-learning, workouts and health, study and focus, planning and
    goals, life and happiness, resilience and confidence, habits and
    productivity, and relationships and kindness.
-   **Date-based content selection:** repeated runs on the same date
    select the same entry while the content file remains unchanged.
-   **Responsive HTML email:** a minimal cream-and-gold design with a
    quote, author attribution, and a short reflection.
-   **Plain-text fallback** for email clients that do not display HTML.
-   **Multiple recipients** with individual email delivery and
    case-insensitive duplicate-recipient removal.
-   **Gmail SMTP integration** using TLS and a Gmail App Password.
-   **Environment-based local configuration** and GitHub Actions secrets
    for cloud execution.
-   **Content validation** for motivational entries and required fields.
-   **Cloud scheduling** through GitHub Actions, with a configured
    `cron-job.org` workflow-dispatch trigger.
-   **IST-aware processing date** using the `Asia/Kolkata` timezone.
-   **Duplicate-send prevention** based on the last successfully
    processed date.
-   **Delivery failure handling:** raises an error when one or more
    recipient sends fail and avoids recording the date as successfully
    processed in that case.
-   **Workflow logs** for cloud-run inspection and troubleshooting.

## Architecture

``` text
                         ┌──────────────────────────┐
                         │ Motivational content     │
                         │ data/quotes.json         │
                         └────────────┬─────────────┘
                                      │
                                      ▼
┌───────────────────┐     ┌──────────────────────────┐
│ GitHub Actions    │────▶│ Python application       │
│ scheduled/manual  │     │ src/main.py              │
└───────────────────┘     └────────────┬─────────────┘
                                       │
                            ┌──────────▼───────────┐
                            │ Content manager      │
                            │ Validate and select  │
                            │ the day's entry      │
                            └──────────┬───────────┘
                                       │
                            ┌──────────▼───────────┐
                            │ Email composition    │
                            │ HTML + plain text    │
                            └──────────┬───────────┘
                                       │
                            ┌──────────▼───────────┐
                            │ Gmail SMTP           │
                            │ Send to recipients   │
                            └──────────┬───────────┘
                                       │
                            ┌──────────▼───────────┐
                            │ Processing date      │
                            │ recorded on success  │
                            └──────────────────────┘

Cloud configuration:
GitHub Actions repository secrets provide sender credentials
and the recipient list. cron-job.org is configured to dispatch
the workflow through GitHub's workflow-dispatch endpoint.
```

### Execution flow

1.  The GitHub Actions workflow starts on its configured schedule or
    through a manual dispatch.
2.  The workflow checks out the repository, configures Python, and
    installs dependencies.
3.  The cloud workflow supplies sender credentials and the recipient
    list from GitHub Actions repository secrets.
4.  The application calculates the current date in the `Asia/Kolkata`
    timezone.
5.  The duplicate-send guard checks the stored processing date. If the
    current date has already been recorded, the application skips
    delivery.
6.  The content manager validates `data/quotes.json` and selects the
    entry for the current date.
7.  The application creates the subject, plain-text body, and HTML body.
8.  The email sender connects to Gmail SMTP and attempts delivery to
    each configured recipient.
9.  If any delivery fails, the application reports the failure and does
    not mark the date as successfully processed.
10. If all recipient sends complete successfully, the application
    records the date.
11. GitHub Actions commits the updated processing-date file so
    subsequent runs can recognize the completed date.

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Content and configuration | JSON |
| Email delivery | Gmail SMTP, `smtplib`, `email.message` |
| Email presentation | HTML and plain text |
| Local environment configuration | `python-dotenv` |
| Cloud execution | GitHub Actions |
| External workflow dispatch | cron-job.org |
| Source control | Git and GitHub |

## Repository Structure

``` text
daily-motivation-email-automation/
├── .github/
│   └── workflows/
│       ├── daily-motivation.yml
│       └── scheduler-test.yml
├── src/
│   ├── main.py
│   ├── email_sender.py
│   └── content_manager.py
├── data/
│   ├── quotes.json
│   ├── recipients.example.json
│   ├── recipients.json          # Local-only; excluded from Git
│   └── last_sent_date.txt       # Runtime state; updated by workflow
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── test_content.py
```

**Configuration and runtime files:** The local `.env` file contains
sender credentials and is excluded from Git. The local
`data/recipients.json` file is also excluded from Git. Cloud execution
uses the `RECIPIENTS_JSON` repository secret instead. The workflow
updates `data/last_sent_date.txt` after successful processing.

The `scheduler-test.yml` workflow is separate from the production
workflow. Review its current configuration before using it; do not
assume it has the same behavior as the production workflow.

## Prerequisites

### Local execution

-   Python installed on your computer.
-   Git, if you plan to clone the repository.
-   A Gmail account.
-   Google 2-Step Verification enabled.
-   A Gmail App Password for SMTP access.
-   Recipient addresses for people who have agreed to receive the
    messages.

### Cloud execution

-   A GitHub repository with GitHub Actions enabled.
-   The required repository secrets configured.
-   A Gmail account and valid App Password.
-   The production workflow's required repository permissions.
-   The configured `cron-job.org` job, if retaining the external
    workflow-dispatch trigger.

## Local Installation and Configuration

### 1. Clone the repository

``` bash
git clone https://github.com/kommeranithinreddy/daily-motivation-email-automation.git
cd daily-motivation-email-automation
```

### 2. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

### 3. Configure sender credentials

Create a `.env` file in the project root, using `.env.example` as a
template.

``` text
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
```

Use a Gmail App Password rather than your regular Google account
password. Keep `.env` private and never commit it to Git.

### 4. Configure local recipients

Copy `data/recipients.example.json` to `data/recipients.json`.

Replace the example values with the complete list of intended
recipients:

``` json
[
  "recipient1@example.com",
  "recipient2@example.com"
]
```

These are placeholder addresses. Save the file as
`data/recipients.json`. This file is excluded from Git to protect
recipient privacy.

### 5. Run the application

From the repository root:

``` bash
python -m src.main
```

The application selects the date's motivational entry, prepares the
email, and attempts to send it to each configured recipient. Review the
terminal output and recipient inboxes to confirm the result.

**Caution:** A local run can send real emails. If the current date has
already been recorded as processed, the duplicate-send guard may skip
delivery.

## Cloud Configuration: GitHub Actions

The production workflow is located at:

``` text
.github/workflows/daily-motivation.yml
```

It is configured for a daily run at **9:00 AM India Standard Time
(IST)** and supports manual execution through `workflow_dispatch`.

The workflow runs on a GitHub-hosted Ubuntu runner. Your personal
computer does not need to remain switched on.

### Required repository secrets

Open the repository on GitHub and navigate to:

**Settings → Secrets and variables → Actions**

Configure these repository secrets:

  -----------------------------------------------------------------------
  Secret                              Purpose
  ----------------------------------- -----------------------------------
  `EMAIL_ADDRESS`                     Gmail address used to send the
                                      emails

  `EMAIL_APP_PASSWORD`                Gmail App Password used for SMTP
                                      authentication

  `RECIPIENTS_JSON`                   JSON array containing the complete
                                      recipient list
  -----------------------------------------------------------------------

Example structure for `RECIPIENTS_JSON`:

``` json
[
  "recipient1@example.com",
  "recipient2@example.com"
]
```

Use actual recipient addresses only in the secret value. Never commit or
share secret values.

### Managing recipients

The cloud workflow reads recipients from `RECIPIENTS_JSON`. You do not
need to change the Python source code to add, remove, or replace
recipients.

1.  Open the GitHub repository.
2.  Go to **Settings → Secrets and variables → Actions**.
3.  Locate `RECIPIENTS_JSON` and select **Update**.
4.  Enter the **complete updated JSON array**, including every recipient
    who should continue receiving emails.
5.  Save the secret.

GitHub does not reveal the saved value of an existing secret. Keep a
secure copy of the intended complete recipient list so you can replace
the value accurately when needed.

-   **Add:** Include the new address and retain existing recipients.
-   **Remove:** Omit the address that should no longer receive emails.
-   **Replace:** Remove the old address and add the new one.

Secret changes apply to subsequent workflow executions. They do not
change sender credentials or the workflow schedule.

### Scheduling architecture

The production workflow has a native GitHub Actions schedule at 9:00 AM
IST. In addition, `cron-job.org` is configured to send a
workflow-dispatch request to GitHub at the configured time.

The external job uses GitHub's workflow-dispatch endpoint and a token
stored in its request configuration. Keep that token private and ensure
it has only the permissions required to dispatch the workflow.

Because both native scheduling and an external dispatch can initiate
workflow runs, inspect the current configuration before changing either
schedule. The date-based guard helps prevent repeated sends, but it is
not a guarantee of exactly-once delivery in every failure or concurrency
scenario.

If you decide to remove the external trigger or change the scheduling
arrangement, update the relevant configuration deliberately and verify
the resulting workflow behavior.

### Run the workflow manually

To dispatch the production workflow manually:

1.  Open the repository on GitHub.
2.  Select **Actions**.
3.  Open **Daily Motivation Email**.
4.  Select **Run workflow**.
5.  Choose the `main` branch and confirm.

**Important:** Manual execution can send real emails. The application
skips delivery if the current date is already recorded as processed. Do
not run the production workflow merely to test a configuration change
unless you understand the potential email impact.

### Monitor workflow runs

Use the repository's **Actions** tab to inspect workflow runs, logs, and
failures.

The workflow requires permission to update `data/last_sent_date.txt`.
Its `contents: write` permission supports committing this
processing-date record after successful email processing.

Successful workflow completion should be interpreted alongside the logs
and application behavior. A run that skips delivery because the date was
already processed does not, by itself, verify a fresh email send.

## Content Management

Motivational entries are stored in `data/quotes.json`.

The content manager validates the entries and selects one based on the
current date. The project currently documents 240 entries across eight
themes.

### Date-based selection

Selection is date-based rather than random. With an unchanged content
file, repeated runs on the same date select the same entry. The
selection cycles through the list after the entries have been traversed.

If the content list or its ordering changes, the selection associated
with a date may change as well.

### Email format

The email includes:

-   The date.
-   A motivational quote.
-   Author attribution.
-   A short reflection or message.

The message is generated in both HTML and plain-text formats so email
clients can use the format they support.

## Reliability and Delivery Semantics

### Duplicate-send prevention

The application calculates the processing date using the `Asia/Kolkata`
timezone and compares it with the stored date.

After all recipient sends complete successfully, it records the date.
Subsequent runs on the same date skip delivery.

This protects against many unnecessary repeat sends, but it does **not**
provide a strict exactly-once delivery guarantee.

For example, if some recipients receive an email and another recipient's
delivery fails, the date is not recorded as successfully processed. A
retry may therefore send the message again to recipients who already
received it.

The current mechanism tracks the processed date, not a durable success
record for each individual recipient.

### Failure handling

If a recipient send fails, the application collects the failure and
raises an error after attempting the recipient sends. The date is not
recorded as successfully processed when any recipient fails.

Check the workflow logs to identify the failure. Before manually
retrying, consider that some recipients may already have received the
email.

### Operational dependencies

Delivery depends on:

-   GitHub Actions availability and workflow configuration.
-   Valid repository secrets.
-   Valid Gmail SMTP credentials and account settings.
-   Network and SMTP availability.
-   Correct repository permissions for updating the processing-date
    file.
-   The configured schedule and, if used, the external workflow-dispatch
    job.

A scheduled trigger indicates that a run was requested; it does not by
itself guarantee that every email was delivered.

## Testing and Validation

### Validate motivational content

From the repository root, run:

``` bash
python test_content.py
```

This checks the quote data and its compatibility with the content
manager.

### Validate Python syntax

For example:

``` bash
python -m py_compile src/main.py
```

This checks syntax without running the email-sending application.

### Review changes before pushing

``` bash
git status
git diff --check
```

Confirm that private configuration files such as `.env` and
`data/recipients.json` are not staged for commit.

### Verify cloud behavior

Use the GitHub Actions logs to inspect workflow execution. To verify a
fresh delivery, confirm that the application actually attempted to send
emails; a run that skipped because the date was already processed is not
a fresh delivery test.

Avoid unnecessary production test runs because they can send real
emails.

## Security and Privacy

-   Keep `.env` local and excluded from version control.
-   Keep `data/recipients.json` local and excluded from version control.
-   Store cloud sender credentials and recipient configuration in GitHub
    Actions secrets.
-   Keep the `cron-job.org` dispatch token private.
-   Never print, commit, or share Gmail App Passwords, tokens, or actual
    recipient lists.
-   Grant workflow tokens only the permissions they require.
-   Send emails only to people who have agreed to receive them.
-   Provide a practical way for recipients to opt out as the recipient
    list grows.
-   Review `git status` before committing changes.

## Current Implementation Status

## Current Implementation Status

| Component | Status |
|---|---|
| Python email application | Implemented |
| Gmail SMTP delivery | Implemented |
| HTML and plain-text email generation | Implemented |
| JSON-based content management | Implemented |
| GitHub Actions production workflow | Configured |
| Daily schedule at 9:00 AM IST | Configured |
| `cron-job.org` workflow dispatch | Configured |
| Repository secrets | Configured |
| Date-based duplicate-send prevention | Implemented |
| Delivery failure handling | Implemented |
| Scheduled email delivery | Working |
| Recipient-list management through GitHub Secrets | Working |

The application has been deployed through GitHub Actions, and scheduled email delivery has been confirmed working. Recipient management through the `RECIPIENTS_JSON` repository secret is also working.

The automation should continue to be monitored through GitHub Actions logs to identify any future delivery failures.

This status describes the known configuration. Check the current
repository settings and recent workflow logs before relying on any item
as proof of a new successful delivery.
  
-----------------------------------------------------------------------

## Potential Future Improvements

-   Add automated tests for email composition without sending real
    messages.
-   Track delivery outcomes at the individual-recipient level.
-   Improve retry behavior for transient SMTP failures.
-   Add recipient opt-out management.
-   Expand or refine the motivational content over time.
-   Improve monitoring and notification for failed workflow runs.
-   Review the scheduling arrangement to minimize unnecessary or
    overlapping triggers.

## Contributing and Maintenance

For changes to the project:

1.  Make the smallest change that addresses the requirement.
2.  Run the relevant content or syntax checks.
3.  Review the diff and staged files.
4.  Confirm that private configuration files and secrets are not
    included.
5.  Commit and push the change.
6.  Inspect the relevant GitHub Actions run after deployment.

The application should be tested carefully when changes affect recipient
handling, email delivery, scheduling, date tracking, or repository
permissions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for the full license text.
