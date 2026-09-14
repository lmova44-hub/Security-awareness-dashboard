from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# ============================================================
# Environment variables
# ============================================================

RESULTS_API_URL = os.environ.get("RESULTS_API_URL")
RESULTS_API_TOKEN = os.environ.get("RESULTS_API_TOKEN")


# ============================================================
# Get campaign statistics from the safe results API
# ============================================================

def get_campaign_stats():
    stats = {
        "sent": 0,
        "opened": 0,
        "clicked": 0,
        "submitted": 0
    }

    # If the results API is not configured, return zero values.
    if not RESULTS_API_URL:
        return stats

    try:
        response = requests.get(
            RESULTS_API_URL,
            headers={
                "Authorization": f"Bearer {RESULTS_API_TOKEN}"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        stats["sent"] = data.get("sent", 0)
        stats["opened"] = data.get("opened", 0)
        stats["clicked"] = data.get("clicked", 0)
        stats["submitted"] = data.get("submitted", 0)

    except (requests.RequestException, ValueError, TypeError):
        # Keep the dashboard available even if the backend
        # is temporarily unavailable.
        pass

    return stats


# ============================================================
# Dashboard
# ============================================================

@app.route("/")
def dashboard():
    stats = get_campaign_stats()

    return render_template(
        "dashboard.html",
        stats=stats
    )


# ============================================================
# Campaigns
# ============================================================

@app.route("/campaigns")
def campaigns():
    return render_template("campaigns.html")


# ============================================================
# Results
# ============================================================

@app.route("/results")
def results():
    stats = get_campaign_stats()

    return render_template(
        "results.html",
        stats=stats
    )


# ============================================================
# Activity Logs
# ============================================================

@app.route("/logs")
def logs():
    return render_template("logs.html")


# ============================================================
# Training
# ============================================================

@app.route("/training")
def training():
    return render_template("training.html")


# ============================================================
# Local development
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
