from config import *

try:
    import google.cloud.logging

    if GCP_ENABLED and ENABLE_CLOUD_LOGGING:
        client = google.cloud.logging.Client.from_service_account_json(
            SERVICE_ACCOUNT
        )

        client.setup_logging()

        logger = client.logger("Ransomware-Detection")

    else:
        logger = None

except Exception:
    logger = None


def cloud_log(severity, message):

    if logger is None:
        print("⚪ Cloud Logging Disabled")
        return

    try:
        logger.log_text(
            message,
            severity=severity
        )

        print("☁ Logged to Google Cloud")

    except Exception as e:
        print("Cloud Logging Failed")
        print(e)
