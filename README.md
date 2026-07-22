# 🛡 Cloud-Based Ransomware Detection & Monitoring System

A real-time ransomware detection and monitoring system built with **Python**, **Flask**, and **Google Cloud Platform (GCP)**. The application monitors a honeypot directory for suspicious file activities, detects potential ransomware behavior, logs security events, generates PDF incident reports, sends email alerts, and optionally uploads data to Google Cloud Storage.

---

## 📌 Features

- 🔍 Real-time file monitoring using Watchdog
- 🚨 Behavior-based ransomware detection
- 📊 Interactive Flask dashboard
- 📝 Event logging with SQLite
- 📄 Automatic PDF incident report generation
- 📧 Email alert notifications
- ☁ Google Cloud Storage integration
- 📜 Google Cloud Logging integration
- 📈 Threat visualization using Chart.js
- ⚙ Configurable detection thresholds

---

## 🏗 System Architecture

```
                 +-------------------------+
                 |   Honeypot Directory    |
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 | Watchdog File Monitor   |
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 | Ransomware Detection    |
                 +-----------+-------------+
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
   SQLite Database     PDF Incident      Email Alert
                         Report

          |
          v

 +-------------------+      +----------------------+
 | Google Cloud      | ---> | Cloud Storage        |
 | Logging           |      | Database Backup      |
 +-------------------+      +----------------------+

          |
          v

 +------------------------------+
 | Flask Web Dashboard          |
 | Dashboard • Events • Reports |
 | Threats • Settings           |
 +------------------------------+
```

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | Flask |
| Database | SQLite |
| Monitoring | Watchdog |
| Cloud Storage | Google Cloud Storage |
| Logging | Google Cloud Logging |
| Reports | ReportLab |
| Charts | Chart.js |
| Frontend | HTML, CSS, Bootstrap |

---

# 📂 Project Structure

```
Cloud-Based-Ransomware-Detection-System/
│
├── app.py
├── monitor.py
├── detector.py
├── database.py
├── config.py
├── cloud_storage.py
├── cloud_logging.py
├── email_alert.py
├── report.py
├── gcp.py
├── requirements.txt
├── .env.example
├── README.md
│
├── templates/
│
├── honeypot/
│   └── .gitkeep
│
├── reports/
│
└── database/
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/Darshan29aher/Cloud-Based-Ransomware-Detection-System.git

cd Cloud-Based-Ransomware-Detection-System
```

Create a virtual environment

```bash
python -m venv venv
```

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```cmd
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Configuration

Create a `.env` file using `.env.example`.

Example:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_BUCKET=your-bucket-name

ENABLE_EMAIL_ALERTS=True
ENABLE_CLOUD_STORAGE=True
ENABLE_CLOUD_LOGGING=True
```

---

# ☁ Google Cloud Setup

Configure Google Cloud authentication:

```bash
gcloud auth application-default login
```

or set a service account:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

Enable required APIs:

- Cloud Storage
- Cloud Logging

---

# 🚀 Running the Project

Start the Flask dashboard

```bash
python app.py
```

Start the monitoring engine

```bash
python monitor.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📊 Dashboard Modules

- 🏠 Dashboard
- 📋 Security Events
- 🚨 Threat Detection
- 📄 Incident Reports
- ⚙ Settings

---

# 🔍 Detection Logic

The system detects:

- Rapid file modifications
- Mass file deletion
- Suspicious encrypted extensions
- High-frequency filesystem activity

When suspicious behavior exceeds configured thresholds, the application:

- Logs the incident
- Generates a PDF report
- Sends an email notification
- Uploads the database to Google Cloud Storage (optional)
- Writes logs to Google Cloud Logging

---

# 📸 Screenshots

Add screenshots here after uploading them.

Example:

```
screenshots/
    dashboard.png
    events.png
    threats.png
    reports.png
    settings.png
```

Then embed them:

```markdown
## Dashboard

![Dashboard](screenshots/dashboard.png)

## Threats

![Threats](screenshots/threats.png)

## Reports

![Reports](screenshots/reports.png)
```

---

# 🔮 Future Enhancements

- Machine Learning-based ransomware detection
- Real-time WebSocket updates
- Slack/MS Teams notifications
- Docker deployment
- Kubernetes support
- SIEM integration
- Multi-user authentication
- REST API

---

# 👨‍💻 Author

**Darshan Aher**

Cybersecurity | Cloud Security | Google Cloud | AWS

GitHub:

https://github.com/Darshan29aher

---

# 📜 License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, consider giving it a star.
