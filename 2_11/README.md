# Exercise 2.11 – Containerized development environment

For this exercise I took a small Python (Flask) web app that counts page visits and
stores the counter in Redis. I moved its development environment into containers, so
the only thing needed on the machine is Docker. Python, Flask and Redis don't have to
be installed locally.

## What I did

- **Containerized the app**: I wrote a `Dockerfile` that installs the Python
  dependencies and starts Flask in debug mode (`FLASK_DEBUG=1`).
- **Hot reload during development**: the project directory is bind-mounted into the
  container (`.:/app`). When I edit code on the host, Flask detects the change and
  restarts automatically, so I don't need to rebuild the image.
- **Containerized the database**: Redis runs as its own service from the official
  `redis` image instead of being installed on my machine.
- **Data persistence**: Redis data is stored in a named volume (`data:/data`), so the
  visit counter is kept after `docker compose down`.
- **Networking**: the app reaches Redis through the Compose network by its service name
  (`REDIS_HOST=redis`). `depends_on` makes Compose start Redis before the app.

## Files

| File                 | Purpose                                  |
|----------------------|------------------------------------------|
| `app.py`             | Flask app that increments `hits` in Redis |
| `requirements.txt`   | Python dependencies (flask, redis)        |
| `Dockerfile`         | Builds the app image in dev mode          |
| `docker-compose.yml` | Starts the app and Redis together         |

## docker-compose.yml

```yaml
services:
  redis:
    image: redis
    volumes:
      - data:/data

  app:
    build: .
    volumes:
      - .:/app
    ports:
      - 5000:5000
    environment:
      - FLASK_DEBUG=1
      - REDIS_HOST=redis
    depends_on:
      - redis

volumes:
  data:
```

## How to run

```bash
docker compose up --build
```

Open http://localhost:5000. The visit count goes up each time you refresh the page.

If you edit `app.py` and refresh, the change shows up straight away because of hot reload.

Run `docker compose down` to stop. Add `-v` to also delete the Redis data.
