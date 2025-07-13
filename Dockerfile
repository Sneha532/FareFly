FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY ./FareFly/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ./FareFly/backend/src/ /app/src/
COPY ./FareFly/backend/alembic.ini .
RUN mkdir -p /app/migrations
COPY ./FareFly/backend/migrations/ /app/migrations/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Create startup script
RUN echo '#!/bin/bash' > start.sh && \
    echo 'echo "Starting application..."' >> start.sh && \
    echo 'echo "Database URL: ${DATABASE_URL:0:25}..."' >> start.sh && \
    echo 'alembic upgrade head || echo "Warning: Migration failed but continuing"' >> start.sh && \
    echo 'uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000}' >> start.sh && \
    chmod +x start.sh

EXPOSE ${PORT}
CMD ["./start.sh"]