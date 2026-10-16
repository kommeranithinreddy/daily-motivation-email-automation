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
    """Create the plain-text and HTML newsletter."""

    quote_text = escape(quote["quote"])
    author = escape(quote["author"])
    thought = escape(quote["message"])

    date_text = today.strftime("%B %d, %Y")
    date_upper = escape(date_text.upper())

    subject = f"Your Daily Motivation — {date_text}"

    plain_text = (
        "A LITTLE MOTIVATION FOR TODAY\n"
        f"{date_text}\n\n"
        "TODAY'S INSPIRATION\n\n"
        f'"{quote["quote"]}"\n'
        f"— {quote['author']}\n\n"
        "A THOUGHT FOR TODAY\n\n"
        f"{quote['message']}\n\n"
        "MAKE TODAY COUNT.\n\n"
        "A little inspiration, delivered to you every day.\n"
    )

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>A Little Motivation</title>
    </head>
    <body style="margin:0;padding:24px 10px;background-color:#f3f1ed;
                 font-family:Georgia,'Times New Roman',serif;color:#172522;">
        <div style="max-width:680px;margin:0 auto;background-color:#fffaf1;
                    border:1px solid #eadbc1;border-radius:12px;overflow:hidden;">

            <div style="padding:38px 28px 30px;text-align:center;
                        background-color:#f8ead5;border-bottom:3px solid #d3ad68;">
                <p style="margin:0 0 12px;font-family:Arial,sans-serif;
                          font-size:11px;letter-spacing:4px;color:#9b702c;">
                    A DAILY MOMENT OF INSPIRATION
                </p>
                <h1 style="margin:0;font-size:34px;line-height:1.2;
                           font-weight:normal;color:#172522;">
                    A Little Motivation<br>for Today
                </h1>
                <p style="margin:18px 0 0;font-family:Arial,sans-serif;
                          font-size:12px;letter-spacing:4px;color:#75644f;">
                    {date_upper}
                </p>
                <p style="margin:22px 0 0;font-size:13px;font-style:italic;
                          color:#75644f;">
                    Same small steps, brighter days.
                </p>
            </div>

            <div style="padding:38px 28px 30px;text-align:center;">
                <p style="margin:0 0 22px;font-family:Arial,sans-serif;
                          font-size:12px;font-weight:bold;letter-spacing:4px;
                          color:#8e692f;">
                    TODAY'S INSPIRATION
                </p>
                <div style="width:65px;height:2px;margin:0 auto 28px;
                            background-color:#c99a43;"></div>
                <p style="margin:0;font-size:27px;line-height:1.55;
                          font-style:italic;overflow-wrap:anywhere;">
                    &ldquo;{quote_text}&rdquo;
                </p>
                <p style="margin:22px 0 0;font-size:17px;line-height:1.5;
                          color:#766653;">
                    &mdash; {author}
                </p>
            </div>

            <div style="margin:0 22px;padding:25px 22px;
                        background-color:#f8eddd;border-left:3px solid #c99a43;
                        border-radius:6px;">
                <p style="margin:0 0 15px;font-family:Arial,sans-serif;
                          font-size:12px;font-weight:bold;letter-spacing:3px;
                          color:#9b702c;">
                    A THOUGHT FOR TODAY
                </p>
                <p style="margin:0;font-size:17px;line-height:1.8;
                          color:#28352f;overflow-wrap:anywhere;">
                    {thought}
                </p>
            </div>

            <div style="padding:30px 24px;text-align:center;">
                <div style="width:48px;height:2px;margin:0 auto 20px;
                            background-color:#c99a43;"></div>
                <p style="margin:0;font-size:17px;letter-spacing:3px;
                          color:#9b702c;">
                    MAKE TODAY COUNT.
                </p>
            </div>

            <div style="margin:0 22px;padding:20px 8px 24px;
                        border-top:1px solid #e7d7bd;text-align:center;">
                <p style="margin:0;font-size:14px;line-height:1.8;
                          color:#756653;">
                    A little inspiration, delivered to you every day.
                </p>
                <p style="margin:12px 0 0;font-family:Arial,sans-serif;
                          font-size:10px;letter-spacing:2px;line-height:2;
                          color:#8e795e;">
                    STAY POSITIVE &nbsp;|&nbsp; STAY CONSISTENT &nbsp;|&nbsp;
                    KEEP GROWING
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
