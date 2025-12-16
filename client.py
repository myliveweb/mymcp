import asyncio
import json
from fastmcp import Client
import main  # Импортируем сервер напрямую для in-process подключения


def render_result(name: str, content):
    """Печатает результат инструмента человекочитаемо."""
    if name == "list_torrent_path":
        data = content
        if isinstance(content, str):
            try:
                data = json.loads(content)
            except Exception:
                pass
        if isinstance(data, dict):
            path = data.get("path", "")
            print(f"Путь: {path}")
            entries = data.get("entries") or []
            if not entries:
                print("Пусто")
            else:
                print("Содержимое:")
                for entry in entries:
                    n = entry.get("name", "")
                    t = entry.get("type", "")
                    print(f"- [{t}] {n}")
            if "error" in data:
                print(f"Ошибка: {data['error']}")
        else:
            print(data)
        return

    if name == "telegram_send_message":
        if isinstance(content, dict):
            status = content.get("status_code")
            ok = content.get("ok")
            error = content.get("error")
            print(f"status_code={status}, ok={ok}")
            if error:
                print(f"error={error}")
            else:
                print(f"response={content.get('response')}")
        else:
            print(content)
        return

    # По умолчанию печатаем как есть
    print(content)

async def main_func():
    # Подключение к серверу in-process (используем сам объект FastMCP)
    async with Client(main.mcp) as client:
        # Получаем список доступных инструментов
        tools = await client.list_tools()
        print("Доступные инструменты:")
        for tool in tools:
            print(f"- {tool.name}")

        # Набор вызовов с тестовыми аргументами
        calls = [
            ("get_python_version", {}),
            ("echo", {"message": "hello from client"}),
            ("ping", {}),
            ("add_numbers", {"a": 2, "b": 3}),
            ("get_status", {}),
            ("info", {}),
            ("to_upper", {"text": "fastmcp"}),
            ("now_iso", {}),
            ("concat", {"a": "fast", "b": "mcp"}),
            ("telegram_send_message", {"text": "Hello from FastMCP client", "chat_id": None}),
            # ("http_get_example", {"url": "https://example.com"}),  # при необходимости
            ("list_torrent_path", {}),
        ]

        for name, args in calls:
            result = await client.call_tool(name, args if args else None)
            print(f"\n{name} ->")
            if result.content and len(result.content) > 0:
                content_item = result.content[0]
                content = content_item.text if hasattr(content_item, "text") else content_item
            else:
                content = result.content
            render_result(name, content)

if __name__ == "__main__":
    asyncio.run(main_func())

