
import streamlit as st
import sqlite3
from datetime import date, datetime, timezone, timedelta
import math
import requests
import pandas as pd
import shutil
import json
import io
import zipfile

st.set_page_config(page_title="Asset Management", layout="wide", page_icon="💰", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    :root {
        --bg-main: #070b14;
        --bg-panel: #121a2a;
        --bg-panel-2: #1a2438;
        --text-main: #edf2ff;
        --text-soft: #9db0cc;
        --accent: #67a4ff;
        --accent-2: #31d0aa;
        --line: rgba(132, 166, 223, 0.26);
    }

    .stApp {
        font-family: "Segoe UI", "Aptos", system-ui, sans-serif;
        color: var(--text-main);
        background:
            radial-gradient(1100px 520px at 8% -8%, rgba(47, 111, 255, 0.2), transparent 62%),
            radial-gradient(900px 460px at 98% 2%, rgba(34, 203, 157, 0.15), transparent 55%),
            linear-gradient(170deg, #0a0f1c 0%, #070b14 58%, #060910 100%);
    }

    .admin-row-separator {
        height: 1px;
        margin: 0.7rem 0 1.05rem 0;
        background: linear-gradient(90deg, rgba(103, 164, 255, 0), rgba(103, 164, 255, 0.28), rgba(49, 208, 170, 0.18), rgba(103, 164, 255, 0));
        border-radius: 999px;
    }

    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    .top-nav-title {
        font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #8ebeff;
        margin-bottom: 0.35rem;
    }

    div[role="radiogroup"] {
        display: inline-flex !important;
        flex-wrap: wrap;
        gap: 0.45rem;
        padding: 0.55rem;
        border-radius: 14px;
        border: 1px solid var(--line);
        background: rgba(12, 19, 33, 0.88);
        margin-bottom: 1rem;
        width: fit-content !important;
    }

    div[role="radiogroup"] > div {
        flex: 0 0 auto !important;
    }

    div[role="radiogroup"] > *:last-child {
        margin-right: 0 !important;
    }

    div[role="radiogroup"] > label,
    div[role="radiogroup"] > div > label {
        border-radius: 10px;
        border: 1px solid rgba(132, 166, 223, 0.22);
        background: rgba(19, 28, 45, 0.9);
        padding: 0.55rem 0.9rem;
        min-height: auto;
    }

    div[role="radiogroup"] > label:hover,
    div[role="radiogroup"] > div > label:hover {
        border-color: rgba(132, 182, 255, 0.55);
        background: rgba(28, 44, 72, 0.9);
    }

    div[role="radiogroup"] > label p,
    div[role="radiogroup"] > div > label p {
        color: #dce8ff !important;
        font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
        font-weight: 500;
        font-size: 1rem;
        margin: 0;
    }

    h1, h2, h3 {
        font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
        color: var(--text-main);
        letter-spacing: 0.015em;
    }

    p, label, .stCaption, .stMarkdown {
        color: var(--text-soft);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(155deg, rgba(25,34,52,0.95), rgba(18,25,40,0.95));
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.9rem 1rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
    }

    [data-testid="stMetric"] label,
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text-main) !important;
        font-weight: 600;
    }

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background: rgba(17, 24, 39, 0.95);
        border: 1px solid var(--line);
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stDataFrame"] * {
        color: #dbe7ff !important;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: rgba(17, 24, 39, 0.65);
    }

    [data-baseweb="tab-list"] {
        gap: 0.55rem;
        flex-wrap: wrap;
        margin-bottom: 0.8rem;
    }

    [data-baseweb="tab"] {
        border-radius: 10px !important;
        border: 1px solid var(--line) !important;
        color: var(--text-soft) !important;
        background: rgba(18, 24, 39, 0.65) !important;
        font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
        font-size: 1rem !important;
        line-height: 1.1 !important;
        min-height: 48px !important;
        padding: 0.75rem 1rem !important;
    }

    [aria-selected="true"][data-baseweb="tab"] {
        background: linear-gradient(145deg, rgba(54,117,255,0.32), rgba(35,205,164,0.2)) !important;
        color: #f3f7ff !important;
        border-color: rgba(121, 168, 255, 0.55) !important;
        box-shadow: 0 0 0 1px rgba(112, 164, 255, 0.2) inset;
    }

    .stButton > button,
    [data-testid="baseButton-primary"] {
        border-radius: 10px;
        border: 1px solid rgba(104, 160, 255, 0.45);
        background: linear-gradient(140deg, #2a5dcf 0%, #1f4aa6 100%);
        color: #eef4ff;
        font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
        font-weight: 600;
    }

    .stButton > button:hover,
    [data-testid="baseButton-primary"]:hover {
        border-color: rgba(124, 184, 255, 0.75);
        filter: brightness(1.08);
    }

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextArea textarea {
        background: #0f182a !important;
        color: #e9f1ff !important;
        border: 1px solid var(--line) !important;
        border-radius: 10px !important;
    }

    [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {
        color: #d9e6ff !important;
    }

    [data-testid="stInfo"] {
        background: rgba(35, 68, 134, 0.33);
        border: 1px solid rgba(114, 159, 244, 0.48);
    }

    [data-testid="stSuccess"] {
        background: rgba(20, 108, 82, 0.36);
        border: 1px solid rgba(68, 214, 171, 0.45);
    }

    [data-testid="stWarning"] {
        background: rgba(121, 81, 19, 0.35);
        border: 1px solid rgba(245, 193, 81, 0.45);
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    .block-container {
        padding-top: 1.1rem !important;
        max-width: 1400px;
    }

    .wow-hero {
        background:
            radial-gradient(110% 150% at 0% 0%, rgba(97, 151, 255, 0.22), transparent 45%),
            radial-gradient(120% 140% at 100% 0%, rgba(58, 214, 177, 0.20), transparent 48%),
            linear-gradient(160deg, rgba(21, 30, 47, 0.95), rgba(16, 22, 36, 0.95));
        border: 1px solid var(--line);
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.32);
        border-radius: 18px;
        padding: 1.35rem 1.35rem 1.25rem;
        margin-bottom: 1rem;
    }

    .wow-hero h1 {
        margin: 0;
        font-size: 2rem;
    }

    .wow-hero p {
        margin-top: 0.35rem;
        margin-bottom: 0.9rem;
        color: #a9bfdf;
    }

    .wow-kicker {
        font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #8fc2ff;
        margin-bottom: 0.35rem;
    }

    .wow-chips {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.65rem;
    }

    .wow-chip {
        border-radius: 11px;
        border: 1px solid rgba(129, 172, 235, 0.26);
        background: rgba(13, 20, 35, 0.85);
        padding: 0.55rem 0.7rem;
    }

    .wow-chip span {
        display: block;
        color: #95aac9;
        font-size: 0.78rem;
        margin-bottom: 0.2rem;
    }

    .wow-chip strong {
        font-size: 1rem;
        color: #eaf2ff;
        font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
    }

    .maintenance-hero {
        border: 1px solid rgba(118, 170, 255, 0.3);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        margin: 0.4rem 0 0.8rem 0;
        background:
            radial-gradient(120% 150% at 0% 0%, rgba(85, 136, 255, 0.22), transparent 45%),
            radial-gradient(120% 150% at 100% 0%, rgba(48, 203, 168, 0.2), transparent 50%),
            linear-gradient(160deg, rgba(20, 29, 45, 0.95), rgba(13, 21, 35, 0.95));
    }

    .maintenance-hero h4 {
        margin: 0;
        font-size: 1.05rem;
        color: #f2f7ff;
        font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
    }

    .maintenance-hero p {
        margin: 0.3rem 0 0;
        color: #a9c0e4;
        font-size: 0.92rem;
    }

    .ops-danger-badge {
        display: inline-block;
        margin: 0.2rem 0 0.7rem 0;
        padding: 0.34rem 0.58rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 115, 115, 0.55);
        background: rgba(117, 30, 34, 0.35);
        color: #ffd9dd;
        font-size: 0.82rem;
        letter-spacing: 0.01em;
    }

    .ops-kpi-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.55rem;
        margin-bottom: 0.65rem;
    }

    .ops-kpi-card {
        border-radius: 12px;
        border: 1px solid rgba(127, 168, 235, 0.26);
        background: rgba(15, 22, 36, 0.88);
        padding: 0.58rem 0.62rem;
        opacity: 0;
        transform: translateY(8px);
        animation: opsFadeUp 420ms ease forwards;
    }

    .ops-kpi-card:nth-child(1) { animation-delay: 50ms; }
    .ops-kpi-card:nth-child(2) { animation-delay: 120ms; }
    .ops-kpi-card:nth-child(3) { animation-delay: 190ms; }
    .ops-kpi-card:nth-child(4) { animation-delay: 260ms; }

    @keyframes opsFadeUp {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0px);
        }
    }

    .ops-kpi-card span {
        display: block;
        color: #91a9ce;
        font-size: 0.76rem;
        margin-bottom: 0.14rem;
    }

    .ops-kpi-card strong {
        color: #f1f6ff;
        font-size: 1rem;
    }

    .danger-panel {
        border: 1px solid rgba(255, 118, 133, 0.45);
        border-radius: 14px;
        padding: 0.85rem 0.9rem;
        background:
            radial-gradient(120% 130% at 0% 0%, rgba(176, 42, 58, 0.26), transparent 45%),
            linear-gradient(165deg, rgba(49, 18, 23, 0.92), rgba(31, 13, 18, 0.94));
        margin: 0.45rem 0 0.75rem 0;
    }

    .danger-panel h4 {
        margin: 0;
        color: #ffe9ec;
        font-size: 1.02rem;
    }

    .danger-panel p {
        margin: 0.35rem 0 0;
        color: #ffb8c1;
        font-size: 0.9rem;
    }

    .ops-filter-hint {
        font-size: 0.83rem;
        color: #9eb3cf;
        margin-top: 0.15rem;
    }

    .section-hero {
        border: 1px solid rgba(109, 164, 244, 0.28);
        border-radius: 14px;
        padding: 0.78rem 0.9rem;
        margin: 0.25rem 0 0.8rem 0;
        background: linear-gradient(165deg, rgba(18, 29, 47, 0.94), rgba(13, 20, 34, 0.94));
    }

    .section-hero h4 {
        margin: 0;
        color: #f2f7ff;
        font-size: 1.03rem;
    }

    .section-hero p {
        margin: 0.28rem 0 0;
        color: #a4b9d6;
        font-size: 0.9rem;
    }

    .mini-stat-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.55rem;
        margin-bottom: 0.7rem;
    }

    .mini-stat-card {
        border: 1px solid rgba(120, 165, 234, 0.25);
        border-radius: 12px;
        background: rgba(16, 24, 40, 0.88);
        padding: 0.58rem 0.65rem;
    }

    .mini-stat-card span {
        display: block;
        font-size: 0.76rem;
        color: #94abca;
        margin-bottom: 0.12rem;
    }

    .mini-stat-card strong {
        color: #f1f6ff;
        font-size: 1rem;
    }

    @media (max-width: 960px) {
        .wow-chips {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- DB INIT ---
import os
def get_db():
    db_path = os.path.join(os.path.dirname(__file__), "data", "assets.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn

def fetchall_dict(cursor):
    """Return all rows as list of dicts."""
    cols = [col[0] for col in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def init_db(conn):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS holdings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_type TEXT NOT NULL,
        asset_name TEXT NOT NULL,
        buy_date TEXT NOT NULL,
        buy_price_unit REAL NOT NULL,
        quantity REAL NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS accounts (
        account_name TEXT PRIMARY KEY,
        amount REAL NOT NULL,
        updated_at TEXT
    );
    CREATE TABLE IF NOT EXISTS receivables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        debtor TEXT NOT NULL,
        amount REAL NOT NULL,
        updated_at TEXT
    );
    CREATE TABLE IF NOT EXISTS debts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creditor TEXT NOT NULL,
        amount REAL NOT NULL,
        updated_at TEXT
    );

    CREATE TABLE IF NOT EXISTS price_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_type TEXT NOT NULL,
        asset_name TEXT NOT NULL,
        source_url TEXT NOT NULL,
        is_active INTEGER NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS asset_config (
        asset_type TEXT PRIMARY KEY,
        is_enabled INTEGER NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS portfolio_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recorded_at TEXT NOT NULL,
        total_value REAL NOT NULL
    );
    CREATE TABLE IF NOT EXISTS khoms_debts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        holding_id INTEGER,
        asset_type TEXT NOT NULL,
        asset_name TEXT NOT NULL,
        buy_date TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TEXT NOT NULL,
        paid_at TEXT,
        note TEXT
    );
    CREATE TABLE IF NOT EXISTS btc_dca_settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        is_enabled INTEGER NOT NULL DEFAULT 0,
        amount_eur REAL NOT NULL DEFAULT 0,
        frequency TEXT NOT NULL DEFAULT 'week',
        interval_count INTEGER NOT NULL DEFAULT 1,
        anchor_date TEXT,
        weekday INTEGER NOT NULL DEFAULT 0,
        month_day INTEGER NOT NULL DEFAULT 1,
        last_run_at TEXT
    );
    ''')
    conn.commit()

    for table_name in ["accounts", "receivables", "debts"]:
        table_cols = [row[1] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()]
        if "updated_at" not in table_cols:
            conn.execute(f"ALTER TABLE {table_name} ADD COLUMN updated_at TEXT")
            conn.commit()

    default_sources = [
        ("gold", "Gold Bar 100g", "https://www.achat-or-et-argent.fr/or/lingot-100g-or/3557"),
        ("gold", "Gold Maple Leaf", "https://www.achat-or-et-argent.fr/or/maple-leaf-1-once-or/3192"),
        ("gold", "Gold Bar 1oz", "https://www.achat-or-et-argent.fr/or/lingotin-1-once-or/3554"),
        ("silver", "Silver Maple Leaf", "https://www.achat-or-et-argent.fr/argent/maple-leaf-1-once/1668"),
        ("btc", "BTC", "https://api.strike.me/v1/rates/ticker"),
    ]
    for asset_type, asset_name, url in default_sources:
        exists = conn.execute(
            "SELECT 1 FROM price_sources WHERE asset_type=? AND asset_name=? AND source_url=?",
            (asset_type, asset_name, url),
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO price_sources (asset_type, asset_name, source_url, is_active) VALUES (?, ?, ?, 1)",
                (asset_type, asset_name, url),
            )

    default_assets = ["gold", "silver", "btc", "cash", "receivables", "debts"]
    for asset_type in default_assets:
        exists = conn.execute(
            "SELECT 1 FROM asset_config WHERE asset_type=?",
            (asset_type,),
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO asset_config (asset_type, is_enabled) VALUES (?, 1)",
                (asset_type,),
            )

    dca_exists = conn.execute("SELECT 1 FROM btc_dca_settings WHERE id=1").fetchone()
    if not dca_exists:
        conn.execute(
            """
            INSERT INTO btc_dca_settings
            (id, is_enabled, amount_eur, frequency, interval_count, anchor_date, weekday, month_day, last_run_at)
            VALUES (1, 0, 100.0, 'week', 1, ?, 0, 1, NULL)
            """,
            (date.today().isoformat(),),
        )
    conn.commit()

    # Migrate: create pending khoms for existing holdings without one
    orphan_holdings = conn.execute(
        "SELECT h.id, h.asset_type, h.asset_name, h.buy_date, h.buy_price_unit, h.quantity "
        "FROM holdings h "
        "WHERE h.asset_type IN ('gold','silver','btc') "
        "AND NOT EXISTS (SELECT 1 FROM khoms_debts k WHERE k.holding_id = h.id)"
    ).fetchall()
    _mig_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    for _h in orphan_holdings:
        _hid, _atype, _aname, _bdate, _bprice, _qty = _h
        _kamt = float(_bprice) * float(_qty) * 0.20
        conn.execute(
            "INSERT INTO khoms_debts (holding_id, asset_type, asset_name, buy_date, amount, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, 'pending', ?)",
            (_hid, _atype, _aname, _bdate, _kamt, _mig_ts),
        )
    conn.commit()

conn = get_db()
init_db(conn)

API_BASE_URL = os.getenv("PRICING_API_BASE_URL", "http://127.0.0.1:8001").rstrip("/")
APP_DEMO_MODE = os.getenv("APP_DEMO_MODE", "0").strip().lower() in {"1", "true", "yes", "on"}
APP_ADMIN_PASSWORD = os.getenv("APP_ADMIN_PASSWORD", "")
RUNTIME_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "data", "runtime_settings.json")
ADMIN_AUDIT_LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "admin_audit.log")


def load_runtime_settings():
    defaults = {
        "ui": {
            "live_prices_ttl_seconds": 5,
            "history_ttl_seconds": 10,
            "history_limit": 2000,
            "api_timeout_seconds": 20,
            "health_check_timeout_seconds": 5,
            "btc_price_min": 0,
            "btc_price_max": 0,
            "portfolio_total_min": 0,
            "portfolio_total_max": 0,
        },
        "pricing_api": {
            "cache_ttl_seconds": 60,
            "request_timeout_seconds": 10,
            "request_retries": 3,
            "request_backoff_seconds": 1,
        },
    }
    if not os.path.exists(RUNTIME_SETTINGS_PATH):
        return defaults
    try:
        with open(RUNTIME_SETTINGS_PATH, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except Exception:
        return defaults

    if not isinstance(loaded, dict):
        return defaults

    for top_key, top_value in defaults.items():
        loaded_section = loaded.get(top_key)
        if not isinstance(loaded_section, dict):
            loaded[top_key] = dict(top_value)
            continue
        for key, default_value in top_value.items():
            current_value = loaded_section.get(key)
            if not isinstance(current_value, type(default_value)):
                loaded_section[key] = default_value
    return loaded


def save_runtime_settings(payload):
    os.makedirs(os.path.dirname(RUNTIME_SETTINGS_PATH), exist_ok=True)
    with open(RUNTIME_SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=True, indent=2)


def append_admin_audit_log(action, status, details=""):
    os.makedirs(os.path.dirname(ADMIN_AUDIT_LOG_PATH), exist_ok=True)
    entry = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "action": str(action),
        "status": str(status),
        "details": str(details)[:500],
    }
    with open(ADMIN_AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=True) + "\n")

    # Keep log file bounded to avoid unbounded growth on long-lived deployments.
    try:
        if os.path.getsize(ADMIN_AUDIT_LOG_PATH) > 1_000_000:
            with open(ADMIN_AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(ADMIN_AUDIT_LOG_PATH, "w", encoding="utf-8") as f:
                f.writelines(lines[-1000:])
    except Exception:
        pass


def read_admin_audit_log(limit=100):
    if not os.path.exists(ADMIN_AUDIT_LOG_PATH):
        return []
    entries = []
    try:
        with open(ADMIN_AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    parsed = json.loads(line)
                except Exception:
                    continue
                if isinstance(parsed, dict):
                    entries.append(parsed)
    except Exception:
        return []
    return entries[-limit:]


def sparkline(values):
    ticks = "▁▂▃▄▅▆▇█"
    if not values:
        return ""
    min_v = min(values)
    max_v = max(values)
    if max_v == min_v:
        return ticks[0] * min(24, len(values))
    chars = []
    for value in values[-24:]:
        normalized = (float(value) - float(min_v)) / (float(max_v) - float(min_v))
        idx = int(round(normalized * (len(ticks) - 1)))
        idx = max(0, min(len(ticks) - 1, idx))
        chars.append(ticks[idx])
    return "".join(chars)


def audit_row_style(row):
    status = str(row.get("status", "")).lower()
    if status == "error":
        return ["background-color: rgba(130, 34, 49, 0.25)"] * len(row)
    if status == "ok":
        return ["background-color: rgba(24, 110, 83, 0.2)"] * len(row)
    return [""] * len(row)


def compute_source_confidence(source_assets, refresh_age_seconds):
    rows = []
    for item in source_assets or []:
        status = str(item.get("status", "")).lower()
        latency_ms = int(item.get("latency_ms", 0) or 0)
        if status != "ok":
            score = 0
        else:
            latency_penalty = min(45, int(latency_ms / 25))
            freshness_penalty = min(25, int((refresh_age_seconds or 0) / 20))
            score = max(0, 100 - latency_penalty - freshness_penalty)
        if score >= 80:
            level = "high"
        elif score >= 50:
            level = "medium"
        else:
            level = "low"
        rows.append(
            {
                "Type": item.get("asset_type", ""),
                "Asset": item.get("asset_name", ""),
                "Status": item.get("status", ""),
                "Latency ms": latency_ms,
                "Confidence": score,
                "Confidence level": level,
                "Error": item.get("error", ""),
            }
        )

    if not rows:
        return {"score": 0, "label": "unknown", "rows": []}

    score = int(sum(row["Confidence"] for row in rows) / len(rows))
    label = "high" if score >= 80 else "medium" if score >= 50 else "low"
    return {"score": score, "label": label, "rows": rows}


def detect_portfolio_outlier(history_rows, current_total):
    if not history_rows:
        return {"is_outlier": False, "delta_pct": 0.0, "baseline": 0.0}
    series = pd.DataFrame(history_rows)
    if "total_value" not in series.columns or series.empty:
        return {"is_outlier": False, "delta_pct": 0.0, "baseline": 0.0}
    try:
        baseline = float(series["total_value"].tail(12).median())
    except Exception:
        baseline = 0.0
    if baseline == 0:
        return {"is_outlier": False, "delta_pct": 0.0, "baseline": 0.0}
    delta_pct = ((float(current_total) - baseline) / baseline) * 100
    return {
        "is_outlier": abs(delta_pct) >= 7.0,
        "delta_pct": float(delta_pct),
        "baseline": baseline,
    }


def build_diagnostics_bundle(conn, counts, live_for_health, source_health):
    now_utc = datetime.now(timezone.utc)
    health_payload = {"status": "unknown"}
    health_error = ""
    latency_ms = None
    try:
        started = datetime.now(timezone.utc)
        health_resp = requests.get(f"{API_BASE_URL}/health", timeout=HEALTH_TIMEOUT_SECONDS)
        health_resp.raise_for_status()
        health_payload = health_resp.json()
        latency_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
    except Exception as exc:
        health_error = str(exc)

    history_rows = fetchall_dict(
        conn.execute(
            "SELECT recorded_at, total_value FROM portfolio_history ORDER BY id DESC LIMIT 240"
        )
    )

    snapshot = {
        "generated_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "api_base_url": API_BASE_URL,
        "api_health": health_payload,
        "api_health_error": health_error,
        "api_health_latency_ms": latency_ms,
        "db_counts": counts,
        "source_health": source_health,
        "sources_total": len((live_for_health or {}).get("assets", [])),
        "runtime_settings": load_runtime_settings(),
    }

    bundle = io.BytesIO()
    with zipfile.ZipFile(bundle, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("health_snapshot.json", json.dumps(snapshot, ensure_ascii=True, indent=2))
        zf.writestr("runtime_settings.json", json.dumps(load_runtime_settings(), ensure_ascii=True, indent=2))
        zf.writestr("portfolio_history_recent.json", json.dumps(history_rows, ensure_ascii=True, indent=2))
        if os.path.exists(ADMIN_AUDIT_LOG_PATH):
            with open(ADMIN_AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
                zf.writestr("admin_audit.log", f.read())

    bundle.seek(0)
    name = f"diagnostics_{now_utc.strftime('%Y%m%d_%H%M%S')}.zip"
    return bundle.getvalue(), name


RUNTIME_SETTINGS = load_runtime_settings()
LIVE_PRICES_TTL = max(1, int(RUNTIME_SETTINGS["ui"]["live_prices_ttl_seconds"]))
HISTORY_TTL = max(1, int(RUNTIME_SETTINGS["ui"]["history_ttl_seconds"]))
HISTORY_LIMIT = max(1, int(RUNTIME_SETTINGS["ui"]["history_limit"]))
API_TIMEOUT_SECONDS = max(1, int(RUNTIME_SETTINGS["ui"]["api_timeout_seconds"]))
HEALTH_TIMEOUT_SECONDS = max(1, int(RUNTIME_SETTINGS["ui"]["health_check_timeout_seconds"]))
BTC_PRICE_MIN = max(0, int(RUNTIME_SETTINGS["ui"]["btc_price_min"]))
BTC_PRICE_MAX = max(0, int(RUNTIME_SETTINGS["ui"]["btc_price_max"]))
PORTFOLIO_TOTAL_MIN = max(0, int(RUNTIME_SETTINGS["ui"]["portfolio_total_min"]))
PORTFOLIO_TOTAL_MAX = max(0, int(RUNTIME_SETTINGS["ui"]["portfolio_total_max"]))


def fmt_euro(value):
    return f"{value:,.2f} €".replace(",", " ")


def auto_create_khoms(conn, holding_id, asset_type, asset_name, buy_date, buy_price_unit, quantity):
    """Insert a pending Khoms debt (20%) for a gold/silver/btc holding."""
    if asset_type not in ("gold", "silver", "btc"):
        return
    amount = float(buy_price_unit) * float(quantity) * 0.20
    conn.execute(
        "INSERT INTO khoms_debts (holding_id, asset_type, asset_name, buy_date, amount, status, created_at) "
        "VALUES (?, ?, ?, ?, ?, 'pending', ?)",
        (
            holding_id,
            asset_type,
            asset_name,
            str(buy_date),
            amount,
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )


def get_btc_dca_settings(conn):
    row = conn.execute(
        """
        SELECT id, is_enabled, amount_eur, frequency, interval_count, anchor_date, weekday, month_day, last_run_at
        FROM btc_dca_settings
        WHERE id=1
        """
    ).fetchone()
    if not row:
        return {
            "id": 1,
            "is_enabled": 0,
            "amount_eur": 100.0,
            "frequency": "week",
            "interval_count": 1,
            "anchor_date": date.today().isoformat(),
            "weekday": 0,
            "month_day": 1,
            "last_run_at": None,
        }
    cols = [
        "id",
        "is_enabled",
        "amount_eur",
        "frequency",
        "interval_count",
        "anchor_date",
        "weekday",
        "month_day",
        "last_run_at",
    ]
    return dict(zip(cols, row))


def is_btc_dca_due(settings, now_utc):
    if int(settings.get("is_enabled", 0) or 0) != 1:
        return False
    amount = float(settings.get("amount_eur", 0.0) or 0.0)
    if amount <= 0:
        return False

    frequency = str(settings.get("frequency", "week") or "week").strip().lower()
    interval_count = max(1, int(settings.get("interval_count", 1) or 1))
    weekday = max(0, min(6, int(settings.get("weekday", 0) or 0)))
    month_day = max(1, min(28, int(settings.get("month_day", 1) or 1)))

    anchor_raw = str(settings.get("anchor_date", "") or "").strip()[:10]
    try:
        anchor = datetime.strptime(anchor_raw, "%Y-%m-%d").date()
    except Exception:
        anchor = date.today()

    today = now_utc.date()
    if today < anchor:
        return False

    last_run_raw = str(settings.get("last_run_at", "") or "").strip()
    if last_run_raw:
        try:
            last_run_date = datetime.strptime(last_run_raw[:10], "%Y-%m-%d").date()
            if last_run_date == today:
                return False
        except Exception:
            pass

    if frequency == "day":
        days_since_anchor = (today - anchor).days
        return days_since_anchor % interval_count == 0

    if frequency == "week":
        if today.weekday() != weekday:
            return False
        days_since_anchor = (today - anchor).days
        weeks_since_anchor = days_since_anchor // 7
        return weeks_since_anchor % interval_count == 0

    if frequency == "month":
        if today.day != month_day:
            return False
        months_since_anchor = (today.year - anchor.year) * 12 + (today.month - anchor.month)
        return months_since_anchor >= 0 and (months_since_anchor % interval_count == 0)

    return False


def run_btc_dca_if_due(conn, btc_price_eur):
    settings = get_btc_dca_settings(conn)
    now_utc = datetime.now(timezone.utc)
    if not is_btc_dca_due(settings, now_utc):
        return None

    price = float(btc_price_eur or 0.0)
    amount_eur = float(settings.get("amount_eur", 0.0) or 0.0)
    if price <= 0 or amount_eur <= 0:
        return None

    quantity = amount_eur / price
    buy_date_str = now_utc.date().isoformat()
    cur = conn.execute(
        "INSERT INTO holdings (asset_type, asset_name, buy_date, buy_price_unit, quantity) VALUES (?, ?, ?, ?, ?)",
        ("btc", "BTC", buy_date_str, price, quantity),
    )
    holding_id = cur.lastrowid
    auto_create_khoms(conn, holding_id, "btc", "BTC", buy_date_str, price, quantity)
    conn.execute(
        "UPDATE btc_dca_settings SET last_run_at=? WHERE id=1",
        (now_utc.strftime("%Y-%m-%d %H:%M:%S"),),
    )
    conn.commit()

    return {
        "amount_eur": amount_eur,
        "price": price,
        "quantity": quantity,
        "at": now_utc.strftime("%Y-%m-%d %H:%M:%S"),
    }


def get_active_asset_names(asset_type):
    rows = fetchall_dict(
        conn.execute(
            "SELECT DISTINCT asset_name FROM price_sources WHERE asset_type=? AND is_active=1 ORDER BY asset_name",
            (asset_type,),
        )
    )
    return [row["asset_name"] for row in rows]


def get_asset_name_choices(asset_type):
    # Fallback choices keep admin input usable even if a source is inactive/missing.
    defaults = {
        "gold": ["Gold Bar 100g", "Gold Maple Leaf", "Gold Bar 1oz"],
        "silver": ["Silver Maple Leaf"],
        "btc": ["BTC"],
    }
    active = get_active_asset_names(asset_type)
    merged = list(active)
    for name in defaults.get(asset_type, []):
        if name not in merged:
            merged.append(name)
    return merged


def get_asset_type_icon(asset_type):
    return {
        "gold": "🥇",
        "silver": "🥈",
        "btc": "₿",
    }.get(asset_type, asset_type)


def get_table_count(table_name):
    return conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]


def ensure_rich_portfolio_data():
    now_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    richer_holdings = [
        ("gold", "Gold Bar 100g", "2022-11-04", 5750.0, 1.0),
        ("gold", "Gold Bar 100g", "2023-08-15", 6020.0, 1.0),
        ("gold", "Gold Maple Leaf", "2024-01-13", 1980.0, 2.0),
        ("gold", "Gold Bar 1oz", "2025-02-20", 2480.0, 2.0),
        ("silver", "Silver Maple Leaf", "2022-10-01", 24.9, 140.0),
        ("silver", "Silver Maple Leaf", "2023-07-10", 27.1, 90.0),
        ("silver", "Silver Maple Leaf", "2024-09-30", 31.2, 110.0),
        ("btc", "BTC", "2022-06-18", 19500.0, 0.35),
        ("btc", "BTC", "2023-12-05", 36800.0, 0.18),
        ("btc", "BTC", "2025-01-23", 42000.0, 0.12),
    ]
    for row in richer_holdings:
        exists = conn.execute(
            "SELECT 1 FROM holdings WHERE asset_type=? AND asset_name=? AND buy_date=? AND buy_price_unit=? AND quantity=?",
            row,
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO holdings (asset_type, asset_name, buy_date, buy_price_unit, quantity) VALUES (?, ?, ?, ?, ?)",
                row,
            )

    richer_accounts = [
        ("Checking account", 12450.0, now_ts),
        ("Savings account", 17200.0, now_ts),
        ("Brokerage cash", 6200.0, now_ts),
        ("USD Account", 2800.0, now_ts),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO accounts (account_name, amount, updated_at) VALUES (?, ?, ?)",
        richer_accounts,
    )

    richer_receivables = [
        ("Family reimbursement", 1850.0, now_ts),
        ("Security deposit", 1200.0, now_ts),
        ("Annual bonus receivable", 3200.0, now_ts),
    ]
    for row in richer_receivables:
        exists = conn.execute(
            "SELECT 1 FROM receivables WHERE debtor=? AND amount=?",
            (row[0], row[1]),
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO receivables (debtor, amount, updated_at) VALUES (?, ?, ?)",
                row,
            )

    richer_debts = [
        ("Deferred card", 980.0, now_ts),
        ("Home improvement loan", 6400.0, now_ts),
        ("Car monthly payment", 1850.0, now_ts),
    ]
    for row in richer_debts:
        exists = conn.execute(
            "SELECT 1 FROM debts WHERE creditor=? AND amount=?",
            (row[0], row[1]),
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO debts (creditor, amount, updated_at) VALUES (?, ?, ?)",
                row,
            )

    history_count = conn.execute("SELECT COUNT(*) FROM portfolio_history").fetchone()[0]
    if history_count < 320:
        conn.execute("DELETE FROM portfolio_history")
        base_holdings = conn.execute("SELECT COALESCE(SUM(buy_price_unit * quantity), 0) FROM holdings").fetchone()[0] or 0.0
        base_cash = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM accounts").fetchone()[0] or 0.0
        base_receivables = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM receivables").fetchone()[0] or 0.0
        base_debts = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM debts").fetchone()[0] or 0.0
        base_khoms = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM khoms_debts WHERE status='pending'").fetchone()[0] or 0.0
        baseline = float(base_holdings + base_cash + base_receivables - base_debts - base_khoms)

        now_utc = datetime.now(timezone.utc).replace(microsecond=0)
        points = 380
        for i in range(points):
            ts = now_utc - timedelta(days=(points - i))
            wave_1 = 5200.0 * math.sin(i / 13.5)
            wave_2 = 2400.0 * math.cos(i / 29.0)
            seasonal = 1300.0 * math.sin(i / 58.0)
            drift = i * 36.0
            total = max(1000.0, baseline + wave_1 + wave_2 + seasonal + drift)
            conn.execute(
                "INSERT INTO portfolio_history (recorded_at, total_value) VALUES (?, ?)",
                (ts.strftime("%Y-%m-%dT%H:%M:%S"), total),
            )

    conn.commit()
def clear_admin_edit_state(prefix):
    keys = [
        f"{prefix}_edit_id",
        f"{prefix}_edit_original",
        f"{prefix}_name",
        f"{prefix}_amount",
    ]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]


def get_enabled_assets():
    return {"gold": True, "silver": True, "btc": True, "cash": True, "receivables": True, "debts": True}


def get_portfolio_summary():
    enabled = get_enabled_assets()
    holdings = fetchall_dict(
        conn.execute("SELECT asset_type, buy_price_unit, quantity FROM holdings")
    )
    totals = {"gold": 0.0, "silver": 0.0, "btc": 0.0}
    for row in holdings:
        asset_type = row["asset_type"]
        if asset_type in totals and enabled.get(asset_type, True):
            totals[asset_type] += float(row["buy_price_unit"]) * float(row["quantity"])

    cash = (conn.execute("SELECT COALESCE(SUM(amount), 0) FROM accounts").fetchone()[0] or 0.0) if enabled.get("cash") else 0.0
    receivables_total = (conn.execute("SELECT COALESCE(SUM(amount), 0) FROM receivables").fetchone()[0] or 0.0) if enabled.get("receivables") else 0.0
    debts_manual = (conn.execute("SELECT COALESCE(SUM(amount), 0) FROM debts").fetchone()[0] or 0.0) if enabled.get("debts") else 0.0
    khoms_pending = (conn.execute("SELECT COALESCE(SUM(amount), 0) FROM khoms_debts WHERE status='pending'").fetchone()[0] or 0.0) if enabled.get("debts") else 0.0
    debts = float(debts_manual) + float(khoms_pending)

    total = totals["gold"] + totals["silver"] + totals["btc"] + float(cash) + float(receivables_total) - debts
    return {
        "gold": totals["gold"],
        "silver": totals["silver"],
        "btc": totals["btc"],
        "cash": float(cash),
        "receiv": float(receivables_total),
        "receivables": float(receivables_total),
        "debts": float(debts),
        "total": total,
    }


def get_receivables_value(summary):
    return float(summary.get("receivables", summary.get("receiv", 0.0)))

if APP_DEMO_MODE and "rich_portfolio_seeded" not in st.session_state:
    ensure_rich_portfolio_data()
    st.session_state["rich_portfolio_seeded"] = True


@st.cache_data(ttl=LIVE_PRICES_TTL, show_spinner=False)
def fetch_live_prices():
    response = requests.get(f"{API_BASE_URL}/prices", timeout=API_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=HISTORY_TTL, show_spinner=False)
def fetch_history(limit=HISTORY_LIMIT):
    response = requests.get(f"{API_BASE_URL}/history?limit={limit}", timeout=API_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json().get("history", [])


dca_run_event = None
try:
    live_for_dca = fetch_live_prices()
    live_btc_for_dca = float((live_for_dca.get("prices", {}) or {}).get("btc", 0.0) or 0.0)
    dca_run_event = run_btc_dca_if_due(conn, live_btc_for_dca)
except Exception:
    dca_run_event = None


# --- SIDEBAR NAVIGATION ---
enabled_assets = get_enabled_assets()
menu_items = ["Home", "Assets", "Cash", "Receivables", "Debts", "Admin"]
if not (enabled_assets.get("gold") or enabled_assets.get("silver") or enabled_assets.get("btc")):
    menu_items.remove("Assets")
if not enabled_assets.get("cash"):
    menu_items.remove("Cash")
if not enabled_assets.get("receivables"):
    menu_items.remove("Receivables")
if not enabled_assets.get("debts"):
    menu_items.remove("Debts")

st.markdown('<div class="top-nav-title">Navigation</div>', unsafe_allow_html=True)
menu_slug_map = {
    "Home": "home",
    "Assets": "assets",
    "Cash": "cash",
    "Receivables": "receivables",
    "Debts": "debts",
    "Admin": "admin",
}
slug_menu_map = {slug: label for label, slug in menu_slug_map.items()}

requested_page = st.query_params.get("page", "")
if isinstance(requested_page, list):
    requested_page = requested_page[0] if requested_page else ""
requested_page = str(requested_page).strip().lower()

default_menu = slug_menu_map.get(requested_page, menu_items[0])
if default_menu not in menu_items:
    default_menu = menu_items[0]

if "menu_nav" not in st.session_state or st.session_state["menu_nav"] not in menu_items:
    st.session_state["menu_nav"] = default_menu


def _sync_menu_query_param():
    selected = st.session_state.get("menu_nav", menu_items[0])
    st.query_params["page"] = menu_slug_map.get(selected, "home")


st.radio(
    "Navigation",
    menu_items,
    horizontal=True,
    key="menu_nav",
    on_change=_sync_menu_query_param,
    label_visibility="collapsed",
)
menu = st.session_state.get("menu_nav", menu_items[0])
selected_slug = menu_slug_map.get(menu, "home")
if st.query_params.get("page", "") != selected_slug:
    st.query_params["page"] = selected_slug

# --- PAGES ---
if menu == "Home":
    portfolio_summary = get_portfolio_summary()
    live_payload = None
    market_totals = None
    refresh_age_seconds = None
    try:
        live_payload = fetch_live_prices()
        fetched_at = pd.to_datetime(live_payload["fetched_at"], utc=True, errors="coerce")
        if pd.notna(fetched_at):
            refresh_age_seconds = max(0, int((datetime.now(timezone.utc) - fetched_at.to_pydatetime()).total_seconds()))
        market_totals = live_payload.get("market_totals")
    except Exception as exc:
        st.warning(f"Live prices unavailable: {exc}")

    st.markdown('''
    <style>
    .dashboard-card {
        background: rgba(28, 35, 61, 0.95);
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.45);
    }
    .dashboard-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .dashboard-label {
        color: #9bb1ff;
        font-size: 1rem;
        margin-bottom: 0.4rem;
        font-weight: 500;
    }
    .dashboard-value {
        color: #f4f7ff;
        font-size: 1.4rem;
        font-weight: 700;
    }
    .dashboard-subvalue {
        color: #c9d7ff;
        font-size: 0.9rem;
        margin-top: 0.25rem;
        line-height: 1.25;
    }
    .dashboard-total {
        margin-top: 1rem;
        padding: 1rem;
        background: linear-gradient(90deg, #1f3c88, #3f72af);
        border-radius: 16px;
        text-align: center;
        color: #fff;
        font-size: 1.3rem;
        font-weight: 700;
        box-shadow: 0 4px 18px rgba(0,0,0,0.3);
    }
    </style>
    ''', unsafe_allow_html=True)
    home_totals = market_totals or portfolio_summary

    def asset_value_html(asset_key: str, tax_key: str) -> str:
        gross = float(home_totals.get(asset_key, 0.0) or 0.0)
        tax = float(home_totals.get(tax_key, 0.0) or 0.0)
        net = max(0.0, gross - tax)
        return (
            f"<div>Net: {fmt_euro(net)}</div>"
            f"<div class='dashboard-subvalue'>Brut: {fmt_euro(gross)}</div>"
        )

    gold_value_html = asset_value_html("gold", "gold_tax_estimated")
    silver_value_html = asset_value_html("silver", "silver_tax_estimated")
    btc_value_html = asset_value_html("btc", "btc_tax_estimated")

    cards = [
        {
            "label": "Gold",
            "icon": "🥇",
            "value": home_totals['gold'],
            "value_html": gold_value_html,
            "color": "#FFD700",
        },
        {
            "label": "Silver",
            "icon": "🥈",
            "value": home_totals['silver'],
            "value_html": silver_value_html,
            "color": "#C0C0C0",
        },
        {
            "label": "Bitcoin",
            "icon": "₿",
            "value": home_totals['btc'],
            "value_html": btc_value_html,
            "color": "#F7931A",
        },
        {"label": "Cash", "icon": "💶", "value": home_totals['cash'], "color": "#4CAF50"},
        {"label": "Receivables", "icon": "📥", "value": get_receivables_value(home_totals), "color": "#2196F3"},
        {"label": "Debts", "icon": "📤", "value": home_totals['debts'], "color": "#E53935"},
    ]
    for start in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, card in zip(cols, cards[start:start + 3]):
            with col:
                st.markdown(f'''
                <div class="dashboard-card" style="border-top: 4px solid {card['color']}">
                    <div class="dashboard-icon">{card['icon']}</div>
                    <div class="dashboard-label">{card['label']}</div>
                    <div class="dashboard-value">{card.get('value_html', fmt_euro(card['value']))}</div>
                </div>
                ''', unsafe_allow_html=True)
    total_display = float(home_totals.get("total", 0.0) or 0.0)
    taxes_estimated = float(home_totals.get("taxes_estimated", 0.0) or 0.0)
    total_gross = float(home_totals.get("total_gross", total_display) or 0.0)
    st.markdown(
        f'<div class="dashboard-total">Total: {fmt_euro(total_display)} </div>',
        unsafe_allow_html=True,
    )
    if refresh_age_seconds is not None:
        st.caption(f"Live sell prices updated {refresh_age_seconds} seconds ago.")

    live_prices = (live_payload or {}).get("prices", {})
    live_btc_price = float(live_prices.get("btc", 0.0) or 0.0)
    alert_messages = []
    if BTC_PRICE_MIN > 0 and live_btc_price < BTC_PRICE_MIN:
        alert_messages.append(f"BTC below min threshold: {fmt_euro(live_btc_price)} < {fmt_euro(BTC_PRICE_MIN)}")
    if BTC_PRICE_MAX > 0 and live_btc_price > BTC_PRICE_MAX:
        alert_messages.append(f"BTC above max threshold: {fmt_euro(live_btc_price)} > {fmt_euro(BTC_PRICE_MAX)}")
    if PORTFOLIO_TOTAL_MIN > 0 and float(home_totals["total"]) < PORTFOLIO_TOTAL_MIN:
        alert_messages.append(f"Portfolio below min threshold: {fmt_euro(home_totals['total'])} < {fmt_euro(PORTFOLIO_TOTAL_MIN)}")
    if PORTFOLIO_TOTAL_MAX > 0 and float(home_totals["total"]) > PORTFOLIO_TOTAL_MAX:
        alert_messages.append(f"Portfolio above max threshold: {fmt_euro(home_totals['total'])} > {fmt_euro(PORTFOLIO_TOTAL_MAX)}")

    if alert_messages:
        for message in alert_messages:
            st.warning(message)

    history = fetch_history()
    if history:
        history_df = pd.DataFrame(history)
        history_df["recorded_at"] = pd.to_datetime(history_df["recorded_at"], utc=True, errors="coerce")
        history_df = history_df.dropna(subset=["recorded_at"]).sort_values("recorded_at")
        if not history_df.empty:
            st.write("")
            h_left, h_right = st.columns([3, 5])
            with h_left:
                st.subheader("Total value evolution")
            with h_right:
                period = st.radio(
                    "Period",
                    ["7D", "1M", "3M", "1Y", "All"],
                    horizontal=True,
                    index=1,
                    label_visibility="collapsed",
                    key="chart_period",
                )

            now_utc = pd.Timestamp.now(tz="UTC")
            period_days = {"7D": 7, "1M": 30, "3M": 90, "1Y": 365, "All": None}
            resample_freq = {"7D": None, "1M": None, "3M": "6h", "1Y": "D", "All": "W"}

            days = period_days[period]
            filtered_df = history_df[history_df["recorded_at"] >= (now_utc - pd.Timedelta(days=days))] if days else history_df.copy()

            freq = resample_freq[period]
            if freq and not filtered_df.empty:
                filtered_df = (
                    filtered_df.set_index("recorded_at")["total_value"]
                    .resample(freq)
                    .mean()
                    .dropna()
                    .reset_index()
                )

            if filtered_df.empty:
                st.info("No data available for this period.")
            else:
                first_val = filtered_df["total_value"].iloc[0]
                last_val = filtered_df["total_value"].iloc[-1]
                delta = last_val - first_val
                delta_pct = (delta / first_val * 100) if first_val != 0 else 0
                sign = "+" if delta >= 0 else ""
                color = "green" if delta >= 0 else "red"
                arrow = "▲" if delta >= 0 else "▼"
                st.markdown(
                    f"<span style='color:{color}; font-weight:600;'>{arrow} {sign}{fmt_euro(delta)} ({sign}{delta_pct:.1f}%)</span> "
                    f"<span style='color:#9bb1ff; font-size:0.9em;'>over the selected period</span>",
                    unsafe_allow_html=True,
                )
                chart_df = filtered_df.rename(columns={"recorded_at": "Recorded date", "total_value": "Total value"})
                st.line_chart(chart_df, x="Recorded date", y="Total value", width="stretch", height=300)

# --- PAGE ASSETS ---
elif menu == "Assets":
    labels = []
    assets = []
    if enabled_assets.get("gold"):
        labels.append("Gold")
        assets.append("gold")
    if enabled_assets.get("silver"):
        labels.append("Silver")
        assets.append("silver")
    if enabled_assets.get("btc"):
        labels.append("Bitcoin")
        assets.append("btc")

    tab = st.tabs(labels)
    for i, asset_type in enumerate(assets):
        with tab[i]:
            rows = fetchall_dict(
                conn.execute(
                    "SELECT asset_name AS Asset, buy_date AS 'Buy date', buy_price_unit AS 'Buy price', quantity AS Quantity FROM holdings WHERE asset_type=? ORDER BY buy_date DESC",
                    (asset_type,),
                )
            )
            if rows:
                asset_df = pd.DataFrame(rows)
                asset_df["Total buy"] = asset_df["Buy price"].astype(float) * asset_df["Quantity"].astype(float)
                latest_buy = str(asset_df["Buy date"].iloc[0])
                total_buy = float(asset_df["Total buy"].sum())
                total_qty = float(asset_df["Quantity"].sum())
                lines_count = int(len(asset_df))

                st.markdown(
                    f"""
                    <div class="mini-stat-grid">
                        <div class="mini-stat-card"><span>Lines</span><strong>{lines_count}</strong></div>
                        <div class="mini-stat-card"><span>Total quantity</span><strong>{total_qty:.2f}</strong></div>
                        <div class="mini-stat-card"><span>Total buy value</span><strong>{fmt_euro(total_buy)}</strong></div>
                        <div class="mini-stat-card"><span>Latest buy</span><strong>{latest_buy}</strong></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                display_df = asset_df.copy()
                display_df["Buy price"] = display_df["Buy price"].map(fmt_euro)
                display_df["Total buy"] = display_df["Total buy"].map(fmt_euro)
                st.dataframe(display_df, width="stretch", hide_index=True)
            else:
                st.info("No assets in this category.")

# --- PAGE CASH ---
elif menu == "Cash":
    rows = fetchall_dict(conn.execute("SELECT account_name AS Account, amount AS Amount, updated_at AS 'Updated at' FROM accounts ORDER BY account_name"))
    if rows:
        cash_df = pd.DataFrame(rows)
        total_cash = float(cash_df["Amount"].sum())
        max_idx = cash_df["Amount"].astype(float).idxmax()
        top_account = str(cash_df.loc[max_idx, "Account"])
        top_amount = float(cash_df.loc[max_idx, "Amount"])

        st.markdown(
            f"""
            <div class="mini-stat-grid">
                <div class="mini-stat-card"><span>Accounts</span><strong>{len(cash_df)}</strong></div>
                <div class="mini-stat-card"><span>Total cash</span><strong>{fmt_euro(total_cash)}</strong></div>
                <div class="mini-stat-card"><span>Top account</span><strong>{top_account}</strong></div>
                <div class="mini-stat-card"><span>Top amount</span><strong>{fmt_euro(top_amount)}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        show_df = cash_df.copy()
        show_df["Amount"] = show_df["Amount"].map(fmt_euro)
        st.dataframe(show_df, width="stretch", hide_index=True)
    else:
        st.info("No cash accounts.")

# --- PAGE RECEIVABLES ---
elif menu == "Receivables":
    rows = fetchall_dict(conn.execute("SELECT debtor AS Debtor, amount AS Amount, updated_at AS 'Updated at' FROM receivables ORDER BY amount DESC"))
    if rows:
        recv_df = pd.DataFrame(rows)
        total_recv = float(recv_df["Amount"].sum())
        top_debtor = str(recv_df.iloc[0]["Debtor"])
        top_recv = float(recv_df.iloc[0]["Amount"])
        st.markdown(
            f"""
            <div class="mini-stat-grid">
                <div class="mini-stat-card"><span>Debtors</span><strong>{len(recv_df)}</strong></div>
                <div class="mini-stat-card"><span>Total receivables</span><strong>{fmt_euro(total_recv)}</strong></div>
                <div class="mini-stat-card"><span>Top debtor</span><strong>{top_debtor}</strong></div>
                <div class="mini-stat-card"><span>Top amount</span><strong>{fmt_euro(top_recv)}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        show_df = recv_df.copy()
        show_df["Amount"] = show_df["Amount"].map(fmt_euro)
        st.dataframe(show_df, width="stretch", hide_index=True)
    else:
        st.info("No receivables.")

# --- PAGE DEBTS ---
elif menu == "Debts":
    debts_tab, khoms_pending_tab, khoms_history_tab = st.tabs(["📋 Debts", "⏳ Pending Khoms", "✅ Khoms History"])

    with debts_tab:
        rows = fetchall_dict(conn.execute("SELECT creditor AS Creditor, amount AS Amount, updated_at AS 'Updated at' FROM debts ORDER BY amount DESC"))
        if rows:
            debt_df = pd.DataFrame(rows)
            total_debts = float(debt_df["Amount"].sum())
            top_creditor = str(debt_df.iloc[0]["Creditor"])
            top_debt = float(debt_df.iloc[0]["Amount"])
            st.markdown(
                f"""
                <div class="mini-stat-grid">
                    <div class="mini-stat-card"><span>Manual debts</span><strong>{len(debt_df)}</strong></div>
                    <div class="mini-stat-card"><span>Total manual debts</span><strong>{fmt_euro(total_debts)}</strong></div>
                    <div class="mini-stat-card"><span>Top creditor</span><strong>{top_creditor}</strong></div>
                    <div class="mini-stat-card"><span>Top amount</span><strong>{fmt_euro(top_debt)}</strong></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            show_df = debt_df.copy()
            show_df["Amount"] = show_df["Amount"].map(fmt_euro)
            st.dataframe(show_df, width="stretch", hide_index=True)
        else:
            st.info("No manual debt entries.")

    with khoms_pending_tab:
        pending = fetchall_dict(conn.execute(
            "SELECT id, asset_type, asset_name, buy_date, amount, created_at "
            "FROM khoms_debts WHERE status='pending' ORDER BY created_at DESC"
        ))
        if not pending:
            st.info("No pending Khoms - all eligible assets were settled.")
        else:
            total_pending = sum(r["amount"] for r in pending)
            st.markdown(f"### Total to settle: {fmt_euro(total_pending)}")
            st.write("")
            for row in pending:
                c1, c2, c3, c4, c5 = st.columns([2.5, 1.6, 1.8, 2.8, 1.4])
                with c1:
                    icon = {"gold": "🥇", "silver": "🥈", "btc": "₿"}.get(row["asset_type"], "💰")
                    icon_col, text_col = st.columns([0.18, 0.82])
                    with icon_col:
                        st.markdown(
                            f"<div style='width:1.4rem; text-align:center; font-size:1.15rem; line-height:1.4rem;'>{icon}</div>",
                            unsafe_allow_html=True,
                        )
                    with text_col:
                        st.write(f"**{row['asset_name']}** ({row['asset_type'].upper()})")
                with c2:
                    st.write(fmt_euro(row["amount"]))
                with c3:
                    st.caption(f"Purchase: {row['buy_date']}")
                with c4:
                    note = st.text_input(
                        "Note",
                        key=f"khoms_note_{row['id']}",
                        label_visibility="collapsed",
                        placeholder="Payment note (optional)",
                    )
                with c5:
                    if st.button("✅ Mark as paid", key=f"khoms_pay_{row['id']}"):
                        conn.execute(
                            "UPDATE khoms_debts SET status='paid', paid_at=?, note=? WHERE id=?",
                            (datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), note or None, row["id"]),
                        )
                        conn.commit()
                        st.success(f"Khoms settled for {row['asset_name']}")
                        st.rerun()

    with khoms_history_tab:
        paid = fetchall_dict(conn.execute(
            "SELECT asset_type, asset_name, buy_date, amount, paid_at, note "
            "FROM khoms_debts WHERE status='paid' ORDER BY paid_at DESC"
        ))
        if not paid:
            st.info("No Khoms payment recorded yet.")
        else:
            total_paid = sum(r["amount"] for r in paid)
            st.markdown(f"### Total settled: {fmt_euro(total_paid)}")
            df_paid = pd.DataFrame([{
                "Type": r["asset_type"].upper(),
                "Asset": r["asset_name"],
                "Buy date": r["buy_date"],
                "Amount": fmt_euro(r["amount"]),
                "Paid on": (r["paid_at"] or "")[:10],
                "Note": r["note"] or "",
            } for r in paid])
            st.dataframe(df_paid, width="stretch", hide_index=True)

# --- PAGE ADMIN ---
elif menu == "Admin":
    st.caption("Manage positions and display settings.")

    if APP_ADMIN_PASSWORD:
        if "admin_authenticated" not in st.session_state:
            st.session_state["admin_authenticated"] = False
        if not st.session_state["admin_authenticated"]:
            with st.form("admin_login"):
                admin_password_input = st.text_input("Admin password", type="password")
                submitted_login = st.form_submit_button("Sign in")
                if submitted_login:
                    if admin_password_input == APP_ADMIN_PASSWORD:
                        st.session_state["admin_authenticated"] = True
                        st.success("Admin access granted")
                        st.rerun()
                    else:
                        st.error("Invalid password")
            st.stop()

    st.subheader("Position management")
    admin_section = st.segmented_control(
        "Admin section",
        ["Assets", "Cash", "Receivables", "Debts"],
        default="Assets",
        key="admin_section",
        label_visibility="collapsed",
    )
    if admin_section == "Assets":
        with st.container(border=True):
            allowed_asset_types = [asset_type for asset_type in ["gold", "silver", "btc"] if enabled_assets.get(asset_type, True)]
            asset_type_icons = [get_asset_type_icon(asset_type) for asset_type in allowed_asset_types]
            selected_asset_icon = st.segmented_control(
                "Asset type",
                asset_type_icons,
                default=get_asset_type_icon(allowed_asset_types[0]) if allowed_asset_types else None,
                key="admin_asset_type_icon",
                label_visibility="collapsed",
            )
            asset_type = next(
                asset_key for asset_key in allowed_asset_types if get_asset_type_icon(asset_key) == selected_asset_icon
            )
            asset_name_options = get_asset_name_choices(asset_type)
            previous_asset_type = st.session_state.get("admin_asset_type_prev")
            if previous_asset_type != asset_type:
                if asset_type == "btc":
                    st.session_state["admin_asset_name"] = "BTC"
                elif asset_name_options:
                    st.session_state["admin_asset_name"] = asset_name_options[0]
                else:
                    st.session_state["admin_asset_name"] = ""
                st.session_state["admin_asset_type_prev"] = asset_type

            current_asset_name = st.session_state.get("admin_asset_name", "")
            if asset_type != "btc" and asset_name_options and current_asset_name not in asset_name_options:
                st.session_state["admin_asset_name"] = asset_name_options[0]

            form_col_1, form_col_2 = st.columns(2)
            with form_col_1:
                if asset_type == "btc":
                    asset_name = "BTC"
                    st.text_input("Asset", value=asset_name, disabled=True, key="admin_asset_name_btc")
                elif asset_name_options:
                    asset_name = st.selectbox("Asset", asset_name_options, key="admin_asset_name")
                else:
                    asset_name = st.text_input("Asset", key="admin_asset_name")
                buy_date = st.date_input("Buy date", value=date.today(), key="admin_buy_date")
            with form_col_2:
                buy_price_unit = st.number_input("Unit buy price", min_value=0.0, step=0.01, key="admin_buy_price_unit")
                quantity = st.number_input("Quantity", min_value=0.01, step=0.01, value=1.0, key="admin_quantity")

            if st.button("Add asset", key="admin_add_asset"):
                if asset_name and buy_price_unit > 0 and quantity > 0:
                    cur = conn.execute(
                        "INSERT INTO holdings (asset_type, asset_name, buy_date, buy_price_unit, quantity) VALUES (?, ?, ?, ?, ?)",
                        (asset_type, asset_name, str(buy_date), buy_price_unit, quantity),
                    )
                    holding_id = cur.lastrowid
                    auto_create_khoms(conn, holding_id, asset_type, asset_name, str(buy_date), buy_price_unit, quantity)
                    conn.commit()
                    extra = " - 20% Khoms created automatically" if asset_type in ("gold", "silver", "btc") else ""
                    st.success(f"Asset added{extra}")
                    st.rerun()
                else:
                    st.warning("Valid name, price and quantity are required")

        st.caption("Bitcoin DCA automation")
        dca_settings = get_btc_dca_settings(conn)
        dca_frequency_labels = {"day": "Day", "week": "Week", "month": "Month"}
        weekday_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        with st.form("btc_dca_settings_form"):
            dca_enabled = st.checkbox("Enable BTC DCA", value=bool(int(dca_settings.get("is_enabled", 0) or 0)))
            dca_col_1, dca_col_2, dca_col_3 = st.columns(3)
            with dca_col_1:
                dca_amount_eur = st.number_input(
                    "Amount per execution (EUR)",
                    min_value=0.0,
                    step=10.0,
                    value=float(dca_settings.get("amount_eur", 100.0) or 100.0),
                )
            with dca_col_2:
                dca_frequency = st.selectbox(
                    "Frequency",
                    ["day", "week", "month"],
                    index=["day", "week", "month"].index(str(dca_settings.get("frequency", "week") or "week")),
                    format_func=lambda x: dca_frequency_labels.get(x, x.title()),
                )
            with dca_col_3:
                dca_interval_count = st.number_input(
                    "Every N periods",
                    min_value=1,
                    max_value=365,
                    step=1,
                    value=max(1, int(dca_settings.get("interval_count", 1) or 1)),
                )

            dca_anchor_date = st.date_input(
                "Anchor date",
                value=datetime.strptime(
                    str(dca_settings.get("anchor_date", date.today().isoformat()) or date.today().isoformat())[:10],
                    "%Y-%m-%d",
                ).date(),
            )

            dca_weekday = int(dca_settings.get("weekday", 0) or 0)
            dca_month_day = int(dca_settings.get("month_day", 1) or 1)
            if dca_frequency == "week":
                dca_weekday = weekday_labels.index(
                    st.selectbox("Execution weekday", weekday_labels, index=max(0, min(6, dca_weekday)))
                )
            elif dca_frequency == "month":
                dca_month_day = st.number_input(
                    "Execution day in month",
                    min_value=1,
                    max_value=28,
                    step=1,
                    value=max(1, min(28, dca_month_day)),
                )

            dca_save = st.form_submit_button("Save DCA settings")
            if dca_save:
                conn.execute(
                    """
                    UPDATE btc_dca_settings
                    SET is_enabled=?, amount_eur=?, frequency=?, interval_count=?, anchor_date=?, weekday=?, month_day=?
                    WHERE id=1
                    """,
                    (
                        1 if dca_enabled else 0,
                        float(dca_amount_eur),
                        str(dca_frequency),
                        int(dca_interval_count),
                        str(dca_anchor_date),
                        int(dca_weekday),
                        int(dca_month_day),
                    ),
                )
                conn.commit()
                st.success("BTC DCA settings saved")
                st.rerun()

        dca_last_run_at = str(dca_settings.get("last_run_at", "") or "").strip()
        if dca_last_run_at:
            st.caption(f"Last DCA execution: {dca_last_run_at} UTC")
        else:
            st.caption("Last DCA execution: never")

        if dca_run_event:
            st.success(
                "BTC DCA executed automatically - "
                f"{fmt_euro(dca_run_event['amount_eur'])} at {fmt_euro(dca_run_event['price'])} "
                f"for {dca_run_event['quantity']:.8f} BTC"
            )

        st.caption("Existing assets")
        holdings_rows = fetchall_dict(
            conn.execute(
                "SELECT h.id, h.asset_type, h.asset_name, h.buy_date, h.buy_price_unit, h.quantity, "
                "COALESCE(k.amount, 0) AS khoms_amount "
                "FROM holdings h "
                "LEFT JOIN khoms_debts k ON k.holding_id = h.id AND k.status='pending' "
                "ORDER BY h.buy_date DESC, h.id DESC"
            )
        )
        if holdings_rows:
            grouped_holdings = {"gold": [], "silver": [], "btc": []}
            for row in holdings_rows:
                grouped_holdings.setdefault(row["asset_type"], []).append(row)

            section_meta = [
                ("gold", "Gold", "🥇"),
                ("silver", "Silver", "🥈"),
                ("btc", "BTC", "₿"),
            ]

            available_sections = [label for asset_key, label, _icon in section_meta if grouped_holdings.get(asset_key)]
            selected_existing_asset_type = st.segmented_control(
                "Existing asset type",
                available_sections,
                default=available_sections[0] if available_sections else None,
                key="existing_assets_section",
                label_visibility="collapsed",
            )

            selected_asset_key = next(
                asset_key for asset_key, label, _icon in section_meta if label == selected_existing_asset_type
            )
            selected_section_icon = next(
                icon for asset_key, _label, icon in section_meta if asset_key == selected_asset_key
            )
            selected_rows = grouped_holdings.get(selected_asset_key, [])

            for row in selected_rows:
                col_1, col_2, col_3, col_4, col_5, col_6 = st.columns([2.4, 1.3, 1.3, 1.2, 1.3, 0.9])
                with col_1:
                    icon = {"gold": "🥇", "silver": "🥈", "btc": "₿"}.get(row["asset_type"], "💰")
                    st.write(f"{icon} {row['asset_name']}")
                    st.caption(f"{row['asset_type'].upper()} • {row['buy_date']}")
                with col_2:
                    st.write(fmt_euro(row["buy_price_unit"]))
                    st.caption("Buy price")
                with col_3:
                    st.write(row["quantity"])
                    st.caption("Quantity")
                with col_4:
                    st.write(fmt_euro(float(row["buy_price_unit"]) * float(row["quantity"])))
                    st.caption("Total buy")
                with col_5:
                    st.write(fmt_euro(row["khoms_amount"]))
                    st.caption("Pending Khoms")
                with col_6:
                    if st.button("🗑", key=f"delete_asset_{row['id']}"):
                        conn.execute("DELETE FROM khoms_debts WHERE holding_id=? AND status='pending'", (row["id"],))
                        conn.execute("DELETE FROM holdings WHERE id=?", (row["id"],))
                        conn.commit()
                        st.success("Asset deleted")
                        st.rerun()
                st.markdown("<div class='admin-row-separator'></div>", unsafe_allow_html=True)
        else:
            st.caption("No assets to delete")

    elif admin_section == "Cash":
        cash_editing = st.session_state.get("cash_edit_original") is not None
        cash_mode = st.radio("Update mode", ["Absolute amount", "Delta (+/-)"], horizontal=True, key="cash_mode")
        with st.form("admin_manage_cash"):
            account_name = st.text_input("Account", value=st.session_state.get("cash_name", ""))
            amount = st.number_input(
                "Balance" if cash_mode == "Absolute amount" else "Delta",
                step=0.01,
                value=float(st.session_state.get("cash_amount", 0.0)) if cash_mode == "Absolute amount" else 0.0,
            )
            submitted = st.form_submit_button("Update" if cash_editing else "Add / update")
            if submitted:
                if account_name:
                    original_name = st.session_state.get("cash_edit_original")
                    if original_name and original_name != account_name:
                        conn.execute("DELETE FROM accounts WHERE account_name=?", (original_name,))
                    base_row = conn.execute("SELECT amount FROM accounts WHERE account_name=?", (account_name,)).fetchone()
                    base_amount = float(base_row[0]) if base_row else 0.0
                    final_amount = amount if cash_mode == "Absolute amount" else base_amount + amount
                    conn.execute(
                        "INSERT OR REPLACE INTO accounts (account_name, amount, updated_at) VALUES (?, ?, ?)",
                        (account_name, final_amount, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")),
                    )
                    conn.commit()
                    clear_admin_edit_state("cash")
                    st.success("Cash balance saved")
                    st.rerun()
                else:
                    st.warning("Account name is required")

        st.caption("Existing accounts")
        cash_rows = fetchall_dict(conn.execute("SELECT account_name, amount, updated_at FROM accounts ORDER BY account_name"))
        if cash_rows:
            st.markdown(f"### Total cash: {fmt_euro(sum(row['amount'] for row in cash_rows))}")
            for row in cash_rows:
                col_1, col_2, col_3, col_4 = st.columns([3.6, 1.8, 0.8, 0.8])
                with col_1:
                    st.write(f"🏦 {row['account_name']}")
                    st.caption(f"Updated on {row['updated_at']}")
                with col_2:
                    st.write(fmt_euro(row["amount"]))
                    st.caption("Current balance")
                with col_3:
                    if st.button("✏️", key=f"edit_cash_{row['account_name']}"):
                        st.session_state["cash_edit_original"] = row["account_name"]
                        st.session_state["cash_name"] = row["account_name"]
                        st.session_state["cash_amount"] = float(row["amount"])
                        st.rerun()
                with col_4:
                    if st.button("🗑", key=f"del_cash_{row['account_name']}"):
                        conn.execute("DELETE FROM accounts WHERE account_name=?", (row["account_name"],))
                        conn.commit()
                        if st.session_state.get("cash_edit_original") == row["account_name"]:
                            clear_admin_edit_state("cash")
                        st.success("Account deleted")
                        st.rerun()
                st.markdown("<div class='admin-row-separator'></div>", unsafe_allow_html=True)
        else:
            st.caption("No accounts")

    elif admin_section == "Receivables":
        receivables_editing = st.session_state.get("receivables_edit_id") is not None
        receivables_mode = st.radio("Update mode", ["Absolute amount", "Delta (+/-)"], horizontal=True, key="receivables_mode")
        with st.form("admin_manage_receivables"):
            debtor = st.text_input("Debtor", value=st.session_state.get("receivables_name", ""))
            amount = st.number_input(
                "Amount" if receivables_mode == "Absolute amount" else "Delta",
                step=0.01,
                value=float(st.session_state.get("receivables_amount", 0.0)) if receivables_mode == "Absolute amount" else 0.0,
            )
            submitted = st.form_submit_button("Update" if receivables_editing else "Add")
            if submitted:
                if debtor:
                    row_id = st.session_state.get("receivables_edit_id")
                    if row_id:
                        base_row = conn.execute("SELECT amount FROM receivables WHERE id=?", (row_id,)).fetchone()
                        base_amount = float(base_row[0]) if base_row else 0.0
                        final_amount = amount if receivables_mode == "Absolute amount" else base_amount + amount
                        conn.execute(
                            "UPDATE receivables SET debtor=?, amount=?, updated_at=? WHERE id=?",
                            (debtor, final_amount, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), row_id),
                        )
                        msg = "Receivable updated"
                    else:
                        conn.execute(
                            "INSERT INTO receivables (debtor, amount, updated_at) VALUES (?, ?, ?)",
                            (debtor, amount, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")),
                        )
                        msg = "Receivable added"
                    conn.commit()
                    clear_admin_edit_state("receivables")
                    st.success(msg)
                    st.rerun()
                else:
                    st.warning("Debtor is required")

        st.caption("Existing receivables")
        receivable_rows = fetchall_dict(conn.execute("SELECT id, debtor, amount, updated_at FROM receivables ORDER BY amount DESC, id DESC"))
        if receivable_rows:
            st.markdown(f"### Total receivables: {fmt_euro(sum(row['amount'] for row in receivable_rows))}")
            for row in receivable_rows:
                col_1, col_2, col_3, col_4 = st.columns([3.6, 1.8, 0.8, 0.8])
                with col_1:
                    st.write(f"📥 {row['debtor']}")
                    st.caption(f"Updated on {row['updated_at']}")
                with col_2:
                    st.write(fmt_euro(row["amount"]))
                    st.caption("Amount to receive")
                with col_3:
                    if st.button("✏️", key=f"edit_recv_{row['id']}"):
                        st.session_state["receivables_edit_id"] = row["id"]
                        st.session_state["receivables_name"] = row["debtor"]
                        st.session_state["receivables_amount"] = float(row["amount"])
                        st.rerun()
                with col_4:
                    if st.button("🗑", key=f"del_recv_{row['id']}"):
                        conn.execute("DELETE FROM receivables WHERE id=?", (row["id"],))
                        conn.commit()
                        if st.session_state.get("receivables_edit_id") == row["id"]:
                            clear_admin_edit_state("receivables")
                        st.success("Receivable deleted")
                        st.rerun()
                st.markdown("<div class='admin-row-separator'></div>", unsafe_allow_html=True)
        else:
            st.caption("No receivables")

    elif admin_section == "Debts":
        debts_editing = st.session_state.get("debts_edit_id") is not None
        debts_mode = st.radio("Update mode", ["Absolute amount", "Delta (+/-)"], horizontal=True, key="debts_mode")
        with st.form("admin_manage_debts"):
            creditor = st.text_input("Creditor", value=st.session_state.get("debts_name", ""))
            amount = st.number_input(
                "Amount" if debts_mode == "Absolute amount" else "Delta",
                step=0.01,
                value=float(st.session_state.get("debts_amount", 0.0)) if debts_mode == "Absolute amount" else 0.0,
            )
            submitted = st.form_submit_button("Update" if debts_editing else "Add")
            if submitted:
                if creditor:
                    row_id = st.session_state.get("debts_edit_id")
                    if row_id:
                        base_row = conn.execute("SELECT amount FROM debts WHERE id=?", (row_id,)).fetchone()
                        base_amount = float(base_row[0]) if base_row else 0.0
                        final_amount = amount if debts_mode == "Absolute amount" else base_amount + amount
                        conn.execute(
                            "UPDATE debts SET creditor=?, amount=?, updated_at=? WHERE id=?",
                            (creditor, final_amount, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), row_id),
                        )
                        msg = "Debt updated"
                    else:
                        conn.execute(
                            "INSERT INTO debts (creditor, amount, updated_at) VALUES (?, ?, ?)",
                            (creditor, amount, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")),
                        )
                        msg = "Debt added"
                    conn.commit()
                    clear_admin_edit_state("debts")
                    st.success(msg)
                    st.rerun()
                else:
                    st.warning("Creditor is required")

        st.caption("Existing debts")
        debt_rows = fetchall_dict(conn.execute("SELECT id, creditor, amount, updated_at FROM debts ORDER BY amount DESC, id DESC"))
        if debt_rows:
            st.markdown(f"### Total manual debts: {fmt_euro(sum(row['amount'] for row in debt_rows))}")
            for row in debt_rows:
                col_1, col_2, col_3, col_4 = st.columns([3.6, 1.8, 0.8, 0.8])
                with col_1:
                    st.write(f"📤 {row['creditor']}")
                    st.caption(f"Updated on {row['updated_at']}")
                with col_2:
                    st.write(fmt_euro(row["amount"]))
                    st.caption("Amount to pay")
                with col_3:
                    if st.button("✏️", key=f"edit_debt_{row['id']}"):
                        st.session_state["debts_edit_id"] = row["id"]
                        st.session_state["debts_name"] = row["creditor"]
                        st.session_state["debts_amount"] = float(row["amount"])
                        st.rerun()
                with col_4:
                    if st.button("🗑", key=f"del_debt_{row['id']}"):
                        conn.execute("DELETE FROM debts WHERE id=?", (row["id"],))
                        conn.commit()
                        if st.session_state.get("debts_edit_id") == row["id"]:
                            clear_admin_edit_state("debts")
                        st.success("Debt deleted")
                        st.rerun()
                st.markdown("<div class='admin-row-separator'></div>", unsafe_allow_html=True)
        else:
            st.caption("No debts")

    st.subheader("Maintenance")
    st.caption("Dynamic settings managed via local JSON: data/runtime_settings.json")
    st.markdown(
        """
        <div class="maintenance-hero">
            <h4>Maintenance Console</h4>
            <p>Monitoring, backup, restore, and critical admin actions from one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    maintenance_tab_ops, maintenance_tab_settings, maintenance_tab_data, maintenance_tab_purge = st.tabs(
        ["Ops", "Dynamic settings", "Data & Export", "Purge"]
    )

    with maintenance_tab_settings:
        with st.form("runtime_settings_form"):
            st.markdown("### Dynamic settings")
            settings_col_1, settings_col_2 = st.columns(2)
            with settings_col_1:
                ui_live_ttl = st.number_input(
                    "UI live price TTL (seconds)",
                    min_value=1,
                    max_value=600,
                    value=int(RUNTIME_SETTINGS["ui"]["live_prices_ttl_seconds"]),
                    step=1,
                )
                ui_history_ttl = st.number_input(
                    "UI history TTL (seconds)",
                    min_value=1,
                    max_value=600,
                    value=int(RUNTIME_SETTINGS["ui"]["history_ttl_seconds"]),
                    step=1,
                )
                ui_history_limit = st.number_input(
                    "History max points",
                    min_value=50,
                    max_value=5000,
                    value=int(RUNTIME_SETTINGS["ui"]["history_limit"]),
                    step=50,
                )
            with settings_col_2:
                ui_api_timeout = st.number_input(
                    "UI API timeout (seconds)",
                    min_value=1,
                    max_value=120,
                    value=int(RUNTIME_SETTINGS["ui"]["api_timeout_seconds"]),
                    step=1,
                )
                ui_health_timeout = st.number_input(
                    "UI healthcheck timeout (seconds)",
                    min_value=1,
                    max_value=120,
                    value=int(RUNTIME_SETTINGS["ui"]["health_check_timeout_seconds"]),
                    step=1,
                )
                api_cache_ttl = st.number_input(
                    "API cache TTL (seconds)",
                    min_value=10,
                    max_value=3600,
                    value=int(RUNTIME_SETTINGS["pricing_api"]["cache_ttl_seconds"]),
                    step=10,
                )
                api_request_timeout = st.number_input(
                    "API external request timeout (seconds)",
                    min_value=1,
                    max_value=120,
                    value=int(RUNTIME_SETTINGS["pricing_api"]["request_timeout_seconds"]),
                    step=1,
                )
                api_request_retries = st.number_input(
                    "API external request retries",
                    min_value=1,
                    max_value=10,
                    value=int(RUNTIME_SETTINGS["pricing_api"]["request_retries"]),
                    step=1,
                )
                api_request_backoff = st.number_input(
                    "API retry backoff (seconds)",
                    min_value=1,
                    max_value=30,
                    value=int(RUNTIME_SETTINGS["pricing_api"]["request_backoff_seconds"]),
                    step=1,
                )

            save_settings = st.form_submit_button("Save settings")
            if save_settings:
                payload = {
                    "ui": {
                        "live_prices_ttl_seconds": int(ui_live_ttl),
                        "history_ttl_seconds": int(ui_history_ttl),
                        "history_limit": int(ui_history_limit),
                        "api_timeout_seconds": int(ui_api_timeout),
                        "health_check_timeout_seconds": int(ui_health_timeout),
                        "btc_price_min": int(RUNTIME_SETTINGS["ui"]["btc_price_min"]),
                        "btc_price_max": int(RUNTIME_SETTINGS["ui"]["btc_price_max"]),
                        "portfolio_total_min": int(RUNTIME_SETTINGS["ui"]["portfolio_total_min"]),
                        "portfolio_total_max": int(RUNTIME_SETTINGS["ui"]["portfolio_total_max"]),
                    },
                    "pricing_api": {
                        "cache_ttl_seconds": int(api_cache_ttl),
                        "request_timeout_seconds": int(api_request_timeout),
                        "request_retries": int(api_request_retries),
                        "request_backoff_seconds": int(api_request_backoff),
                    },
                }
                save_runtime_settings(payload)
                fetch_live_prices.clear()
                fetch_history.clear()
                append_admin_audit_log("save_runtime_settings", "ok", "settings updated from admin")
                st.success("Settings saved. Restart the API to apply pricing_api fields.")
                st.rerun()

    counts = {
        "Assets": conn.execute("SELECT COUNT(*) FROM holdings").fetchone()[0],
        "Accounts": conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0],
        "Receivables": conn.execute("SELECT COUNT(*) FROM receivables").fetchone()[0],
        "Debts": conn.execute("SELECT COUNT(*) FROM debts").fetchone()[0],
        "History": conn.execute("SELECT COUNT(*) FROM portfolio_history").fetchone()[0],
        "Khoms": conn.execute("SELECT COUNT(*) FROM khoms_debts").fetchone()[0],
        "Price sources": conn.execute("SELECT COUNT(*) FROM price_sources").fetchone()[0],
    }

    live_for_health = None
    try:
        live_for_health = fetch_live_prices()
    except Exception:
        live_for_health = None
    source_rows = (live_for_health or {}).get("assets", [])
    source_health = (live_for_health or {}).get("source_health", {})
    history_preview_values = []
    try:
        history_preview = fetch_history(limit=60)
        history_preview_values = [
            float(item.get("total_value", 0.0) or 0.0)
            for item in history_preview
            if isinstance(item, dict)
        ]
    except Exception:
        history_preview_values = []
    history_sparkline = sparkline(history_preview_values)
    backups_dir = os.path.join(os.path.dirname(__file__), "data", "backups")
    backup_files = []
    if os.path.exists(backups_dir):
        backup_files = sorted(
            [name for name in os.listdir(backups_dir) if name.endswith(".db")],
            reverse=True,
        )

    with maintenance_tab_ops:
        st.markdown("### Platform status")
        st.markdown(
            f"""
            <div class="ops-kpi-strip">
                <div class="ops-kpi-card"><span>🗃 Total DB rows</span><strong>{sum(counts.values())}</strong></div>
                <div class="ops-kpi-card"><span>✅ Healthy sources</span><strong>{int(source_health.get('ok', 0) or 0)}</strong></div>
                <div class="ops-kpi-card"><span>⚠ Failing sources</span><strong>{int(source_health.get('error', 0) or 0)}</strong></div>
                <div class="ops-kpi-card"><span>📈 History points</span><strong>{counts['History']}</strong><span>{history_sparkline}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(
            [{"Table": key, "Rows": value} for key, value in counts.items()],
            width="stretch",
            hide_index=True,
        )

        if source_rows:
            st.caption("Detailed source health")
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Type": row.get("asset_type", ""),
                            "Asset": row.get("asset_name", ""),
                            "Status": row.get("status", ""),
                            "Latency ms": row.get("latency_ms", ""),
                            "Error": row.get("error", ""),
                        }
                        for row in source_rows
                    ]
                ),
                width="stretch",
                hide_index=True,
            )

        tools_col_1, tools_col_2, tools_col_3 = st.columns(3)
        with tools_col_1:
            if st.button("Refresh local UI cache", use_container_width=True):
                fetch_live_prices.clear()
                fetch_history.clear()
                append_admin_audit_log("clear_ui_cache", "ok")
                st.success("Streamlit cache cleared")
        with tools_col_2:
            if st.button("Check pricing API", use_container_width=True):
                try:
                    health_resp = requests.get(f"{API_BASE_URL}/health", timeout=HEALTH_TIMEOUT_SECONDS)
                    health_resp.raise_for_status()
                    append_admin_audit_log("health_check", "ok", health_resp.text)
                    st.success(f"API OK: {health_resp.text}")
                except Exception as exc:
                    append_admin_audit_log("health_check", "error", str(exc))
                    st.error(f"API unavailable: {exc}")
        with tools_col_3:
            bundle_bytes, bundle_name = build_diagnostics_bundle(conn, counts, live_for_health, source_health)
            st.download_button(
                "Download diagnostics bundle",
                data=bundle_bytes,
                file_name=bundle_name,
                mime="application/zip",
                use_container_width=True,
            )

        st.caption("Active pricing sources")
        source_price_map = {
            (str(row.get("asset_type", "")), str(row.get("asset_name", ""))): float(row.get("value_eur", 0.0) or 0.0)
            for row in source_rows
            if str(row.get("status", "")) == "ok"
        }
        active_sources_rows = fetchall_dict(
            conn.execute(
                "SELECT asset_type, asset_name, source_url, is_active FROM price_sources ORDER BY asset_type, asset_name"
            )
        )
        for row in active_sources_rows:
            price_key = (str(row.get("asset_type", "")), str(row.get("asset_name", "")))
            live_price = source_price_map.get(price_key)
            row["live_price_eur"] = fmt_euro(live_price) if live_price is not None else "-"

        display_sources_rows = [
            {
                "Asset type": row.get("asset_type", ""),
                "Asset": row.get("asset_name", ""),
                "Source URL": row.get("source_url", ""),
                "Live price (€)": row.get("live_price_eur", "-"),
                "Active": row.get("is_active", ""),
            }
            for row in active_sources_rows
        ]

        st.dataframe(
            display_sources_rows,
            width="stretch",
            hide_index=True,
        )

        st.markdown("### Recent admin log")
        audit_rows = read_admin_audit_log(limit=40)
        if audit_rows:
            def format_audit_action(action_value: str) -> str:
                return str(action_value or "").replace("_", " ").strip().title()

            audit_actions = sorted({row.get("action", "") for row in audit_rows if row.get("action")})
            audit_statuses = sorted({row.get("status", "") for row in audit_rows if row.get("status")})
            action_label_to_raw = {format_audit_action(raw_action): raw_action for raw_action in audit_actions}
            sorted_action_labels = sorted(action_label_to_raw.keys())

            filter_col_1, filter_col_2, filter_col_3 = st.columns(3)
            with filter_col_1:
                selected_action_label = st.selectbox(
                    "Action filter",
                    ["All"] + sorted_action_labels,
                    key="audit_filter_action",
                )
                selected_action = "All" if selected_action_label == "All" else action_label_to_raw[selected_action_label]
            with filter_col_2:
                selected_status = st.selectbox(
                    "Status filter",
                    ["All"] + audit_statuses,
                    key="audit_filter_status",
                )
            with filter_col_3:
                selected_period = st.selectbox(
                    "Period",
                    ["24h", "7d", "30d", "All"],
                    index=1,
                    key="audit_filter_period",
                )

            now_utc = datetime.now(timezone.utc)
            period_days = {"24h": 1, "7d": 7, "30d": 30, "All": None}
            selected_days = period_days[selected_period]

            filtered_rows = []
            for row in audit_rows:
                if selected_action != "All" and row.get("action") != selected_action:
                    continue
                if selected_status != "All" and row.get("status") != selected_status:
                    continue
                if selected_days is not None:
                    try:
                        row_dt = datetime.strptime(str(row.get("at", "")), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    except Exception:
                        continue
                    if (now_utc - row_dt).days >= selected_days:
                        continue
                filtered_rows.append(row)

            st.markdown(
                f"<div class='ops-filter-hint'>{len(filtered_rows)} entries for active filters.</div>",
                unsafe_allow_html=True,
            )
            audit_df = pd.DataFrame(filtered_rows[::-1])
            if not audit_df.empty and "status" in audit_df.columns:
                if "action" in audit_df.columns:
                    audit_df["action_label"] = audit_df["action"].map(format_audit_action)
                audit_df["status"] = audit_df["status"].astype(str).str.lower()
                audit_df["status_badge"] = audit_df["status"].map({
                    "ok": "OK",
                    "error": "ERROR",
                }).fillna("INFO")
                display_cols = [col for col in ["at", "action_label", "status_badge", "status", "details"] if col in audit_df.columns]
                audit_df = audit_df[display_cols]
                if "action_label" in audit_df.columns:
                    audit_df = audit_df.rename(columns={"action_label": "Action"})
                audit_df = audit_df.rename(columns={"at": "At", "status_badge": "Status", "status": "Raw status", "details": "Details"})
                styled_audit = audit_df.style.apply(audit_row_style, axis=1)
                st.dataframe(styled_audit, width="stretch", hide_index=True)
            else:
                st.dataframe(audit_df, width="stretch", hide_index=True)
            if st.button("Export admin log (CSV)"):
                exports_dir = os.path.join(os.path.dirname(__file__), "data", "exports")
                os.makedirs(exports_dir, exist_ok=True)
                stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                audit_path = os.path.join(exports_dir, f"admin_audit_{stamp}.csv")
                pd.DataFrame(filtered_rows).to_csv(audit_path, index=False)
                append_admin_audit_log("export_admin_audit_csv", "ok", f"{audit_path} rows={len(filtered_rows)}")
                st.success(f"Log exported: {audit_path}")
        else:
            st.info("No admin actions logged yet.")

    with maintenance_tab_data:
        st.markdown("### Backup & Export")
        backup_label = st.text_input("Backup name", value="")
        data_col_1, data_col_2 = st.columns(2)
        with data_col_1:
            if st.button("Create SQLite backup", use_container_width=True):
                src_db = os.path.join(os.path.dirname(__file__), "data", "assets.db")
                backups_dir = os.path.join(os.path.dirname(__file__), "data", "backups")
                os.makedirs(backups_dir, exist_ok=True)
                stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                safe_label = (backup_label or "backup").strip().replace(" ", "_")
                dest_db = os.path.join(backups_dir, f"assets_{safe_label}_{stamp}.db")
                shutil.copy2(src_db, dest_db)
                append_admin_audit_log("create_backup", "ok", dest_db)
                st.success(f"Backup created: {dest_db}")

        with data_col_2:
            if st.button("Export CSV (snapshot)", use_container_width=True):
                exports_dir = os.path.join(os.path.dirname(__file__), "data", "exports")
                os.makedirs(exports_dir, exist_ok=True)
                stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                tables = [
                    "holdings",
                    "accounts",
                    "receivables",
                    "debts",
                    "khoms_debts",
                    "portfolio_history",
                    "price_sources",
                ]
                exported_files = []
                for table_name in tables:
                    df_table = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    file_path = os.path.join(exports_dir, f"{table_name}_{stamp}.csv")
                    df_table.to_csv(file_path, index=False)
                    exported_files.append(file_path)
                append_admin_audit_log("export_csv_snapshot", "ok", f"count={len(exported_files)}")
                st.success(f"{len(exported_files)} CSV files exported to {exports_dir}")

        st.markdown("### Guided restore")
        if not backup_files:
            st.info("No .db backup found in data/backups")
        else:
            selected_backup = st.selectbox("Choose a backup", backup_files)
            selected_backup_path = os.path.join(backups_dir, selected_backup)
            backup_size_kb = os.path.getsize(selected_backup_path) / 1024
            backup_mtime = datetime.fromtimestamp(os.path.getmtime(selected_backup_path), tz=timezone.utc)
            st.caption(
                f"File: {selected_backup} | Size: {backup_size_kb:.1f} KB | Modified: {backup_mtime.strftime('%Y-%m-%d %H:%M:%S UTC')}"
            )
            st.markdown("#### Preview (dry run)")
            dry_run_rows = []
            try:
                dry_conn = sqlite3.connect(selected_backup_path)
                dry_tables = [
                    row[0]
                    for row in dry_conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
                    ).fetchall()
                ]
                for table_name in dry_tables:
                    row_count = dry_conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                    dry_run_rows.append({"Table": table_name, "Rows": row_count})
                dry_conn.close()
            except Exception as exc:
                dry_run_rows = [{"Table": "error", "Rows": str(exc)}]
            st.dataframe(pd.DataFrame(dry_run_rows), width="stretch", hide_index=True)

            restore_phrase = st.text_input("Confirm by typing RESTORE")
            restore_check = st.checkbox("I confirm restoring this backup")
            if st.button("Restore this backup", type="primary"):
                if restore_phrase != "RESTORE" or not restore_check:
                    st.warning("Invalid confirmation, type RESTORE")
                else:
                    try:
                        src_conn = sqlite3.connect(selected_backup_path)
                        with conn:
                            src_conn.backup(conn)
                        src_conn.close()
                        fetch_live_prices.clear()
                        fetch_history.clear()
                        append_admin_audit_log("restore_backup", "ok", selected_backup)
                        st.success("Backup restored successfully")
                        st.rerun()
                    except Exception as exc:
                        append_admin_audit_log("restore_backup", "error", str(exc))
                        st.error(f"Restore failed: {exc}")

    with maintenance_tab_purge:
        st.markdown(
            """
            <div class="danger-panel">
                <h4>Purge</h4>
                <p>Dangerous actions. Ensure you have a recent backup before continuing.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Purge history")
        danger_phrase = st.text_input("Confirm by typing PURGE_HISTORY")
        danger_check = st.checkbox("I confirm the full history purge")
        if st.button("Delete all portfolio history", type="primary"):
            if danger_phrase != "PURGE_HISTORY" or not danger_check:
                st.warning("Invalid confirmation, type PURGE_HISTORY")
            else:
                conn.execute("DELETE FROM portfolio_history")
                conn.commit()
                fetch_history.clear()
                append_admin_audit_log("purge_portfolio_history", "ok")
                st.success("History deleted")

        st.markdown("### Data cleanup")
        cleanup_scope = st.segmented_control(
            "Cleanup scope",
            ["All data", "Assets", "Cash", "Receivables", "Debts"],
            default="All data",
            key="purge_scope",
            label_visibility="collapsed",
        )

        scope_meta = {
            "All data": {
                "token": "PURGE_ALL_DATA",
                "details": "holdings, accounts, receivables, debts, khoms_debts, portfolio_history",
                "action": "purge_all_data",
                "tables": ["holdings", "accounts", "receivables", "debts", "khoms_debts", "portfolio_history"],
            },
            "Assets": {
                "token": "PURGE_ASSETS",
                "details": "holdings and khoms_debts",
                "action": "purge_assets_data",
                "tables": ["holdings", "khoms_debts"],
            },
            "Cash": {
                "token": "PURGE_CASH",
                "details": "accounts",
                "action": "purge_cash_data",
                "tables": ["accounts"],
            },
            "Receivables": {
                "token": "PURGE_RECEIVABLES",
                "details": "receivables",
                "action": "purge_receivables_data",
                "tables": ["receivables"],
            },
            "Debts": {
                "token": "PURGE_DEBTS",
                "details": "debts and khoms_debts",
                "action": "purge_debts_data",
                "tables": ["debts", "khoms_debts"],
            },
        }
        selected_scope_meta = scope_meta[cleanup_scope]
        cleanup_token = selected_scope_meta["token"]
        st.caption(f"Selected cleanup: {cleanup_scope} -> {selected_scope_meta['details']}")

        impacted_counts: dict[str, int] = {}
        impacted_total = 0
        preview_error = None
        try:
            for table_name in selected_scope_meta["tables"]:
                row = conn.execute(f"SELECT COUNT(*) AS c FROM {table_name}").fetchone()
                if not row:
                    count = 0
                elif isinstance(row, (tuple, list)):
                    count = int(row[0])
                else:
                    count = int(row["c"])
                impacted_counts[table_name] = count
                impacted_total += count
        except Exception as exc:
            preview_error = str(exc)

        st.markdown("#### Preview")
        if preview_error:
            st.warning(f"Unable to compute preview: {preview_error}")
        else:
            preview_parts = [f"{table_name}: {count}" for table_name, count in impacted_counts.items()]
            st.caption("Rows to delete -> " + " | ".join(preview_parts))
            st.info(f"Estimated rows that will be deleted: {impacted_total}")

        cleanup_phrase = st.text_input(
            f"Confirm by typing {cleanup_token}",
            key="purge_scope_phrase",
        )
        cleanup_check = st.checkbox(
            f"I confirm cleanup for {cleanup_scope}",
            key="purge_scope_check",
        )
        if st.button(f"Run cleanup: {cleanup_scope}", type="primary", key="purge_scope_btn"):
            if cleanup_phrase != cleanup_token or not cleanup_check:
                st.warning(f"Invalid confirmation, type {cleanup_token}")
            else:
                try:
                    if cleanup_scope == "All data":
                        conn.execute("DELETE FROM khoms_debts")
                        conn.execute("DELETE FROM holdings")
                        conn.execute("DELETE FROM accounts")
                        conn.execute("DELETE FROM receivables")
                        conn.execute("DELETE FROM debts")
                        conn.execute("DELETE FROM portfolio_history")
                    elif cleanup_scope == "Assets":
                        conn.execute("DELETE FROM khoms_debts")
                        conn.execute("DELETE FROM holdings")
                    elif cleanup_scope == "Cash":
                        conn.execute("DELETE FROM accounts")
                    elif cleanup_scope == "Receivables":
                        conn.execute("DELETE FROM receivables")
                    elif cleanup_scope == "Debts":
                        conn.execute("DELETE FROM khoms_debts")
                        conn.execute("DELETE FROM debts")

                    conn.commit()
                    fetch_live_prices.clear()
                    fetch_history.clear()
                    append_admin_audit_log(selected_scope_meta["action"], "ok", cleanup_scope)
                    st.success(f"Cleanup completed for {cleanup_scope}")
                    st.rerun()
                except Exception as exc:
                    append_admin_audit_log(selected_scope_meta["action"], "error", str(exc))
                    st.error(f"Cleanup failed: {exc}")

