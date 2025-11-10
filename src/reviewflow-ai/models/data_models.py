"""
Modelos de dados para o sistema ReviewFlow AI.
Utiliza Pydantic para validação e serialização de dados.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class SentimentType(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class UrgencyLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ProblemCategory(str, Enum):
    PRODUCT_QUALITY = "Product_Quality"
    DELIVERY = "Delivery"
    CUSTOMER_SERVICE = "Customer_Service"
    PRICING = "Pricing"


class CustomerTier(str, Enum):
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


class ReviewInput(BaseModel):
    """Modelo para entrada de dados de review."""
    id: Optional[str] = None
    text: str = Field(min_length=10, description="Texto do review (mínimo 10 caracteres)")
    customer_id: str = Field(description="ID único do cliente")
    customer_name: str = Field(description="Nome do cliente")
    product_name: str = Field(description="Nome do produto")
    product_id: Optional[str] = "UNKNOWN"
    purchase_date: Optional[str] = "Unknown"
    rating: Optional[int] = Field(None, ge=1, le=5, description="Avaliação de 1 a 5")

    @validator('id', pre=True, always=True)
    def generate_id_if_missing(cls, v, values):
        if not v and 'text' in values:
            return f"REV-{hash(values['text']) % 10000:04d}"
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Produto excelente, superou minhas expectativas!",
                "customer_id": "CUST-12345",
                "customer_name": "João Silva",
                "product_name": "Smartphone XYZ Pro",
                "product_id": "PROD-001",
                "purchase_date": "2025-10-15",
                "rating": 5
            }
        }


class ReviewAnalysis(BaseModel):
    """Resultado da análise de review pelo Review Analyzer."""
    validation_status: str = Field(description="Status da validação: success ou error")
    error_message: Optional[str] = None
    sentiment: Optional[SentimentType] = None
    sentiment_score: Optional[int] = Field(None, ge=1, le=10)
    categories: List[ProblemCategory] = []
    urgency: Optional[UrgencyLevel] = None
    key_issues: List[str] = []
    customer_id: str
    customer_name: str
    product_name: str
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class ResponseGeneration(BaseModel):
    """Resultado da geração de resposta pelo Response Generator."""
    response_text: str = Field(description="Texto completo da resposta")
    compensation_offered: Optional[str] = None
    tone_used: str = Field(description="Tom utilizado: High_urgency, Medium_urgency ou Low_urgency")


class EscalationType(str, Enum):
    TECHNICAL = "Technical"
    COMMERCIAL = "Commercial"
    LEGAL = "Legal"


class PriorityLevel(str, Enum):
    P1 = "P1"  # Critical
    P2 = "P2"  # High
    P3 = "P3"  # Medium


class EscalationTicket(BaseModel):
    """Resultado da análise de escalação pelo Escalation Manager."""
    escalation_needed: bool
    escalation_type: Optional[EscalationType] = None
    priority: Optional[PriorityLevel] = None
    department: Optional[str] = None
    executive_summary: Optional[str] = None
    recommended_actions: List[str] = []
    suggested_timeline: Optional[str] = None
    customer_value: Optional[str] = None


class WorkflowPath(str, Enum):
    ARCHIVE = "Archive"
    RESPONSE_ONLY = "Response_Only"
    RESPONSE_AND_ESCALATE = "Response_And_Escalate"
    PRIORITY_ESCALATION = "Priority_Escalation"


class CustomerContext(BaseModel):
    """Contexto do cliente para decisões do workflow."""
    tier: CustomerTier
    lifetime_value: str
    previous_complaints: int
    relationship_status: str


class ProductContext(BaseModel):
    """Contexto do produto para decisões do workflow."""
    common_issue: bool
    warranty_applicable: bool
    return_eligible: bool


class WorkflowResult(BaseModel):
    """Resultado completo do processamento pelo Workflow Orchestrator."""
    review_id: str
    workflow_path: WorkflowPath
    customer_context: CustomerContext
    product_context: ProductContext
    agents_triggered: List[str]
    tools_used: List[str]
    priority_level: int = Field(ge=1, le=5)
    estimated_completion_time: str
    sla_status: str
    strategic_notes: str


class CustomerHistory(BaseModel):
    """Histórico completo do cliente."""
    customer_id: str
    customer_name: str
    email: str
    phone: str
    registration_date: str
    customer_tier: CustomerTier
    total_purchases: int
    total_spent: float
    lifetime_value: str
    previous_complaints: int
    complaint_history: List[Dict[str, Any]]
    recent_purchases: List[Dict[str, Any]]
    preferred_payment: str
    average_order_value: float


class ProductInfo(BaseModel):
    """Informações completas do produto."""
    product_id: str
    product_name: str
    category: str
    subcategory: str
    brand: str
    price: float
    original_price: float
    discount_percentage: int
    stock_status: str
    stock_quantity: int
    average_rating: float
    total_reviews: int
    description: str
    warranty_months: int
    warranty_type: str
    shipping_weight_kg: float
    dimensions: str
    common_issues: List[Dict[str, str]]
    return_policy_days: int
    supplier: str
    manufacturing_origin: str
    release_date: str


class ProcessingResult(BaseModel):
    """Resultado final do processamento completo de um review."""
    review_input: ReviewInput
    analysis: ReviewAnalysis
    response: Optional[ResponseGeneration] = None
    escalation: Optional[EscalationTicket] = None
    workflow: WorkflowResult
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "completed"
    errors: List[str] = []