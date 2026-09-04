# Habr for You 🤖

An asynchronous Telegram bot that monitors new articles on [Habr](https://habr.com/) and sends personalized notifications based on users' IT interests.

Users can subscribe to programming languages and IT fields, and the bot periodically checks Habr for new articles in the selected topics.

## Features

- Asynchronous Telegram bot
- Topic-based article subscriptions
- Programming language and IT field categories
- Subscribe and unsubscribe using inline keyboards
- View current subscriptions
- Automatic periodic Habr monitoring
- New article detection based on Habr article IDs
- Personalized article notifications
- Asynchronous HTTP requests and database operations
- PostgreSQL database
- Database migrations with Alembic
- Docker and Docker Compose support
- Persistent PostgreSQL storage
- Application logging and error handling

## Available Commands

| Command | Description |
|---|---|
| `/start` | Start the bot and view the introduction |
| `/subscribe` | Subscribe to new topics |
| `/subscriptions` | View current subscriptions |
| `/unsubscribe` | Unsubscribe from a topic |
| `/help` | Show available commands |

## Supported Topics

### Programming Languages

- Python
- Java
- JavaScript
- SQL
- C#
- C++
- C
- PHP
- Go
- Rust
- Swift
- Kotlin

### IT Fields

- Machine Learning
- QA
- DevOps
- Information Security
- Web Development
- Game Development

## How It Works

1. A user subscribes to one or more topics.
2. The subscriptions are stored in PostgreSQL.
3. A background job periodically retrieves all active topics.
4. The bot asynchronously requests the corresponding Habr pages.
5. The parser extracts the latest article ID, title, and URL.
6. The article ID is compared with the last processed ID stored in the database.
7. If a new article is detected, all subscribers of that topic receive a Telegram notification.
8. The latest article ID is updated after processing.

## Architecture

```text
Telegram
   |
   v
Handlers
   |
   v
Services
   |
   +------------------+
   |                  |
   v                  v
PostgreSQL         Habr Parser
   |                  |
SQLAlchemy          aiohttp
   |                  |
Alembic         BeautifulSoup
```

A background job runs independently from user commands:

```text
JobQueue
   |
   v
Get active topics
   |
   v
Fetch Habr pages
   |
   v
Detect new articles
   |
   v
Get subscribers
   |
   v
Send Telegram notifications
   |
   v
Update PostgreSQL
```

## Tech Stack

- Python 3.12
- python-telegram-bot
- asyncio
- aiohttp
- BeautifulSoup4
- lxml
- SQLAlchemy
- asyncpg
- PostgreSQL
- Alembic
- Docker
- Docker Compose

## Project Structure

```text
habr_bot/
├── alembic/
│   └── versions/
├── bot/
│   ├── constants/
│   ├── handlers/
│   └── keyboards/
├── database/
│   └── repositories/
├── jobs/
├── parser/
├── services/
├── utils/
├── alembic.ini
├── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── main.py
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Configure the following variables:

```env
HABR_BOT_TOKEN=your_telegram_bot_token

POSTGRES_DB=habr_bot
POSTGRES_USER=habr_bot_user
POSTGRES_PASSWORD=your_password

DATABASE_URL=postgresql+asyncpg://habr_bot_user:your_password@localhost:5432/habr_bot
```

Do not commit the `.env` file.

## Running with Docker

Build and start the application:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

View bot logs:

```bash
docker compose logs -f bot
```

Stop the application:

```bash
docker compose down
```

PostgreSQL data is stored in a Docker volume and persists after containers are recreated.

## Database Migrations

Database schema changes are managed with Alembic.

Create a migration:

```bash
alembic revision --autogenerate -m "migration description"
```

Apply migrations:

```bash
alembic upgrade head
```

When running through Docker Compose, migrations are automatically applied before the bot starts.

## Development

For local development without Docker, install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Apply migrations:

```bash
alembic upgrade head
```

Start the bot:

```bash
python main.py
```

## Deployment

The bot is deployed on Railway and runs continuously in a production environment.

The production setup consists of two Railway services:

- **Habr Bot** — the Dockerized Python application
- **PostgreSQL** — the managed production database

The application uses Railway environment variables to securely configure the Telegram bot token and database connection.

Before every deployment, Alembic migrations are automatically applied:

```bash
alembic upgrade head
```

If the migration fails, the new application version is not started.

The bot uses Telegram long polling, so it does not require a public HTTP endpoint or domain.


## CI/CD

The project includes an automated CI/CD pipeline using GitHub Actions and Railway.

### Continuous Integration

Every push or pull request to the `main` branch triggers a GitHub Actions workflow.

The CI pipeline:

1. Checks out the repository
2. Sets up Python 3.12
3. Starts a temporary PostgreSQL 16 database
4. Installs project dependencies
5. Checks Python syntax
6. Applies all Alembic migrations
7. Verifies that SQLAlchemy models do not contain unapplied schema changes
8. Checks that the main application modules can be imported successfully

The workflow must complete successfully before the new version can be deployed.

### Continuous Deployment

Railway is connected directly to the GitHub `main` branch and has **Wait for CI** enabled.

The deployment workflow is:

```text
Developer
    |
    v
git push to main
    |
    v
GitHub Actions
    |
    +---- CI failed ----> Deployment stopped
    |
    v
CI passed
    |
    v
Railway
    |
    v
Build Docker image
    |
    v
Run Alembic migrations
    |
    v
Start application
    |
    v
Production
```

This allows new versions of the bot to be automatically tested and deployed after every successful push to `main`.


## Future Improvements

- Automated CI/CD deployment
- Improved test coverage
- Additional Habr topics
- Better notification customization
- Administration and monitoring tools

## Author

Ara Darbinyan
