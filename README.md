# 🚀 AI Incident Management System

An **AI-powered Incident Management Platform** designed to automatically analyze system incidents, classify severity levels, and provide intelligent triage insights through an interactive dashboard.

This project demonstrates a **production-style full-stack AI application** combining backend APIs, authentication, automated analysis, and a real-time monitoring dashboard.

---

## 📌 Project Overview

Modern IT systems generate thousands of alerts daily. Manual incident handling delays response time and increases operational risk.

The **AI Incident Management System** solves this problem by:

* Automatically analyzing incident descriptions
* Classifying incident severity
* Identifying affected components
* Suggesting possible root causes
* Visualizing incidents through a live command center dashboard

---

## ✨ Key Features

✅ Secure User Authentication (JWT-based)
✅ AI-powered Incident Analysis
✅ Automatic Severity Classification
✅ Incident Creation & Tracking
✅ Real-time Monitoring Dashboard
✅ Role-based Access Support
✅ RESTful FastAPI Backend
✅ Interactive Streamlit UI
✅ Data Visualization & Metrics

---

## 🏗️ System Architecture

```
User → Streamlit Dashboard → FastAPI Backend → AI Analysis Engine → Database
```

### Components

* **Frontend:** Streamlit Premium Dashboard
* **Backend:** FastAPI REST API
* **AI Layer:** Rule/LLM-based incident analysis
* **Database:** JSON / Local storage
* **Authentication:** JWT Token Security

---

## 🛠️ Tech Stack

| Layer             | Technology               |
| ----------------- | ------------------------ |
| Backend           | FastAPI                  |
| Frontend          | Streamlit                |
| Language          | Python                   |
| Visualization     | Plotly                   |
| API Communication | Requests                 |
| Authentication    | JWT                      |
| Server            | Uvicorn                  |
| Deployment        | Render + Streamlit Cloud |

---

## 🔐 Authentication Flow

1. Create User (`/users`)
2. Login (`/login`)
3. Copy Access Token
4. Paste Token into Dashboard Sidebar
5. Perform Incident Operations

---

## 📡 API Endpoints

| Method | Endpoint     | Description        |
| ------ | ------------ | ------------------ |
| POST   | `/users`     | Create user        |
| POST   | `/login`     | Authenticate user  |
| POST   | `/incident`  | Create AI incident |
| GET    | `/incidents` | Fetch incidents    |

---

## 📊 Dashboard Capabilities

* Incident Overview Metrics
* Severity Distribution Charts
* Incident Monitoring Panel
* AI Incident Creation Interface
* Live Incident Updates

---

## 🔮 Future Enhancements

* LLM-based Root Cause Analysis
* Email / Slack Alert Integration
* Incident Auto-Resolution Suggestions
* Database Migration (PostgreSQL)
* Multi-user Role Dashboard
* Cloud Monitoring Integration

---

## 🎯 Use Cases

* IT Operations Monitoring
* DevOps Incident Tracking
* Server Health Management
* AI-assisted Support Systems
* Enterprise Monitoring Tools

---

## 📄 License

This project is developed for educational and portfolio purposes.

