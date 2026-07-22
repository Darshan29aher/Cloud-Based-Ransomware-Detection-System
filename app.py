from flask import (
    Flask,
    render_template,
    send_from_directory,
    abort
)

import sqlite3
import os
from collections import Counter

from config import (
    ENABLE_CLOUD_STORAGE,
    ENABLE_CLOUD_LOGGING,
    ENABLE_EMAIL_ALERTS
)

app = Flask(__name__)

DATABASE = "database/ransomware.db"
REPORT_FOLDER = "reports"


# ----------------------------------------
# Database Connection
# ----------------------------------------

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------------------
# Dashboard
# ----------------------------------------

@app.route("/")
def dashboard():

    conn = get_connection()

    total_events = conn.execute(
        "SELECT COUNT(*) FROM events"
    ).fetchone()[0]

    threats = conn.execute(
        """
        SELECT COUNT(*)
        FROM events
        WHERE severity IN ('High','Critical')
        """
    ).fetchone()[0]

    last_alert = conn.execute(
        """
        SELECT event_type
        FROM events
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    last_alert = last_alert["event_type"] if last_alert else "No Alerts"

    recent_events = conn.execute(
        """
        SELECT *
        FROM events
        ORDER BY id DESC
        LIMIT 15
        """
    ).fetchall()

    severity_rows = conn.execute(
        "SELECT severity FROM events"
    ).fetchall()

    counter = Counter()

    for row in severity_rows:
        counter[row["severity"]] += 1

    chart_labels = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    chart_values = [
        counter["Low"],
        counter["Medium"],
        counter["High"],
        counter["Critical"]
    ]

    if counter["Critical"] > 0:
        status = "Under Attack"
    elif counter["High"] > 0:
        status = "Warning"
    else:
        status = "Safe"

    conn.close()

    return render_template(
        "dashboard.html",
        total_events=total_events,
        threats=threats,
        last_alert=last_alert,
        recent_events=recent_events,
        status=status,
        chart_labels=chart_labels,
        chart_values=chart_values,
        cloud_storage=ENABLE_CLOUD_STORAGE,
        cloud_logging=ENABLE_CLOUD_LOGGING,
        email_alerts=ENABLE_EMAIL_ALERTS
    )


# ----------------------------------------
# Events Page
# ----------------------------------------

@app.route("/events")
def events():

    conn = get_connection()

    events = conn.execute(
        """
        SELECT *
        FROM events
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "events.html",
        events=events
    )


# ----------------------------------------
# Threats Page
# ----------------------------------------

@app.route("/threats")
def threats():

    conn = get_connection()

    threats = conn.execute(
        """
        SELECT *
        FROM events
        WHERE severity IN ('High','Critical')
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "threats.html",
        threats=threats
    )


# ----------------------------------------
# Reports Page
# ----------------------------------------

@app.route("/reports")
def reports():

    pdfs = []

    if os.path.exists(REPORT_FOLDER):

        pdfs = sorted(
            [
                f for f in os.listdir(REPORT_FOLDER)
                if f.lower().endswith(".pdf")
            ],
            reverse=True
        )

    return render_template(
        "reports.html",
        reports=pdfs
    )


# ----------------------------------------
# Download Report
# ----------------------------------------

@app.route("/download/<filename>")
def download(filename):

    if not filename.lower().endswith(".pdf"):
        abort(400)

    file_path = os.path.join(REPORT_FOLDER, filename)

    if not os.path.exists(file_path):
        abort(404)

    return send_from_directory(
        REPORT_FOLDER,
        filename,
        as_attachment=True
    )


# ----------------------------------------
# Settings Page
# ----------------------------------------

@app.route("/settings")
def settings():

    return render_template(
        "settings.html",
        cloud_storage=ENABLE_CLOUD_STORAGE,
        cloud_logging=ENABLE_CLOUD_LOGGING,
        email_alerts=ENABLE_EMAIL_ALERTS,
        database=DATABASE,
        report_folder=REPORT_FOLDER
    )


# ----------------------------------------
# Error Pages
# ----------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    return "<h2>404 - Page Not Found</h2>", 404


@app.errorhandler(400)
def bad_request(error):
    return "<h2>400 - Invalid Request</h2>", 400


# ----------------------------------------
# Run Flask
# ----------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )