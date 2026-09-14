from flask import Flask, render_template
import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GOPHISH_API_KEY = os.environ.get("GOPHISH_API_KEY")
GOPHISH_URL = "https://127.0.0.1:3333"

app = Flask(__name__)

headers = {
    "Authorization": GOPHISH_API_KEY
}

@app.route("/")
def dashboard():
    response = requests.get(
        f"{GOPHISH_URL}/api/campaigns/",
        headers=headers,
        verify=False
    )

    campaigns = response.json()

    stats = {
        "sent": 0,
        "opened": 0,
        "clicked": 0,
        "submitted": 0
    }

    if campaigns:
        campaign = campaigns[-1]

        stats["sent"] = campaign.get("stats", {}).get("sent", 0)
        stats["opened"] = campaign.get("stats", {}).get("opened", 0)
        stats["clicked"] = campaign.get("stats", {}).get("clicked", 0)
        stats["submitted"] = campaign.get("stats", {}).get("submitted_data", 0)

    return render_template("dashboard.html", stats=stats)



@app.route("/campaigns")
def campaigns():
    return render_template("campaigns.html")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/logs")
def logs():
    return render_template("logs.html")


@app.route("/training")
def training():
    return render_template("training.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
