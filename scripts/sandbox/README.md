# Sandbox & Experimental Scripts

This directory is a scratchpad ("rough book") for exploratory scripts, spikes, and integration prototypes.

## Running Scripts

Activate your virtual environment and execute the script from the repository root:

```powershell
# From the repository root
python scripts/sandbox/test_telegram_receive.py
```

## Available Scripts

- **`send_telegram_alert.py`**: A one-shot alert script that sends a message or notification directly to your Telegram chat and exits in under 1 second. Can be scheduled hourly via Windows Task Scheduler or cron.
- **`test_telegram_receive.py`**: A 2-way listener bot to test receiving incoming messages and commands (`/start`, `/ping`) using long polling.
