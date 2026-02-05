# OS Performance Monitor 🚀

An intelligent, real-time operating system monitoring dashboard powered by Python, Flask, and Machine Learning. This tool provides deep insights into system performance, visualizes metrics, and uses AI to suggest optimizations.

![Dashboard Preview](https://via.placeholder.com/800x400?text=OS+Performance+Monitor+Dashboard)

## ✨ Features

- **Real-Time Monitoring**: Live tracking of CPU, RAM, and Disk usage using fluid, canvas-based charts.
- **Process Analysis**: Detailed view of running processes with "Task Manager" style metrics.
- **AI Optimization**: Integrated Machine Learning model (Decision Tree) that classifies system load (Low, Medium, High) and suggests actions.
- **Smart Alerts**: Highlights high-resource processes (High CPU or High Memory) with visual red alerts.
- **Modern UI**: Response, professional "Zinc" dark theme (with Light Mode support), smooth animations, and a landing page.
- **History Tracking**: Logs system metrics to a MySQL database for historical analysis.

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Psutil (Metrics), Scikit-Learn (ML), MySQL Connector.
- **Frontend**: HTML5, CSS3 (Custom Design), JavaScript, Chart.js.
- **Database**: MySQL.

## 📋 Prerequisites

Before running the project, ensure you have the following installed:

1.  **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2.  **MySQL Server**: [Download MySQL](https://dev.mysql.com/downloads/installer/)

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/dinesh4o/OS-Performance.git
    cd OS-Performance
    ```

2.  **Install Dependencies**
    ```bash
    pip install flask psutil mysql-connector-python scikit-learn numpy
    ```

3.  **Database Configuration**
    - Open your MySQL Client (Workbench or CLI).
    - Create the database:
      ```sql
      CREATE DATABASE os_monitor;
      ```
    - *Note: The application expects default credentials (`root` / `password`). If yours differ, update `database.py`.*

4.  **Run the Application**
    ```bash
    python app.py
    ```

5.  **Access the Dashboard**
    - Open your browser and navigate to: `http://localhost:5000`

## 🧠 ML Model

The system includes a pre-trained model (`model.pkl`) to classify system states. You can retrain this model anytime via the "Settings" menu in the dashboard or by hitting the `/api/retrain` endpoint.

## 📜 License

This project is open-source and available under the MIT License.