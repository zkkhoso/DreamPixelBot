import os
import requests
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

CRIC_API_KEY = os.getenv("CRIC_API_KEY", "")
BASE_URL = "https://api.cricapi.com/v1/currentMatches?apikey={}&offset=0"

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    """Render the single-page application."""
    return render_template("index.html")


@app.route("/api/scores")
def scores():
    """Proxy endpoint that fetches live scores from CricAPI.

    Having a backend proxy keeps our API key private and allows us to bypass CORS restrictions.
    """
    if not CRIC_API_KEY:
        return jsonify({"error": "CRIC_API_KEY missing"}), 500

    try:
        resp = requests.get(BASE_URL.format(CRIC_API_KEY), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return jsonify(data)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    # Allow the port to be overridden by an env var (useful for Heroku / Render).
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)