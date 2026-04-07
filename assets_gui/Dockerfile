FROM python:3.11-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY streamlit_app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY streamlit_app/ .

# Create data directory for SQLite and backups
RUN mkdir -p /app/data/backups

# Expose ports
# 8001: FastAPI pricing API
# 8501: Streamlit UI
EXPOSE 8001 8501

# Health check for the API
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health', timeout=2)" || exit 1

# Run both services
CMD python -m uvicorn pricing_api:app --host 0.0.0.0 --port 8001 & \
    python -m streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8501 && wait
