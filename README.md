# 📰 Scraping Service

This microservice scrapes news stories from various internet sources, checks for duplicates using a Redis-based cache, and publishes new stories to a Kafka topic for further processing by other services in the system.

---

## 🚀 Features

- 🌐 Scrapes news stories from online sources
- 🧠 Avoids duplicates using a Redis cache
- 📤 Publishes clean, new stories to Kafka
- ⚙️ Asynchronous processing with `asyncio`
- 🐳 Dockerized for easy deployment
- ✅ GitHub Actions workflow for PRs to `main` branch

---

## 🧰 Tech Stack

- **Python 3.13**
- **Asyncio** for non-blocking operations
- **Redis** for duplicate-check caching
- **Kafka** for message publishing
- **Docker** for containerization
- **GitHub Actions** for CI on PRs to `main`

---

## 🧪 Local Development

### 1. Clone the repo
```bash
git clone https://github.com/Mustapha-Innocer/scraping-service.git
cd scraping-service
```

### 2. Create `.env` file and provide value for each missing variable
```ini
# Kakfa
KAFKA_SERVER=
KAFKA_PORT=

# Redis
REDIS_SERVER=
REDIS_PORT=

# Caching
TTL_NEW_TAG=864000
TTL_ERRORED_TAG=432000
```
### 3. Create new python virtual environment
```bash
python -m venv venv
```

### 4. Intall the python dependencies
```bash
pip install -r requirements.txt
```

### 5. Run
```bash
python main.py
```

---


## 🧠 Environment Variables

| Variable          | Description                   | Example       |
|------------------|-------------------------------|---------------|
| `KAFKA_SERVER`   | Kafka host                     | `localhost`   |
| `KAFKA_PORT`     | Kafka port                     | `9094`        |
| `REDIS_SERVER`   | Redis host                     | `localhost`   |
| `REDIS_PORT`     | Redis port                     | `6379`        |
| `TTL_NEW_TAG`    | Time to live for new story tags         | `864000`      |
| `TTL_ERRORED_TAG`| Time to live for errored story tags     | `432000`      |

---

## 📬 Kafka Topic

- The service publishes stories to a Kafka topic "**news-data**".
- Downstream services like LLM consumers can subscribe to this topic.

---

## 🧱 Related Services

This is part of a larger microservice-based system. See the [Main Project README](https://github.com/Mustapha-Innocer/news-aggregator) for architecture and links to all services.
