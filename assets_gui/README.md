# assets_gui - Asset Management Dashboard 💰

Modern web-based personal asset management application built with **Streamlit** (UI) + **FastAPI** (pricing API) + **SQLite** (database).

## Overview

A comprehensive portfolio management system for tracking and managing:

- **Assets**: Gold, silver, bitcoin holdings with real-time pricing
- **Cash**: Multiple cash accounts and balances
- **Receivables & Debts**: Manage amounts owed to you and by you
- **Admin Tools**: Health checks, database backups, exports, data purging

### Key Pages

- **Home**: Dashboard overview
- **Assets**: Gold, silver, bitcoin portfolio management
- **Cash**: Cash account tracking
- **Receivables**: Outstanding amounts owed to you
- **Debts**: Outstanding amounts you owe
- **Admin**: Maintenance, health checks, backups, data management

## Tech Stack

- **UI Framework**: Streamlit
- **REST API**: FastAPI + Uvicorn
- **Database**: SQLite3
- **Data Processing**: pandas
- **HTTP Client**: requests
- **Environment Management**: python-dotenv

## Project Structure

```
streamlit_app/
├── app.py                 # Main Streamlit application
├── pricing_api.py         # FastAPI local pricing service
├── requirements.txt       # Python dependencies
└── data/
    ├── backups/          # Database backups directory
    ├── runtime_settings.json  # API configuration
    └── *.db              # SQLite database files
```

## Setup & Installation

### Prerequisites

- Python 3.11+
- pip or conda

### Local Development

```bash
cd streamlit_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create data directory
mkdir -p data/backups
```

### Environment Variables (Optional)

Create a `.streamlit/secrets.toml` or `.env` file in `streamlit_app/`:

```env
# For Strike API integration (optional)
STRIKE_API_TOKEN=your_token
STRIKE_API_BASE_URL=https://api.strike.me
STRIKE_SOURCE_CURRENCY=BTC
STRIKE_TARGET_CURRENCY=EUR
```

## Running the Application

### Local Development (one-liner)

```bash
./run_local.sh
```

This starts:
- **FastAPI API**: http://localhost:8001 (pricing engine)
- **Streamlit UI**: http://localhost:8501 (main app)

### Manual Start

```bash
cd streamlit_app

# Terminal 1: Start the pricing API
python -m uvicorn pricing_api:app --host 0.0.0.0 --port 8001

# Terminal 2: Start the Streamlit app
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### API Health Check

```bash
curl http://localhost:8001/health
```

## Docker Deployment

### Build

```bash
docker build -t assets-gui:latest .
```

### Run Container

```bash
# Basic run
docker run -p 8001:8001 -p 8501:8501 assets-gui:latest

# With persistent volume for data
docker run -p 8001:8001 -p 8501:8501 \
  -v assets-data:/app/data \
  assets-gui:latest

# With environment variables
docker run -p 8001:8001 -p 8501:8501 \
  -e STRIKE_API_TOKEN=your_token \
  -e STRIKE_API_BASE_URL=https://api.strike.me \
  -v assets-data:/app/data \
  assets-gui:latest
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.9'

services:
  assets-gui:
    build: .
    ports:
      - "8001:8001"    # FastAPI
      - "8501:8501"    # Streamlit
    volumes:
      - assets-data:/app/data
    environment:
      - STRIKE_API_TOKEN=${STRIKE_API_TOKEN}
      - STRIKE_API_BASE_URL=https://api.strike.me
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

volumes:
  assets-data:
    driver: local
```

Then run:

```bash
docker compose up -d
```

## API Endpoints

### Pricing API (FastAPI)

- `GET /health` - Health check status
- `GET /prices` - Current asset prices
- `GET /settings` - Runtime settings
- (Additional endpoints available in `pricing_api.py`)

## Backup & Restore

### Backup Data

Backups are automatically stored in `data/backups/`. Use the Admin page to:
- Create manual backups
- List existing backups
- Restore from backup
- Export data (CSV/JSON)

### Volume Persistence (Docker)

Always mount a volume for the `data` directory:

```bash
docker run -v assets-data:/app/data ... assets-gui:latest
```

## Troubleshooting

### Streamlit won't start
- Check if port 8501 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`

### API connection errors
- Ensure port 8001 is available
- Check API is running: `curl http://localhost:8001/health`
- Review logs for connection timeouts

### Database issues
- Check `data/` directory permissions
- Review backups in `data/backups/`
- Use Admin page to verify database health

### Docker container exits
- Check logs: `docker logs <container-id>`
- Ensure volumes are properly mounted
- Verify environment variables are set correctly

## Performance Tuning

### Streamlit Cache Settings

Adjustable in `streamlit_app/data/runtime_settings.json`:

```json
{
  "pricing_api": {
    "cache_ttl_seconds": 60,
    "request_timeout_seconds": 10,
    "request_retries": 3,
    "request_backoff_seconds": 1
  }
}
```


```bash
cd /root/assets_gui_poc
./run_local.sh
```

Default endpoints:

- API health: http://127.0.0.1:8001/health
- App: http://127.0.0.1:8501

Run services manually (optional):

```bash
cd /root/assets_gui_poc/streamlit_app
venv/bin/python -m uvicorn pricing_api:app --host 0.0.0.0 --port 8001
```

```bash
cd /root/assets_gui_poc/streamlit_app
venv/bin/python -m streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8501
```

## Configuration

Environment variables:

- `PRICING_API_BASE_URL` (default: `http://127.0.0.1:8001`)
- `APP_DEMO_MODE` (default: `0`)
- `APP_ADMIN_PASSWORD` (optional)

Runtime settings:

- Managed from Admin > Maintenance > Dynamic settings
- Persisted in `streamlit_app/data/runtime_settings.json`
- API-related settings (`pricing_api.*`) apply after API restart

## Admin Maintenance Features

- Pricing API health check
- Active pricing source monitoring
- Diagnostics bundle export (`.zip`)
- SQLite backup creation
- Guided restore from backup
- CSV snapshot export
- Purge tools (history and scoped/full data cleanup)

## URL Navigation

The app supports section links through query parameters, for example:

- `/?page=home`
- `/?page=assets`
- `/?page=cash`
- `/?page=receivables`
- `/?page=debts`
- `/?page=admin`
