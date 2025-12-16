import asyncio
from fastmcp import Client
import main  # Импортируем сервер напрямую для in-process подключения

async def main_func():
    # Подключение к серверу in-process (используем сам объект FastMCP)
    async with Client(main.mcp) as client:
        # Получаем список доступных инструментов
        tools = await client.list_tools()
        print(f"Доступные инструменты: {[tool.name for tool in tools]}")
        
        # Вызываем инструмент get_python_version
        result = await client.call_tool("get_python_version")
        print(f"\nРезультат вызова инструмента:")
        # Результат находится в атрибуте content как список TextContent
        if result.content and len(result.content) > 0:
            print(result.content[0].text)
        else:
            print(result.content)

if __name__ == "__main__":
    asyncio.run(main_func())

