# 🔁 Adaptive Retry Engine

This project demonstrates how retry logic can be implemented **intelligently** instead of blindly retrying failed operations.

In real-world systems, APIs and network calls often fail due to timeouts, server errors, or temporary issues.  
Simply retrying again and again can make things worse.  
This project shows a **smarter approach** to retries using Python.

The same retry logic is demonstrated in **two forms**:
1. A **simple script-based version (`main.py`)**
2. A **FastAPI-based service** to show real-world usage

---

## 🎯 Why This Project Exists

Most beginner projects retry failed operations like this:

```
try → fail → retry → retry → retry
```

This is dangerous because:
- It can overload servers
- It can cause infinite loops
- It ignores why the failure happened

This project solves that by:
- Understanding *what kind of error occurred*
- Deciding *whether retrying makes sense*
- Stopping retries safely when needed
- Keeping logs of retry behavior

---

## 🧠 Core Idea (In Simple Words)

Not every failure should be retried.

The retry engine:
- Retries **temporary failures**
- Stops on **permanent failures**
- Limits retries using a **retry budget**
- Protects systems using a **circuit breaker**
- Logs only meaningful retry events

---

## 📁 Project Structure

```
AdaptiveRetryEngine/
│
├── main.py
├── README.md
├── requirements.txt
│
├── api/
│   └── service.py
│
├── retry/
│   ├── engine.py
│   ├── classifier.py
│   ├── strategies.py
│   ├── circuit_breaker.py
│   ├── budget.py
│   └── history.py
│
├── logs/
│   └── retry_log.ndjson
```

---

## ⚙️ How the Project Works

### 1️⃣ Failure Classification
When an operation fails, the error is classified into types such as:
- Timeout
- Connection error
- HTTP 500 (server error)
- Permanent errors (like bad requests)

This helps decide whether retrying is useful.

---

### 2️⃣ Retry Decision Engine
The RetryEngine checks:
- Is the failure permanent?
- Is retry budget exhausted?
- Is the circuit breaker open?

Only if retrying is safe, the engine allows another attempt.

---

### 3️⃣ Backoff Strategy
Retries are not immediate.  
The delay between retries increases gradually to reduce system load.

---

### 4️⃣ Circuit Breaker
If too many failures happen:
- The circuit opens
- Further retries are blocked
- This prevents cascading failures

---

### 5️⃣ Logging
Only **failures and retry decisions** are logged.

Successful requests are **not logged** to keep logs clean and meaningful.

The log file uses **JSON Lines (NDJSON)** format, which is common for logging systems.

---

## ▶️ Running the Project

### Script-Based Version
```bash
python main.py
```

This version helps understand retry logic without any web framework.

---

### API-Based Version (FastAPI)
```bash
python -m uvicorn api.service:app --reload
```

Open in browser:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

Test endpoint:
```
GET /fetch-data
```

---

## 🧾 Logging Behavior

- Logs contain only failures and retry-related events
- Successful API calls are not logged
- This design avoids unnecessary noise

Example log entry:
```json
{"event":"retry","error":"HTTP_500","attempt":3,"timestamp":"2026-01-11T22:43:58"}
```

---

## 🎓 Academic Value

This project demonstrates:
- Practical understanding of failure handling
- Real-world retry strategies
- Clean modular Python design
- Difference between script-based and API-based execution
- Logging and observability basics

Suitable for:
- Final-year projects
- Resume projects
- Viva and interviews

---

## 📌 Resume Bullet

Built an adaptive retry engine in Python that intelligently handles API failures using error classification, retry budgets, circuit breaker logic, and FastAPI integration with structured logging.

---

## ✅ Project Status

✔ Retry logic implemented  
✔ Script and API versions available  
✔ Logging works correctly  
✔ Easy to explain  
✔ College-level and recruiter-friendly  
✔ GitHub ready  
