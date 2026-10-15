from src.content_manager import get_daily_quote

quote = get_daily_quote()

print("Quote:", quote["quote"])
print("Author:", quote["author"])
print("Message:", quote["message"])