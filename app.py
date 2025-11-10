"""
ReviewFlow AI - API Principal
Sistema de gerenciamento inteligente de reviews de e-commerce.
"""

import os
import asyncio
import time
import logging
from contextlib import asynccontextmanager
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from dotenv import load_dotenv

from src.reviewflow_ai.models.data_models import (
    ReviewInput, 
    ProcessingResult,
    ReviewAnalysis,
    ResponseGeneration,
    EscalationTicket,
    WorkflowResult
)
from src.reviewflow_ai.tools.validation import validate_review_input
from src.reviewflow_ai.agents.workflow_orchestrator import create_workflow_orchestrator_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação."""
    
    logger.info("Iniciando ReviewFlow AI API...")
    
    required_env_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Variáveis de ambiente obrigatórias não encontradas: {missing_vars}")
        raise RuntimeError(f"Missing environment variables: {missing_vars}")
    try:
        app.state.workflow_agent = create_workflow_orchestrator_agent()
        logger.info("Workflow Orchestrator Agent inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar agente: {e}")
        raise
    
    logger.info("ReviewFlow AI API pronta para uso!")
    
    yield
    
    logger.info("Finalizando ReviewFlow AI API...")


# Criar aplicação FastAPI
app = FastAPI(
    title="ReviewFlow AI",
    description="Sistema inteligente de gerenciamento de reviews de e-commerce usando agentes AI",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint de boas-vindas."""
    return {
        "message": "ReviewFlow AI - Sistema de Gerenciamento Inteligente de Reviews",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "process_review": "/api/v1/reviews/process",
            "process_batch": "/api/v1/reviews/batch",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde da aplicação."""
    try:
        agent_status = hasattr(app.state, 'workflow_agent')
        
        env_status = bool(os.getenv("OPENAI_API_KEY"))
        
        overall_status = "healthy" if (agent_status and env_status) else "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": time.time(),
            "components": {
                "workflow_agent": "ok" if agent_status else "error",
                "environment": "ok" if env_status else "error"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.post("/api/v1/reviews/process", response_model=ProcessingResult)
async def process_review(review: ReviewInput):
    """
    Processa um único review usando o sistema de agentes.
    
    Args:
        review: Dados do review a ser processado
        
    Returns:
        ProcessingResult: Resultado completo do processamento
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processando review do cliente: {review.customer_name}")
        
        validated_review = validate_review_input(review.model_dump())
        
        # Converter para JSON para o agente
        review_json = validated_review.model_dump_json(indent=2, ensure_ascii=False)
        
        # Processar com o Workflow Orchestrator
        workflow_agent = app.state.workflow_agent
        
        # Executar o processamento
        result = await workflow_agent.process_review(review_json)
        
        processing_time = time.time() - start_time
        
        if result.get("status") != "success":
            logger.error(f"❌ Erro no processamento: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        # Estruturar resultado final
        processing_result = ProcessingResult(
            review_input=validated_review,
            analysis=ReviewAnalysis(
                validation_status="success",
                sentiment=result["analysis"].get("sentiment"),
                sentiment_score=result["analysis"].get("sentiment_score"),
                categories=result["analysis"].get("categories", []),
                urgency=result["analysis"].get("urgency"),
                key_issues=result["analysis"].get("key_issues", []),
                customer_id=validated_review.customer_id,
                customer_name=validated_review.customer_name,
                product_name=validated_review.product_name,
                confidence_score=result["analysis"].get("confidence_score", 0.0)
            ),
            workflow=WorkflowResult(
                review_id=validated_review.id,
                workflow_path=result["workflow_path"],
                customer_context=result["customer_context"],
                product_context=result["product_context"],
                agents_triggered=["review_analyzer", "workflow_orchestrator"],
                tools_used=["get_customer_history"] if result.get("customer_context") else [],
                priority_level=result["priority_level"],
                estimated_completion_time=result["estimated_completion_time"],
                sla_status="Within_SLA",
                strategic_notes=result["strategic_notes"]
            ),
            processing_time=processing_time
        )
        
        logger.info(f"Review processado com sucesso em {processing_time:.2f}s")
        
        return processing_result
        
    except ValidationError as e:
        logger.error(f"Erro de validação: {e}")
        raise HTTPException(status_code=400, detail=f"Dados de entrada inválidos: {e}")
    
    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")


@app.post("/api/v1/reviews/batch")
async def process_batch_reviews(
    reviews: List[ReviewInput],
    background_tasks: BackgroundTasks
):
    """
    Processa múltiplos reviews em lote.
    
    Args:
        reviews: Lista de reviews a serem processados
        background_tasks: Tarefas em segundo plano do FastAPI
        
    Returns:
        Dict com informações sobre o processamento em lote
    """
    try:
        if len(reviews) > 100:
            raise HTTPException(
                status_code=400, 
                detail="Máximo de 100 reviews por lote"
            )
        
        batch_id = f"BATCH-{int(time.time())}"
        
        logger.info(f"📦 Processando lote {batch_id} com {len(reviews)} reviews")
        
        # Agendar processamento em segundo plano
        background_tasks.add_task(process_batch_background, batch_id, reviews)
        
        return {
            "batch_id": batch_id,
            "total_reviews": len(reviews),
            "status": "processing",
            "message": "Processamento iniciado em segundo plano",
            "estimated_completion": f"{len(reviews) * 2} segundos"
        }
        
    except Exception as e:
        logger.error(f"Erro no processamento em lote: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_batch_background(batch_id: str, reviews: List[ReviewInput]):
    """Processa lote de reviews em segundo plano."""
    logger.info(f"Iniciando processamento do lote {batch_id}")
    
    results = []
    
    for i, review in enumerate(reviews):
        try:
            # Simular processamento (substituir pela lógica real)
            result = await process_single_review_internal(review)
            results.append(result)
            
            logger.info(f"Review {i+1}/{len(reviews)} processado")
            
        except Exception as e:
            logger.error(f"Erro no review {i+1}: {e}")
            results.append({"error": str(e)})
    
    # TODO: Salvar os resultados em um banco de dados
    # ou cache para consulta posterior
    logger.info(f"Lote {batch_id} processado: {len(results)} resultados")


async def process_single_review_internal(review: ReviewInput) -> Dict[str, Any]:
    """Processa um review internamente (para uso em lotes)."""
    validated_review = validate_review_input(review.model_dump())
    
    return {
        "review_id": validated_review.id,
        "customer_name": validated_review.customer_name,
        "status": "processed",
        "processing_time": 1.5  # Placeholder
    }


@app.get("/api/v1/stats")
async def get_stats():
    """Retorna estatísticas do sistema."""
    return {
        "total_processed": 0,  # TODO: Implementar contador
        "average_processing_time": 2.3,
        "system_uptime": time.time(),
        "active_agents": 4
    }


if __name__ == "__main__":
    import uvicorn
    
    # Configuração para desenvolvimento
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload em desenvolvimento
        log_level="info"
    )
