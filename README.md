# Assets - Personal Finance Dashboard 💰

Portfolio management system for tracking precious metals, crypto, cash, and stocks with real-time pricing.

## Quick Start

### Web Dashboard (Recommended)

```bash
cd assets_gui
./run_local.sh
```

Open http://localhost:8501

### CLI Version

```bash
cd assets_cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Docker

```bash
cd assets_gui
docker build -t assets-gui .
docker run -p 8501:8501 -p 8001:8001 -v assets-data:/app/data assets-gui
```

## Features

- 💰 **Precious Metals**: Gold & silver tracking with capital gains
- 🪙 **Bitcoin**: Strike integration with real-time pricing
- 💵 **Cash & Receivables**: Multi-account management
- 📈 **Stocks**: Tax-optimized portfolio tracking
- 📊 **Analytics**: Portfolio evolution and reporting
- 🔄 **Real-time Prices**: Live market data integration

## Architecture

| Component | CLI | GUI |
|-----------|-----|-----|
| Interface | Terminal menu | Web (Streamlit) |
| Database | Config file | SQLite |
| API | - | FastAPI |
| Admin Tools | - | ✅ Dashboard |
| Backups | Manual | ✅ Automated |
| Docker | - | ✅ Ready |

## Structure

```
assets/
├── assets_cli/       # Terminal-based dashboard
├── assets_gui/       # Web-based dashboard
│   ├── Dockerfile
│   └── streamlit_app/
│       ├── app.py           # Streamlit UI
│       ├── pricing_api.py    # FastAPI service
│       └── data/
└── README.md
```

## Documentation

- [assets_gui README](assets_gui/README.md) - Web dashboard setup & deployment
- [assets_cli README](assets_cli/README.md) - CLI setup & configuration

## Stack

**GUI**: Streamlit + FastAPI + SQLite + pandas  
**CLI**: Python + requests + BeautifulSoup
```
## Quick Start

### 🚀 Modern Web Dashboard (Recommended)

```bash
cd assets_gui
./run_local.sh
```

Then visit:
- 🌐 **UI**: http://localhost:8501
- 🔌 **API**: http://localhost:8001

### 🐳 Docker Deployment

```bash
cd assets_gui

# Build image
docker build -t assets-gui:latest .

# Run with persistent data
docker run -p 8001:8001 -p 8501:8501 \
  -v assets-data:/app/data \
  assets-gui:latest
```

### 📺 Legacy CLI

```bash
cd assets_cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Technology Stack

### assets_cli

- **Language**: Python 3
- **UI**: Terminal-based CLI with interactive menus
- **APIs**: CoinGecko (BTC pricing), web scraping (gold/silver)
- **Features**: Discord webhook integration, encrypted config support

### assets_gui

- **Frontend**: Streamlit (Python-based web framework)
- **Backend API**: FastAPI (modern REST API)
- **Database**: SQLite3
- **Pricing**: FastAPI local service with intelligent caching
- **Data**: pandas for analytics
- **Deployment**: Docker containerization

## Feature Comparison

| Feature | CLI | GUI |
|---------|-----|-----|
| Web Interface | ❌ | ✅ |
| Real-time Dashboard | ❌ | ✅ |
| Data Persistence | ⚠️ Config file | ✅ SQLite |
| Admin Tools | Limited | ✅ Full suite |
| Backup/Restore | Manual | ✅ Automated |
| API Access | ❌ | ✅ FastAPI |
| Docker Support | ❌ | ✅ Production-ready |
| Historical Tracking | Basic | ✅ Advanced |
| Scalability | Single user | Multi-user ready |

## Configuration

### assets_gui configuration

1. **Environment Variables** (optional):
   ```bash
   cp .env.example .env
   # Edit with your API keys
   ```

2. **Runtime Settings**:
   ```json
   // streamlit_app/data/runtime_settings.json
   {
     "pricing_api": {
       "cache_ttl_seconds": 60,
       "request_timeout_seconds": 10,
       "request_retries": 3
     }
   }
   ```

3. **Streamlit Secrets** (for sensitive data):
   ```toml
   # ~/.streamlit/secrets.toml
   api_key = "your_api_key"
   ```

### assets_cli configuration

Use `config.py` template:

```bash
cp config.py.template config.py
# Edit with your portfolio data
```

Optional encryption:

```bash
# Encrypt config
age -r age_key config.py -o config.py.age

# Decrypt config
age -d -i ~/.age/key.txt config.py.age > config.py
```

## Features by Component

### 💰 Asset Management

Both platforms support:

- **Gold Portfolio**
  - Real-time price fetching
  - Capital gains calculation
  - Tax computation (30% flat tax - PFU)
  - Net liquidation value

- **Silver Portfolio**
  - Same features as gold
  - Separate position tracking

- **Bitcoin**
  - Strike API integration
  - Real-time BTC/EUR pricing
  - Capital gains and tax reporting
  - Multi-exchange support (GUI only)

- **Stock Portfolio**
  - Holding period tax analysis
  - Different rates for <5 years vs ≥5 years
  - Position management

### 💵 Cash & Receivables

- Multiple cash accounts
- Receivables tracking
- Debt management
- Quick summary views

### 📊 Analytics & Reporting

- Portfolio value evolution charts
- Asset allocation visualization
- Historical performance tracking
- Export capabilities (CSV, JSON)
- Discord integration (CLI)

### 🛠️ Administrative Tools

- **GUI Only Features**:
  - Database health checks
  - Automated backups with versioning
  - One-click data restore
  - Export/import workflows
  - Data purging and cleanup

## API Reference

### FastAPI Pricing Service (GUI)

Base URL: `http://localhost:8001`

**Health Check**:
```bash
curl http://localhost:8001/health
```

**Fetch Prices**:
```bash
curl http://localhost:8001/prices
```

**Get Settings**:
```bash
curl http://localhost:8001/settings
```

See [assets_gui README](assets_gui/README.md) for full API documentation.

## Deployment

### Local Development

```bash
cd assets_gui
./run_local.sh
```

### Production with Docker

```bash
# Build
docker build -t assets-gui:prod .

# Run
docker run -d \
  --name assets-gui \
  -p 8001:8001 \
  -p 8501:8501 \
  -v assets-data:/app/data \
  -e STRIKE_API_TOKEN="your_token" \
  --restart unless-stopped \
  assets-gui:prod
```

### Kubernetes

Use the provided Dockerfile with standard Kubernetes manifests:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: assets-gui
spec:
  replicas: 1
  selector:
    matchLabels:
      app: assets-gui
  template:
    metadata:
      labels:
        app: assets-gui
    spec:
      containers:
      - name: assets-gui
        image: assets-gui:latest
        ports:
        - containerPort: 8001
        - containerPort: 8501
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: assets-data
```

## Troubleshooting

### GUI Issues

- **Port already in use**: 
  ```bash
  lsof -i :8501  # Find process
  kill -9 <PID>  # Kill it
  ```

- **API connection failed**:
  ```bash
  curl http://localhost:8001/health  # Check API
  ```

- **Database errors**:
  - Use Admin > Health Check
  - Restore from backup if needed

### CLI Issues

- **Config not found**: Ensure `config.py` exists (see `config.py.template`)
- **API errors**: Check network connection and API rate limits
- **Import errors**: Reinstall dependencies

### Docker Issues

```bash
# View logs
docker logs <container-id>

# Restart container
docker restart <container-id>

# Shell into container
docker exec -it <container-id> /bin/bash
```
