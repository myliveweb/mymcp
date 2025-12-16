import sys
import os
from zoneinfo import ZoneInfo

import fastmcp
from fastmcp import FastMCP
from dotenv import load_dotenv

# Загружаем переменные окружения из .env (если файл существует)
load_dotenv()

TZ_NAME = os.getenv("TZ_NAME", "Europe/Moscow")
TZ = ZoneInfo(TZ_NAME)

mcp = FastMCP("My MCP Server")

@mcp.tool
def get_python_version() -> str:
    """Возвращает версию Python."""
    return f"Python version: {sys.version}"


@mcp.tool
def echo(message: str) -> str:
    """Простой эхо-инструмент для тестов."""
    return message


@mcp.tool
def ping() -> str:
    """Проверка связности."""
    return "pong"


@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Суммирует два числа."""
    return a + b


@mcp.tool
def get_status() -> dict:
    """Возвращает фиктивный статус сервера."""
    return {
        "status": "ok",
        "env": "dev",
        "version": "0.1.0",
        "timezone": TZ_NAME,
        "fastmcp_version": fastmcp.__version__,
    }


@mcp.tool
def info() -> dict:
    """Метаданные сервера."""
    return {
        "name": "My MCP Server",
        "version": "0.1.0",
        "runtime": sys.version,
        "timezone": TZ_NAME,
        "fastmcp_version": fastmcp.__version__,
    }


@mcp.tool
def to_upper(text: str) -> str:
    """Приводит строку к верхнему регистру."""
    return text.upper()


@mcp.tool
def now_iso() -> str:
    """Текущая дата/время в ISO формате (Europe/Moscow)."""
    import datetime as _dt

    return _dt.datetime.now(TZ).isoformat()


@mcp.tool
def concat(a: str, b: str) -> str:
    """Конкатенация двух строк."""
    return a + b


@mcp.tool
def http_get_example(url: str = "https://example.com") -> dict:
    """Демонстрационный GET с whitelisted URL."""
    import httpx

    if not url.startswith("https://example.com"):
        return {"error": "url not allowed"}

    resp = httpx.get(url, timeout=5.0)
    return {"status_code": resp.status_code, "text": resp.text[:200]}


@mcp.tool
def telegram_send_message(text: str, chat_id: str | None = None) -> dict:
    """Отправляет сообщение в Telegram через Bot API (sendMessage).

    Требуются переменные окружения:
      TELEGRAM_BOT_TOKEN - токен бота
      TELEGRAM_CHAT_ID   - чат по умолчанию (опционально, если chat_id не передан)
    """
    import httpx

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    target_chat = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        return {"error": "TELEGRAM_BOT_TOKEN is missing"}
    if not target_chat:
        return {"error": "chat_id is missing (pass arg or TELEGRAM_CHAT_ID)"}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = httpx.post(url, json={"chat_id": target_chat, "text": text}, timeout=10)
        data = resp.json()
        return {"status_code": resp.status_code, "ok": resp.is_success, "response": data}
    except Exception as exc:
        return {"error": str(exc)}


@mcp.tool
def list_torrent_path() -> dict:
    """Возвращает список файлов и директорий в /mnt/54782556782537DE/Torrent."""
    target = "/mnt/54782556782537DE/Torrent"
    try:
        entries = []
        for name in os.listdir(target):
            full = os.path.join(target, name)
            kind = "dir" if os.path.isdir(full) else "file" if os.path.isfile(full) else "other"
            entries.append({"name": name, "type": kind})
        return {"path": target, "entries": entries}
    except Exception as exc:
        return {"path": target, "error": str(exc)}

if __name__ == "__main__":
    mcp.run()
