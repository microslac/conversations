FROM --platform=linux/amd64 python:3.11.4-slim as app

RUN apt-get update && apt-get install -y --no-install-recommends \
	    ca-certificates curl wget \
    	gcc libpq-dev dumb-init \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY ./requirements/ ./requirements/
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && rm -rf requirements && rm requirements.txt

# Run environments
ENV NUM_WORKERS=1
ENV BIND_PORT=8014
ENV DJANGO_SETTINGS_MODULE="api.settings"

# Application files
COPY ./src ./src
COPY ./logs ./logs
COPY ./docker/gunicorn.py ./gunicorn.py

# Run as non-root user
RUN adduser --shell /bin/bash --uid 1001 appuser
RUN chown -R appuser .
USER appuser

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD gunicorn -c ./gunicorn.py -w "$NUM_WORKERS" -b "0.0.0.0:${BIND_PORT}" --worker-class uvicorn.workers.UvicornWorker --chdir ./src api.asgi:application
