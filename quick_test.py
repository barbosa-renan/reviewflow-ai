"""Teste rápido da API"""
import asyncio
import httpx

async def test_health():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    asyncio.run(test_health())