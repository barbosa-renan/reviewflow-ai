"""
Script para testar a API ReviewFlow AI.
"""

import asyncio
import json
import httpx
from typing import Dict, Any


# Dados de teste
test_review = {
    "text": "Produto chegou quebrado após 2 semanas de espera. Péssimo! Quero reembolso imediato ou vou acionar o Procon.",
    "customer_id": "CUST-12345",
    "customer_name": "João Silva",
    "product_name": "Smartphone XYZ Pro",
    "product_id": "PROD-001",
    "purchase_date": "2025-10-15",
    "rating": 1
}

API_BASE_URL = "http://localhost:8000"


async def test_health_endpoint():
    """Testa o endpoint de health check."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/health")
            print("🏥 Health Check:")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Erro no health check: {e}")


async def test_process_review():
    """Testa o processamento de um review."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/api/v1/reviews/process",
                json=test_review
            )
            print("📝 Processamento de Review:")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Review processado com sucesso!")
                print(f"Review ID: {result.get('review_input', {}).get('id')}")
                print(f"Tempo de processamento: {result.get('processing_time'):.2f}s")
                print(f"Status: {result.get('status')}")
            else:
                print(f"❌ Erro: {response.text}")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")


async def test_batch_processing():
    """Testa o processamento em lote."""
    batch_reviews = [test_review, test_review.copy()]
    batch_reviews[1]["customer_name"] = "Maria Silva"
    batch_reviews[1]["customer_id"] = "CUST-67890"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/api/v1/reviews/batch",
                json=batch_reviews
            )
            print("📦 Processamento em Lote:")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Lote enviado com sucesso!")
                print(f"Batch ID: {result.get('batch_id')}")
                print(f"Total de reviews: {result.get('total_reviews')}")
                print(f"Status: {result.get('status')}")
            else:
                print(f"❌ Erro: {response.text}")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Erro no processamento em lote: {e}")


async def test_stats():
    """Testa o endpoint de estatísticas."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/v1/stats")
            print("📊 Estatísticas:")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Erro nas estatísticas: {e}")


async def main():
    """Executa todos os testes."""
    print("🚀 Iniciando testes da API ReviewFlow AI")
    print("=" * 50)
    
    await test_health_endpoint()
    await test_process_review()
    await test_batch_processing()
    await test_stats()
    
    print("✅ Testes concluídos!")


if __name__ == "__main__":
    asyncio.run(main())