# 🚨 Incident AI Management System

## 📌 Overview

Incident AI is an intelligent incident management backend system built using **FastAPI**, **SQLAlchemy**, and **JWT Authentication**.
The system automatically analyzes alerts using AI and manages incident lifecycle operations securely.

---

## 🚀 Features

✅ AI-based Incident Processing
✅ JWT Authentication
✅ Role-Based Access Control (RBAC)
✅ Incident Ownership Security
✅ Admin Assignment System
✅ Incident Lifecycle Management
✅ Secure CRUD APIs
✅ SQLite Database Integration

---

## 🏗 Tech Stack

* FastAPI
* Python
* SQLAlchemy
* JWT Authentication
* SQLite
* Pydantic
* Uvicorn

---

## 🔐 Roles

### Admin

* Assign incidents
* Update incidents
* Delete incidents
* View all incidents

### Analyst/User

* Create incidents
* View assigned incidents
* Update owned incidents

---

## ⚙️ Installation

```bash
git clone <repo-url>
cd incident_ai
pip install -r requirements.txt
```

Run server:

```bash
python -m uvicorn app:app --reload
```

Open API Docs:

```
http://127.0.0.1:8000/docs
```

---

## 🔑 Default Users

Admin:

```
username: admin
password: admin123
```

Analyst:

```
username: analyst
password: analyst123
```

---

## 📊 Incident Lifecycle

```
OPEN → IN_PROGRESS → RESOLVED → CLOSED
```


