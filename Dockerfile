FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including git and ca-certificates
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install requirements with extra error handling
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools wheel && \
    # First try with regular install
    pip install --no-cache-dir -r requirements.txt || \
    # If that fails, try with --trusted-host
    pip install --no-cache-dir --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host github.com -r requirements.txt || \
    # If that fails too, try cloning manually
    (git clone https://github.com/weatherapicom/python.git && \
     cd python && \
     pip install . && \
     cd .. && \
     rm -rf python && \
     pip install -r requirements.txt)

# Copy configuration files
COPY .env .
COPY pytest.ini .
COPY create_weather_table.sql .
COPY entrypoint.sh .

# Copy Python package files
COPY __init__.py .

# Copy application code
COPY weather_fetcher.py .
COPY weather_service.py .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Use the shell script as entrypoint
ENTRYPOINT ["./entrypoint.sh"] 