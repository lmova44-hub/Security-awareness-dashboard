from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# ============================================================
# Environment variables
# ============================================================

GOPHISH_API_KEY = os.environ.get("GOPHISH_API_KEY")
GOPHISH_URL = os.environ.get("GOPHISH_URL", "https://20.230.166.202:3333")


# ============================================================
# Get campaign statistics directly from GoPhish
# ============================================================

def get_campaign_stats():
    stats = {
        "sent": 0,
        "opened": 0,
        "clicked": 0,
        "submitted": 0
    }

    # If GoPhish is not configured, return zero values.
    if not GOPHISH_API_KEY:
        return stats

    try:
        response = requests.get(
            f"{GOPHISH_URL}/api/campaigns/",
            headers={
                "Authorization": GOPHISH_API_KEY
            },
            timeout=10,
            verify=False
        )

        response.raise_for_status()

        campaigns = response.json()

        # Sum stats across all campaigns
        for campaign in campaigns:
            campaign_stats = campaign.get("stats", {})
            stats["sent"] += campaign_stats.get("sent", 0)
            stats["opened"] += campaign_stats.get("opened", 0)
            stats["clicked"] += campaign_stats.get("clicked", 0)
            stats["submitted"] += campaign_stats.get("submitted_data", 0)

    except (requests.RequestException, ValueError, TypeError):
        # Keep the dashboard available even if GoPhish
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
