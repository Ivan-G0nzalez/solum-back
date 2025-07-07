FROM python:3.10-slim

# Install system dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    g++ \
    gnupg \
    unixodbc \
    unixodbc-dev \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000
