import os
import sys

import httpx


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        sys.exit("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variable.")

    message = "Hourly alert: your scheduled GitHub Actions job is running."
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = httpx.post(
        url,
        json={"chat_id": chat_id, "text": message},
        timeout=20.0,
    )
    response.raise_for_status()
    result = response.json()
    if not result.get("ok"):
        sys.exit(f"Telegram API returned an error: {result}")

    print("Telegram alert sent successfully.")


if __name__ == "__main__":
    main()