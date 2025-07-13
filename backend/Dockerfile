# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the application directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the Python project requirements
RUN pip install -r requirements.txt

# Copy the project code
COPY ./src /app/src
COPY ./alembic.ini /app/alembic.ini
COPY ./migrations /app/migrations

# Default port
ENV PORT=8000

# Create a startup script
RUN printf "#!/bin/bash\n" > ./start.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./start.sh && \
    printf "alembic upgrade head\n" >> ./start.sh && \
    printf "uvicorn src.app.main:app --host 0.0.0.0 --port \$RUN_PORT\n" >> ./start.sh

# Make the startup script executable
RUN chmod +x start.sh

# Clean up apt cache to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Expose the port
EXPOSE ${PORT}

# Run the FastAPI application
CMD ./start.sh