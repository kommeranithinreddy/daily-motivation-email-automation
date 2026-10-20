import json
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape
from pathlib import Path

from src.content_manager import get_daily_quote
from src.email_sender import send_email


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RECIPIENTS_FILE = PROJECT_ROOT / "data" / "recipients.json"
LAST_SENT_FILE = PROJECT_ROOT / "data" / "last_sent_date.txt"


def load_recipients():
    """Load and validate the recipient list."""

    with RECIPIENTS_FILE.open("r", encoding="utf-8") as file:
        recipients = json.load(file)

    if not isinstance(recipients, list):
        raise ValueError("The recipients file must contain a JSON list.")

    recipients = [
        email.strip()
        for email in recipients
        if isinstance(email, str) and email.strip()
    ]

    # Remove duplicate addresses, ignoring letter case.
    recipients = list(dict.fromkeys(
        email.lower() for email in recipients
    ))

    if not recipients:
        raise ValueError("No valid recipients were configured.")

    return recipients


def create_newsletter(quote, today):
    """Create a minimal, elegant motivational newsletter."""

    quote_text = escape(quote["quote"])
    author = escape(quote["author"])
    thought = escape(quote["message"])

    date_text = today.strftime("%B %d, %Y")
    date_upper = escape(date_text.upper())

    subject = f"Your Daily Motivation — {date_text}"

    plain_text = (
        f"DAILY MOTIVATION | {date_text}\n\n"
        f'"{quote["quote"]}"\n'
        f"— {quote['author']}\n\n"
        f"{quote['message']}\n"
    )

    html_body = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Motivation</title>
</head>

<body style="margin:0;padding:24px 10px;background-color:#f3f1ed;
             font-family:Georgia,'Times New Roman',serif;color:#172522;">

    <div style="max-width:680px;margin:0 auto;background-color:#fffaf1;
                border:1px solid #eadbc1;border-radius:12px;overflow:hidden;">

        <!-- Header -->
        <div style="padding:38px 28px 30px;text-align:center;
                    background-color:#f8ead5;
                    border-bottom:3px solid #d3ad68;">

            <p style="margin:0 0 12px;font-family:Arial,sans-serif;
                      font-size:11px;letter-spacing:4px;color:#9b702c;">
                DAILY MOTIVATION
            </p>

            <p style="margin:0;font-family:Arial,sans-serif;
                      font-size:12px;letter-spacing:3px;color:#75644f;">
                {date_upper}
            </p>

        </div>

        <!-- Motivational Quote -->
        <div style="padding:38px 28px 28px;text-align:center;">

            <p style="margin:0;font-size:27px;line-height:1.55;
                      font-style:italic;color:#172522;
                      overflow-wrap:anywhere;">
                &ldquo;{quote_text}&rdquo;
            </p>

            <p style="margin:22px 0 0;font-size:17px;line-height:1.5;
                      color:#766653;overflow-wrap:anywhere;">
                &mdash; {author}
            </p>

        </div>

        <!-- Daily Reflection -->
        <div style="margin:0 32px 34px;text-align:center;">

            <div style="width:44px;height:1px;margin:0 auto 22px;
                        background-color:#c99a43;"></div>

            <p style="margin:0;font-size:16px;line-height:1.8;
                      font-style:italic;color:#756653;
                      overflow-wrap:anywhere;">
                {thought}
            </p>

        </div>

    </div>

</body>
</html>
"""

    return subject, plain_text, html_body
def already_processed_today(today):
    """Check whether today's emails have already been processed."""

    if not LAST_SENT_FILE.exists():
        return False

    last_sent = LAST_SENT_FILE.read_text(encoding="utf-8").strip()
    return last_sent == today.isoformat()

def record_processed_today(today):
    """Record the date after all email attempts succeed."""
    LAST_SENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    LAST_SENT_FILE.write_text(today.isoformat(), encoding="utf-8")

def main():
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()

    if already_processed_today(today):
        print(f"Today's emails have already been processed: {today}.")
        return

    quote = get_daily_quote()
    subject, plain_text, html_body = create_newsletter(quote, today)
    recipients = load_recipients()

    failed_recipients = []

    for recipient in recipients:
        try:
            send_email(
                recipient=recipient,
                subject=subject,
                body=plain_text,
                html_body=html_body,
            )
            print(f"Successfully sent email to {recipient}.")
        except Exception as error:
            failed_recipients.append(recipient)
            print(f"Could not send to {recipient}: {error}")

    if failed_recipients:
        raise RuntimeError(
            f"Email delivery failed for {len(failed_recipients)} recipient(s). "
            "Today's date was not recorded."
        )

    record_processed_today(today)
    print(f"Successfully processed all {len(recipients)} recipients.")


if __name__ == "__main__":
    main()
