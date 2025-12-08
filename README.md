# WorkEntry

A lightweight work-entry / activity-tracking application with a FastAPI backend and Docker-based infrastructure.

## 🚀 Initial Setup

### 1️⃣ Clone the Repository
```
git clone https://github.com/JobyGeJo/WorkEntry.git
cd WorkEntry
```

### 2️⃣ Create the Environment Variables File
Inside `./backend/`, create a file named `variables.env` and add your environment variables:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
POSTGRES_DB=postgres
POSTGRES_HOST=localhost

MONGO_USER=root
MONGO_PASSWORD=root

REDIS_HOST=localhost
```

You may change these values as needed.

### 3️⃣ Start Docker Services
This project uses Docker for PostgreSQL, MongoDB, and Redis.

```
docker-compose up -d
```

### 4️⃣ Run Backend Setup Script
```
python3 backend/setup.py
```

Make sure your environment loads `variables.env`.

### 5️⃣ Start the FastAPI Server
```
uvicorn backend.main:app --reload
```

Ensure the environment variables from `variables.env` are loaded before running.

## 📁 Project Structure
```
WorkEntry/
 ├── backend/
 │   ├── main.py
 │   ├── setup.py
 │   ├── variables.env (you should this)
 │   └── ...
 ├── docker-compose.yml
 └── README.md
```
