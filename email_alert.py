import os
import smtplib

from email.message import EmailMessage
from config import *


def send_email(subject, body, attachment=None):

    if not ENABLE_EMAIL_ALERTS:
        print("⚪ Email Alerts Disabled")
        return

    try:

        msg = EmailMessage()

        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        msg.set_content(body)

        if attachment and os.path.exists(attachment):

            with open(attachment, "rb") as f:
                data = f.read()

            msg.add_attachment(
                data,
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(attachment)
            )

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:

            smtp.starttls()

            smtp.login(
                EMAIL_SENDER,
                EMAIL_PASSWORD
            )

            smtp.send_message(msg)

        print("📧 Email Alert Sent Successfully")

    except Exception as e:

        print("❌ Email Error:", e)
