from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from database import insert_event
from cloud_storage import upload_database
from cloud_logging import cloud_log
from report import generate_report
from email_alert import send_email

from datetime import datetime
import time
import os

# ==============================
# Configuration
# ==============================

HONEYPOT_FOLDER = "honeypot"

TIME_WINDOW = 10
MODIFIED_THRESHOLD = 10
DELETED_THRESHOLD = 5

modified_files = []
deleted_files = []

last_modify_alert = 0
last_delete_alert = 0


# ==============================
# Helper Functions
# ==============================

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_event(event_type, severity, filename):

    insert_event(
        current_time(),
        event_type,
        severity,
        filename
    )

    print(f"[{severity}] {event_type} -> {filename}")

    # Cloud Logging (Optional)
    cloud_log(
        severity.upper(),
        f"{event_type}: {filename}"
    )


def log_incident(message):

    insert_event(
        current_time(),
        "Possible Ransomware Attack",
        "Critical",
        message
    )

    print("\n" + "=" * 60)
    print("🚨 POSSIBLE RANSOMWARE DETECTED 🚨")
    print(message)
    print("=" * 60 + "\n")

    # --------------------------
    # Generate PDF Report
    # --------------------------

    report_path = generate_report(message)

    print(f"📄 Report Saved : {report_path}")

    # --------------------------
    # Upload SQLite Database
    # --------------------------

    upload_database()

    # --------------------------
    # Google Cloud Logging
    # --------------------------

    cloud_log(
        "CRITICAL",
        f"Possible Ransomware Attack - {message}"
    )

    # --------------------------
    # Send Email Alert
    # --------------------------

    send_email(
        subject="🚨 Ransomware Alert Detected",
        body=f"""
Cloud-Based Ransomware Detection & Monitoring System

Severity : CRITICAL

Incident:
{message}

Detection Time:
{current_time()}

The detailed PDF incident report is attached.

This is an automated notification.
""",
        attachment=report_path
    )


# ==============================
# File Monitoring
# ==============================

class RansomwareHandler(FileSystemEventHandler):

    def clean_old_events(self):

        now = time.time()

        while modified_files and now - modified_files[0] > TIME_WINDOW:
            modified_files.pop(0)

        while deleted_files and now - deleted_files[0] > TIME_WINDOW:
            deleted_files.pop(0)

    # ---------------------------------

    def on_created(self, event):

        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)

        log_event(
            "File Created",
            "Low",
            filename
        )

    # ---------------------------------

    def on_modified(self, event):

        global last_modify_alert

        if event.is_directory:
            return

        modified_files.append(time.time())

        self.clean_old_events()

        filename = os.path.basename(event.src_path)

        severity = "Medium"

        if filename.endswith((".locked", ".encrypted", ".crypt")):
            severity = "Critical"

        elif len(modified_files) >= MODIFIED_THRESHOLD:

            severity = "High"

            now = time.time()

            if now - last_modify_alert > TIME_WINDOW:

                log_incident(
                    f"{len(modified_files)} files modified within {TIME_WINDOW} seconds"
                )

                last_modify_alert = now

        log_event(
            "File Modified",
            severity,
            filename
        )

    # ---------------------------------

    def on_deleted(self, event):

        global last_delete_alert

        if event.is_directory:
            return

        deleted_files.append(time.time())

        self.clean_old_events()

        filename = os.path.basename(event.src_path)

        severity = "High"

        if len(deleted_files) >= DELETED_THRESHOLD:

            severity = "Critical"

            now = time.time()

            if now - last_delete_alert > TIME_WINDOW:

                log_incident(
                    f"{len(deleted_files)} files deleted within {TIME_WINDOW} seconds"
                )

                last_delete_alert = now

        log_event(
            "File Deleted",
            severity,
            filename
        )

    # ---------------------------------

    def on_moved(self, event):

        if event.is_directory:
            return

        filename = os.path.basename(event.dest_path)

        severity = "Medium"

        if filename.endswith((".locked", ".encrypted", ".crypt")):

            severity = "Critical"

            log_incident(
                f"Encrypted extension detected: {filename}"
            )

        log_event(
            "File Renamed",
            severity,
            filename
        )


# ==============================
# Start Monitoring
# ==============================

if not os.path.exists(HONEYPOT_FOLDER):
    os.makedirs(HONEYPOT_FOLDER)

observer = Observer()

observer.schedule(
    RansomwareHandler(),
    path=HONEYPOT_FOLDER,
    recursive=True
)

observer.start()

print("=" * 60)
print("🛡 Cloud-Based Ransomware Detection Engine Started")
print("=" * 60)
print(f"Monitoring Folder : {HONEYPOT_FOLDER}")
print(f"Time Window       : {TIME_WINDOW} seconds")
print(f"Modify Threshold  : {MODIFIED_THRESHOLD}")
print(f"Delete Threshold  : {DELETED_THRESHOLD}")
print("=" * 60)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping monitor...")
    observer.stop()

observer.join()