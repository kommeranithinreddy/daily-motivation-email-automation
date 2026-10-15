import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUOTES_FILE = PROJECT_ROOT / "data" / "quotes.json"


def load_quotes():
    """Load motivational quotes from the JSON file."""

    with QUOTES_FILE.open("r", encoding="utf-8") as file:
        quotes = json.load(file)

    if not isinstance(quotes, list) or not quotes:
        raise ValueError("The quotes file must contain a non-empty list.")

    for quote in quotes:
        if not isinstance(quote, dict):
            raise ValueError("Each quote must be a JSON object.")

        for field in ("quote", "author", "message"):
            if not isinstance(quote.get(field), str) or not quote[field].strip():
                raise ValueError(f"Each quote must have a non-empty '{field}'.")

    return quotes


def get_daily_quote():
    """Select a quote deterministically for the current date."""

    from datetime import date

    quotes = load_quotes()
    day_number = date.today().toordinal()
    index = day_number % len(quotes)

    return quotes[index]