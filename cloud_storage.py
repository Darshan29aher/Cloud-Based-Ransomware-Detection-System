from google.cloud import storage
from config import *

DATABASE_FILE = "database/ransomware.db"


def upload_database():

    if not GCP_ENABLED:
        print("⚪ Cloud Storage Disabled")
        return

    try:

        client = storage.Client.from_service_account_json(
            SERVICE_ACCOUNT
        )

        bucket = client.bucket(BUCKET_NAME)

        blob = bucket.blob("ransomware.db")

        blob.upload_from_filename(DATABASE_FILE)

        print("✅ Database uploaded successfully")

    except Exception as e:

        print("Cloud Upload Failed")

        print(e)