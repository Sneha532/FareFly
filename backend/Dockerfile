# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# Skip virtual environment creation to avoid memory issues
WORKDIR /app

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code - use explicit paths
COPY src/ /app/src/
COPY alembic.ini .
COPY migrations/ /app/migrations/

# Create startup script
RUN echo '#!/bin/bash' > start.sh && \
    echo 'alembic upgrade head' >> start.sh && \
    echo 'uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000}' >> start.sh && \
    chmod +x start.sh

EXPOSE ${PORT}
CMD ["./start.sh"]