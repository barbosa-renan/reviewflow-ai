"""
Workflow Orchestrator Agent - Coordena todo o fluxo de processamento.
"""

import json
from typing import Dict, Any
from .review_analyzer import create_review_analyzer_agent
from ..tools.customer_service import get_customer_history
from ..tools.product_service import get_product_info


class WorkflowOrchestrator:
    """Coordenador principal do workflow de processamento de reviews."""
    
    def __init__(self):
        self.review_analyzer = create_review_analyzer_agent()
    
    async def process_review(self, review_data: str) -> Dict[str, Any]:
        """Processa um review completo através do workflow."""
        try:
            # Parse do input
            if isinstance(review_data, str):
                review_input = json.loads(review_data)
            else:
                review_input = review_data
            
            # Stage 1: Análise do review
            analysis_result = await self.review_analyzer.analyze_review(json.dumps(review_input))
            
            if analysis_result.get("validation_status") != "success":
                return {
                    "status": "error",
                    "error": analysis_result.get("error_message", "Validation failed"),
                    "review_id": review_input.get("id", "unknown")
                }
            
            # Stage 2: Buscar contexto do cliente
            customer_context = None
            if review_input.get("customer_id"):
                customer_context = get_customer_history(review_input["customer_id"])
            
            # Stage 3: Buscar contexto do produto
            product_context = None
            if review_input.get("product_id"):
                product_context = get_product_info(review_input["product_id"])
            
            # Stage 4: Determinar workflow path
            workflow_path = self._determine_workflow_path(
                analysis_result, 
                customer_context, 
                product_context
            )
            
            # Stage 5: Executar ações baseadas no workflow path
            actions_taken = await self._execute_workflow_actions(
                workflow_path,
                analysis_result,
                customer_context,
                product_context,
                review_input
            )
            
            # Resultado final
            return {
                "status": "success",
                "review_id": review_input.get("id", "unknown"),
                "analysis": analysis_result,
                "customer_context": self._format_customer_context(customer_context),
                "product_context": self._format_product_context(product_context),
                "workflow_path": workflow_path,
                "actions_taken": actions_taken,
                "priority_level": self._calculate_priority(analysis_result, customer_context),
                "estimated_completion_time": self._estimate_completion_time(workflow_path),
                "strategic_notes": self._generate_strategic_notes(analysis_result, customer_context)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Processing failed: {str(e)}",
                "review_id": review_input.get("id", "unknown") if 'review_input' in locals() else "unknown"
            }
    
    def _determine_workflow_path(self, analysis, customer_context, product_context) -> str:
        """Determina o caminho do workflow baseado na análise."""
        sentiment = analysis.get("sentiment", "").lower()
        urgency = analysis.get("urgency", "").lower()
        
        # Cliente VIP?
        is_vip = False
        if customer_context and customer_context.customer_tier in ["Platinum", "Gold"]:
            is_vip = True
        
        if sentiment == "positive":
            return "Archive"
        elif urgency == "high" or is_vip:
            return "Priority_Escalation"
        elif urgency == "medium":
            return "Response_And_Escalate"
        else:
            return "Response_Only"
    
    async def _execute_workflow_actions(self, workflow_path, analysis, customer_context, product_context, review_input):
        """Executa as ações baseadas no workflow path."""
        actions = []
        
        if workflow_path == "Archive":
            actions.append("Review archived - positive sentiment")
        
        elif workflow_path in ["Response_Only", "Response_And_Escalate", "Priority_Escalation"]:
            # Simular geração de resposta
            actions.append("Response generated")
            
            if workflow_path in ["Response_And_Escalate", "Priority_Escalation"]:
                actions.append("Escalation ticket created")
        
        return actions
    
    def _format_customer_context(self, customer_context):
        """Formata contexto do cliente."""
        if not customer_context:
            return {
                "tier": "Unknown",
                "lifetime_value": "Unknown",
                "previous_complaints": 0,
                "relationship_status": "Unknown"
            }
        
        return {
            "tier": customer_context.customer_tier,
            "lifetime_value": customer_context.lifetime_value,
            "previous_complaints": customer_context.previous_complaints,
            "relationship_status": "VIP" if customer_context.customer_tier in ["Platinum", "Gold"] else "Regular"
        }
    
    def _format_product_context(self, product_context):
        """Formata contexto do produto."""
        if not product_context:
            return {
                "common_issue": False,
                "warranty_applicable": True,
                "return_eligible": True
            }
        
        return {
            "common_issue": len(product_context.common_issues) > 0,
            "warranty_applicable": product_context.warranty_months > 0,
            "return_eligible": product_context.return_policy_days > 0
        }
    
    def _calculate_priority(self, analysis, customer_context):
        """Calcula prioridade (1-5)."""
        urgency = analysis.get("urgency", "").lower()
        
        if customer_context and customer_context.customer_tier == "Platinum":
            return 5
        elif urgency == "high":
            return 4
        elif urgency == "medium":
            return 3
        else:
            return 2
    
    def _estimate_completion_time(self, workflow_path):
        """Estima tempo de conclusão."""
        times = {
            "Archive": "Immediate",
            "Response_Only": "2 hours",
            "Response_And_Escalate": "4 hours",
            "Priority_Escalation": "1 hour"
        }
        return times.get(workflow_path, "2 hours")
    
    def _generate_strategic_notes(self, analysis, customer_context):
        """Gera notas estratégicas."""
        notes = []
        
        urgency = analysis.get("urgency", "").lower()
        sentiment = analysis.get("sentiment", "").lower()
        
        if urgency == "high":
            notes.append("High priority - immediate attention required")
        
        if customer_context and customer_context.customer_tier in ["Platinum", "Gold"]:
            notes.append("VIP customer - handle with priority")
        
        if sentiment == "negative" and len(analysis.get("key_issues", [])) > 2:
            notes.append("Multiple issues reported - comprehensive response needed")
        
        return "; ".join(notes) if notes else "Standard processing workflow"


def create_workflow_orchestrator_agent():
    """Cria e configura o agente Workflow Orchestrator."""
    return WorkflowOrchestrator()