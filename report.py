from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

REPORT_FOLDER = "reports"


def generate_report(message):

    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"Incident_Report_{timestamp}.pdf"

    filepath = os.path.join(REPORT_FOLDER, filename)

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>Cloud-Based Ransomware Detection & Monitoring System</b>",
            styles["Title"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "<b>Severity:</b> CRITICAL",
            styles["Heading2"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "<b>Incident Details</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            message,
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "<b>Recommended Actions</b>",
            styles["Heading2"]
        )
    )

    recommendations = [
        "Disconnect the affected system from the network.",
        "Restore files from a secure backup.",
        "Run a complete antivirus and malware scan.",
        "Review all security and system logs.",
        "Investigate modified and deleted files.",
        "Reset passwords if compromise is suspected."
    ]

    for item in recommendations:
        story.append(
            Paragraph(f"• {item}", styles["Normal"])
        )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "Generated Automatically by Cloud-Based Ransomware Detection & Monitoring System",
            styles["Italic"]
        )
    )

    doc.build(story)

    print(f"📄 Incident Report Generated: {filepath}")

    return filepath
