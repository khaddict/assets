import os
import json
import re
import sqlite3
import threading
import time
import logging
from datetime import datetime, timezone
from typing import Any

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency fallback
    load_dotenv = None

app = FastAPI(title="Local Pricing API", version="1.0.0")
PRICE_CACHE: dict[str, Any] = {"fetched_at": 0.0, "payload": None}
PRICE_CACHE_LOCK = threading.Lock()
REFRESH_IN_PROGRESS = False
logger = logging.getLogger("pricing_api")
RUNTIME_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "data", "runtime_settings.json")

if load_dotenv is not None:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)


def load_runtime_settings() -> dict[str, Any]:
    defaults = {
        "pricing_api": {
            "cache_ttl_seconds": 60,
            "request_timeout_seconds": 10,
            "request_retries": 3,
            "request_backoff_seconds": 1,
        }
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

    pricing_api_settings = loaded.get("pricing_api")
    if not isinstance(pricing_api_settings, dict):
        return defaults

    cache_ttl = pricing_api_settings.get("cache_ttl_seconds")
    request_timeout = pricing_api_settings.get("request_timeout_seconds")
    request_retries = pricing_api_settings.get("request_retries")
    request_backoff = pricing_api_settings.get("request_backoff_seconds")
    if not isinstance(cache_ttl, int):
        cache_ttl = defaults["pricing_api"]["cache_ttl_seconds"]
    if not isinstance(request_timeout, int):
        request_timeout = defaults["pricing_api"]["request_timeout_seconds"]
    if not isinstance(request_retries, int):
        request_retries = defaults["pricing_api"]["request_retries"]
    if not isinstance(request_backoff, int):
        request_backoff = defaults["pricing_api"]["request_backoff_seconds"]

    return {
        "pricing_api": {
            "cache_ttl_seconds": max(10, cache_ttl),
            "request_timeout_seconds": max(1, request_timeout),
            "request_retries": max(1, request_retries),
            "request_backoff_seconds": max(1, request_backoff),
        }
    }


RUNTIME_SETTINGS = load_runtime_settings()
CACHE_TTL_SECONDS = int(RUNTIME_SETTINGS["pricing_api"]["cache_ttl_seconds"])
REQUEST_TIMEOUT_SECONDS = int(RUNTIME_SETTINGS["pricing_api"]["request_timeout_seconds"])
REQUEST_RETRIES = int(RUNTIME_SETTINGS["pricing_api"]["request_retries"])
REQUEST_BACKOFF_SECONDS = int(RUNTIME_SETTINGS["pricing_api"]["request_backoff_seconds"])

STRIKE_API_TOKEN = os.getenv("STRIKE_API_TOKEN", "").strip()
STRIKE_API_BASE_URL = os.getenv("STRIKE_API_BASE_URL", "https://api.strike.me").rstrip("/")
STRIKE_SOURCE_CURRENCY = os.getenv("STRIKE_SOURCE_CURRENCY", "BTC").strip().upper()
STRIKE_TARGET_CURRENCY = os.getenv("STRIKE_TARGET_CURRENCY", "EUR").strip().upper()


def request_with_retry(url: str, timeout: int, headers: dict[str, str] | None = None) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(REQUEST_RETRIES):
        try:
            return requests.get(url, timeout=timeout, headers=headers)
        except Exception as exc:
            last_error = exc
            if attempt + 1 < REQUEST_RETRIES:
                delay = REQUEST_BACKOFF_SECONDS * (2 ** attempt)
                logger.warning(
                    "http retry attempt=%s/%s url=%s delay_seconds=%s error=%s",
                    attempt + 1,
                    REQUEST_RETRIES,
                    url,
                    delay,
                    exc,
                )
                time.sleep(delay)
    if last_error is not None:
        raise last_error
    raise RuntimeError("request failed without explicit error")


def get_db() -> sqlite3.Connection:
    db_path = os.path.join(os.path.dirname(__file__), "data", "assets.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
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
        CREATE TABLE IF NOT EXISTS latest_prices_cache (
            cache_key TEXT PRIMARY KEY,
            fetched_at REAL NOT NULL,
            payload_json TEXT NOT NULL
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
        """
    )
    conn.commit()


def fetchall_dict(cursor: sqlite3.Cursor) -> list[dict[str, Any]]:
    cols = [col[0] for col in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def get_enabled_assets(conn: sqlite3.Connection) -> dict[str, bool]:
    enabled = {
        "gold": True,
        "silver": True,
        "btc": True,
        "cash": True,
        "receivables": True,
        "debts": True,
    }
    return enabled


def parse_eur_price(raw_text: str) -> float | None:
    cleaned = raw_text.replace("\xa0", " ").replace("EUR", "").replace("€", "")
    cleaned = re.sub(r"\s+", "", cleaned).replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def fetch_metal_price(url: str) -> float | None:
    response = request_with_retry(
        url,
        REQUEST_TIMEOUT_SECONDS,
        headers={
            "user-agent": "Mozilla/5.0 assets-gui-poc/1.0",
            "accept": "text/html,application/xhtml+xml",
        },
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    candidates = [
        soup.select_one("#pv").get_text(strip=True) if soup.select_one("#pv") else "",
        (soup.select_one("meta[property='product:price:amount']") or {}).get("content", ""),
        soup.select_one(".price").get_text(strip=True) if soup.select_one(".price") else "",
    ]

    for candidate in candidates:
        if not candidate:
            continue
        parsed = parse_eur_price(str(candidate))
        if parsed is not None:
            return parsed
    return None


def fetch_btc_price() -> tuple[float, str]:
    if not STRIKE_API_TOKEN:
        raise RuntimeError("STRIKE_API_TOKEN is required for BTC pricing")

    response = request_with_retry(
        f"{STRIKE_API_BASE_URL}/v1/rates/ticker",
        REQUEST_TIMEOUT_SECONDS,
        headers={
            "Authorization": f"Bearer {STRIKE_API_TOKEN}",
            "Accept": "application/json",
            "User-Agent": "assets-gui-poc/1.0",
        },
    )

    if response.status_code == 401:
        raise RuntimeError("Strike token unauthorized (401)")
    if response.status_code == 403:
        raise RuntimeError("Strike token missing permission for /v1/rates/ticker")

    response.raise_for_status()
    payload = response.json()
    tickers = payload if isinstance(payload, list) else payload.get("data", [])

    if not isinstance(tickers, list):
        raise RuntimeError("Unexpected Strike response format for rates ticker")

    for item in tickers:
        if not isinstance(item, dict):
            continue
        source_currency = str(item.get("sourceCurrency", "")).upper()
        target_currency = str(item.get("targetCurrency", "")).upper()
        if source_currency == STRIKE_SOURCE_CURRENCY and target_currency == STRIKE_TARGET_CURRENCY:
            return float(item.get("amount", 0.0) or 0.0), f"{STRIKE_API_BASE_URL}/v1/rates/ticker"

    raise RuntimeError(f"Strike pair not found: {STRIKE_SOURCE_CURRENCY}->{STRIKE_TARGET_CURRENCY}")


def build_market_totals(conn: sqlite3.Connection, payload: dict[str, Any]) -> dict[str, float]:
    enabled_assets = get_enabled_assets(conn)
    holdings = fetchall_dict(
        conn.execute(
            "SELECT asset_type, asset_name, quantity, buy_price_unit, buy_date FROM holdings"
        )
    )
    metal_prices = payload.get("prices", {}).get("metals", {})
    btc_price = float(payload.get("prices", {}).get("btc", 0.0) or 0.0)

    gold_value = 0.0
    silver_value = 0.0
    btc_value = 0.0
    gold_tax_estimated = 0.0
    silver_tax_estimated = 0.0
    btc_tax_estimated = 0.0
    now_utc = datetime.now(timezone.utc)

    def parse_buy_date_utc(raw_date: Any) -> datetime | None:
        try:
            date_part = str(raw_date or "").strip()[:10]
            return datetime.strptime(date_part, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except Exception:
            return None

    def estimate_metal_tax_fr(gross_sale: float, buy_cost: float, buy_dt: datetime | None) -> float:
        # Two common FR regimes for precious metals resale:
        # - TMP: 11.5% of sale amount
        # - Plus-value: 36.2% on taxable gain with 5% allowance/year after year 2
        # We keep a conservative estimate by selecting the lowest payable option when data exists.
        gross = max(0.0, float(gross_sale))
        gain = max(0.0, gross - max(0.0, float(buy_cost)))
        tmp_tax = gross * 0.115

        if buy_dt is None:
            return tmp_tax

        holding_days = max(0.0, (now_utc - buy_dt).days)
        holding_years = holding_days / 365.25
        allowance = 0.0
        if holding_years > 2:
            allowance = min(1.0, (holding_years - 2.0) * 0.05)

        taxable_gain = gain * (1.0 - allowance)
        plus_value_tax = taxable_gain * 0.362
        return min(tmp_tax, plus_value_tax)

    def estimate_btc_tax_fr(gross_sale: float, buy_cost: float) -> float:
        gain = max(0.0, max(0.0, float(gross_sale)) - max(0.0, float(buy_cost)))
        # Simplified estimate: PFU 30% on positive gain at disposal.
        return gain * 0.30

    for row in holdings:
        quantity = float(row["quantity"])
        buy_cost = max(0.0, float(row.get("buy_price_unit", 0.0) or 0.0)) * quantity
        buy_dt = parse_buy_date_utc(row.get("buy_date"))

        if row["asset_type"] == "gold" and enabled_assets.get("gold", True):
            gross_sale = float(metal_prices.get(row["asset_name"], 0.0) or 0.0) * quantity
            gold_value += gross_sale
            gold_tax_estimated += estimate_metal_tax_fr(gross_sale, buy_cost, buy_dt)
        elif row["asset_type"] == "silver" and enabled_assets.get("silver", True):
            gross_sale = float(metal_prices.get(row["asset_name"], 0.0) or 0.0) * quantity
            silver_value += gross_sale
            silver_tax_estimated += estimate_metal_tax_fr(gross_sale, buy_cost, buy_dt)
        elif row["asset_type"] == "btc" and enabled_assets.get("btc", True):
            gross_sale = btc_price * quantity
            btc_value += gross_sale
            btc_tax_estimated += estimate_btc_tax_fr(gross_sale, buy_cost)

    cash = (conn.execute("SELECT COALESCE(SUM(amount), 0) FROM accounts").fetchone()[0] or 0.0) if enabled_assets.get("cash") else 0.0
    receiv = (conn.execute("SELECT COALESCE(SUM(amount), 0) FROM receivables").fetchone()[0] or 0.0) if enabled_assets.get("receivables") else 0.0
    debts_manual = (conn.execute("SELECT COALESCE(SUM(amount), 0) FROM debts").fetchone()[0] or 0.0) if enabled_assets.get("debts") else 0.0
    khoms_pending = (conn.execute("SELECT COALESCE(SUM(amount), 0) FROM khoms_debts WHERE status='pending'").fetchone()[0] or 0.0) if enabled_assets.get("debts") else 0.0
    debts = float(debts_manual) + float(khoms_pending)
    taxes_estimated = gold_tax_estimated + silver_tax_estimated + btc_tax_estimated
    total_gross = gold_value + silver_value + btc_value + float(cash) + float(receiv) - debts
    total_net_after_tax = total_gross - taxes_estimated

    return {
        "gold": gold_value,
        "silver": silver_value,
        "btc": btc_value,
        "cash": float(cash),
        "receiv": float(receiv),
        "debts": debts,
        "taxes_estimated": float(taxes_estimated),
        "gold_tax_estimated": float(gold_tax_estimated),
        "silver_tax_estimated": float(silver_tax_estimated),
        "btc_tax_estimated": float(btc_tax_estimated),
        "total_gross": float(total_gross),
        "total_net_after_tax": float(total_net_after_tax),
        # Keep backward compatibility for existing UI/history consumers.
        "total": float(total_net_after_tax),
    }


def save_portfolio_snapshot(conn: sqlite3.Connection, total_value: float, recorded_at: str) -> None:
    last = conn.execute(
        "SELECT recorded_at, total_value FROM portfolio_history ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if last:
        last_dt = datetime.strptime(last[0][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        elapsed = (datetime.now(timezone.utc) - last_dt).total_seconds()
        same_value = abs(float(last[1]) - float(total_value)) < 0.01
        if elapsed < CACHE_TTL_SECONDS - 5 or same_value:
            return

    conn.execute(
        "INSERT INTO portfolio_history (recorded_at, total_value) VALUES (?, ?)",
        (recorded_at, float(total_value)),
    )
    conn.commit()


def load_cached_payload(conn: sqlite3.Connection) -> None:
    row = conn.execute(
        "SELECT fetched_at, payload_json FROM latest_prices_cache WHERE cache_key='prices'"
    ).fetchone()
    if not row:
        return
    try:
        payload = json.loads(row[1])
    except json.JSONDecodeError:
        return
    with PRICE_CACHE_LOCK:
        PRICE_CACHE["fetched_at"] = float(row[0])
        PRICE_CACHE["payload"] = payload


def persist_cached_payload(conn: sqlite3.Connection, fetched_at: float, payload: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO latest_prices_cache (cache_key, fetched_at, payload_json)
        VALUES ('prices', ?, ?)
        ON CONFLICT(cache_key) DO UPDATE SET fetched_at=excluded.fetched_at, payload_json=excluded.payload_json
        """,
        (float(fetched_at), json.dumps(payload)),
    )
    conn.commit()


def refresh_prices_payload(force: bool = False) -> dict[str, Any]:
    global REFRESH_IN_PROGRESS
    now = time.time()
    with PRICE_CACHE_LOCK:
        cached_payload = PRICE_CACHE.get("payload")
        cached_at = float(PRICE_CACHE.get("fetched_at", 0.0) or 0.0)
        if not force and cached_payload and (now - cached_at) < CACHE_TTL_SECONDS:
            return cached_payload
        if REFRESH_IN_PROGRESS and cached_payload:
            return cached_payload
        REFRESH_IN_PROGRESS = True

    try:
        conn = get_db()
        init_db(conn)

        enabled_assets = get_enabled_assets(conn)
        sources = fetchall_dict(
            conn.execute(
                """
                SELECT id, asset_type, asset_name, source_url, is_active
                FROM price_sources
                WHERE is_active = 1
                ORDER BY asset_type, asset_name, id
                """
            )
        )

        result_assets: list[dict[str, Any]] = []

        for source in sources:
            asset_type = source["asset_type"]
            if asset_type in ("gold", "silver") and not enabled_assets.get(asset_type, True):
                continue
            if asset_type == "btc" and not enabled_assets.get("btc", True):
                continue

            item = {
                "asset_type": asset_type,
                "asset_name": source["asset_name"],
                "source_url": source["source_url"],
                "value_eur": 0.0,
                "status": "ok",
                "error": "",
                "latency_ms": 0,
            }

            try:
                started_at = time.perf_counter()
                if asset_type in ("gold", "silver"):
                    parsed = fetch_metal_price(source["source_url"])
                    item["value_eur"] = float(parsed or 0.0)
                elif asset_type == "btc":
                    btc_value_eur, btc_source_url = fetch_btc_price()
                    item["value_eur"] = btc_value_eur
                    item["source_url"] = btc_source_url
                else:
                    item["status"] = "ignored"
                    item["error"] = "unsupported asset type"
                item["latency_ms"] = int((time.perf_counter() - started_at) * 1000)
            except Exception as exc:
                item["status"] = "error"
                item["error"] = str(exc)
                item["latency_ms"] = 0
                logger.warning(
                    "price fetch failed asset_type=%s asset_name=%s source_url=%s error=%s",
                    asset_type,
                    source["asset_name"],
                    source["source_url"],
                    exc,
                )

            result_assets.append(item)

        btc_value = 0.0
        for item in result_assets:
            if item["asset_type"] == "btc" and item["status"] == "ok":
                btc_value = float(item["value_eur"])
                break

        metals = {
            item["asset_name"]: item["value_eur"]
            for item in result_assets
            if item["asset_type"] in ("gold", "silver") and item["status"] == "ok"
        }

        overall_status = "ok"
        if any(item["status"] == "error" for item in result_assets):
            overall_status = "partial"

        recorded_at = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(now))
        payload = {
            "status": overall_status,
            "fetched_at": recorded_at,
            "assets": result_assets,
            "prices": {
                "metals": metals,
                "btc": btc_value,
            },
            "source_health": {
                "ok": len([item for item in result_assets if item.get("status") == "ok"]),
                "error": len([item for item in result_assets if item.get("status") == "error"]),
            },
        }
        payload["market_totals"] = build_market_totals(conn, payload)
        save_portfolio_snapshot(conn, payload["market_totals"]["total"], recorded_at)
        persist_cached_payload(conn, now, payload)

        with PRICE_CACHE_LOCK:
            PRICE_CACHE["fetched_at"] = now
            PRICE_CACHE["payload"] = payload
        return payload
    finally:
        with PRICE_CACHE_LOCK:
            REFRESH_IN_PROGRESS = False


def start_async_refresh_if_needed() -> None:
    global REFRESH_IN_PROGRESS
    with PRICE_CACHE_LOCK:
        cached_payload = PRICE_CACHE.get("payload")
        cached_at = float(PRICE_CACHE.get("fetched_at", 0.0) or 0.0)
        is_stale = (time.time() - cached_at) >= CACHE_TTL_SECONDS
        if REFRESH_IN_PROGRESS or not is_stale or cached_payload is None:
            return
        thread = threading.Thread(target=refresh_prices_payload, kwargs={"force": True}, daemon=True)
        thread.start()


def background_refresh_loop() -> None:
    while True:
        try:
            refresh_prices_payload(force=True)
        except Exception as exc:
            logger.exception("background refresh failed: %s", exc)
        time.sleep(CACHE_TTL_SECONDS)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/prices")
def prices() -> dict[str, Any]:
    conn = get_db()
    init_db(conn)
    load_cached_payload(conn)
    with PRICE_CACHE_LOCK:
        cached_payload = PRICE_CACHE.get("payload")
    if cached_payload is not None:
        start_async_refresh_if_needed()
        return cached_payload
    return refresh_prices_payload(force=True)


@app.get("/history")
def history(limit: int = 180) -> dict[str, Any]:
    conn = get_db()
    init_db(conn)
    safe_limit = max(1, min(1000, int(limit or 180)))
    rows = fetchall_dict(
        conn.execute(
            "SELECT recorded_at, total_value FROM portfolio_history ORDER BY id DESC LIMIT ?",
            (safe_limit,),
        )
    )
    return {"history": list(reversed(rows))}


@app.on_event("startup")
def startup_refresh() -> None:
    conn = get_db()
    init_db(conn)
    load_cached_payload(conn)
    threading.Thread(target=refresh_prices_payload, kwargs={"force": True}, daemon=True).start()
    threading.Thread(target=background_refresh_loop, daemon=True).start()
