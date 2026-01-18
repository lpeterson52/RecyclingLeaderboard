# Use a slim official Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable buffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps for some packages (openssl for dnspython/ssl, build tools if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# Copy app code
COPY . .

# (Optional) create non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Healthcheck (container-level)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://127.0.0.1:8000/health || exit 1

# Use Gunicorn with uvicorn workers for production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", \
     "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "60"]