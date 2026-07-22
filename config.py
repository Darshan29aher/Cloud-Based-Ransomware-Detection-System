from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# ==========================
# Google Cloud Configuration
# ==========================

GCP_ENABLED = False

PROJECT_ID = ""
BUCKET_NAME = ""
SERVICE_ACCOUNT = ""

ENABLE_CLOUD_STORAGE = True
ENABLE_CLOUD_LOGGING = True

# ==========================
# Email Configuration
# ==========================

ENABLE_EMAIL_ALERTS = (
    os.getenv("ENABLE_EMAIL_ALERTS", "False").lower() == "true"
)

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")