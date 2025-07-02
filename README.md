# Cricket Live Score Website

A simple Flask application that displays **live cricket scores** using the free [CricAPI](https://www.cricapi.com/).

## Features

- Lists all current international and domestic matches.
- Displays each team's scores, overs bowled, and match status.
- Automatically refreshes every minute (or on demand via the **Refresh** button).
- Backend proxy keeps your API key hidden and avoids CORS issues.

## Quick Start

```bash
# 1. Clone the repository (skip if you already have the code)
# git clone ...

cd /workspace  # or your project directory

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and paste your CRIC_API_KEY

# 5. Run the server
python app.py
```

Visit `http://localhost:5000` in your browser. The page will automatically load and refresh live scores.

## Deploying

Because it's a standard Flask app, you can deploy to any service that supports Python (Heroku, Render, Railway, etc.). Be sure to set the `CRIC_API_KEY` config variable in your hosting dashboard.

---
**Note**: This project lives alongside other Python code in the repository (a Telegram bot in `main.py`). Running the website and the bot simultaneously will require separate processes (or using something like `gunicorn` with multiple workers). For local development, simply start whichever service you need.