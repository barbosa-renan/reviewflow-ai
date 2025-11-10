"""
Review Analyzer Agent - Responsável por analisar sentimento e categorizar reviews.
"""

import json
import openai
from typing import Dict, Any
from ..models.data_models import ReviewAnalysis, SentimentType, UrgencyLevel, ProblemCategory


class ReviewAnalyzerAgent:
    """Agente para análise de reviews usando OpenAI diretamente."""
    
    def __init__(self):
        self.prompt = """
You are a Review Analyzer agent for an e-commerce company. Your job is to analyze customer reviews and extract structured information.

IMPORTANT: Before processing, validate that the input contains required fields. If validation fails, return an error message.

INPUT FORMAT VALIDATION:
Required fields: text, customer_id, customer_name, product_name
Optional fields: id, product_id, purchase_date, rating

YOUR TASKS:
1. Validate input format first
2. Analyze sentiment and assign score 1-10 (1=very negative, 10=very positive)
3. Classify sentiment as: Positive, Neutral, or Negative
4. Identify problem categories (can be multiple): Product_Quality, Delivery, Customer_Service, Pricing
5. Detect urgency level: Low, Medium, or High
6. Extract key issues mentioned

OUTPUT FORMAT (JSON only):
{
  "validation_status": "success|error",
  "error_message": "string (if validation failed)",
  "sentiment": "Positive|Neutral|Negative",
  "sentiment_score": 1-10,
  "categories": ["Product_Quality", "Delivery", "Customer_Service", "Pricing"],
  "urgency": "Low|Medium|High",
  "key_issues": ["list of specific problems mentioned"],
  "customer_id": "string",
  "customer_name": "string",
  "product_name": "string",
  "confidence_score": 0.0-1.0
}

VALIDATION RULES:
- If required fields missing: set validation_status="error" and provide error_message
- If text < 10 characters: validation error
- If rating exists but not 1-5: validation error
- Only proceed with analysis if validation_status="success"

URGENCY CLASSIFICATION:
- High: legal threats, safety issues, extreme dissatisfaction, VIP customers
- Medium: product defects, significant problems, multiple issues
- Low: minor complaints, suggestions, neutral feedback
"""
    
    async def analyze_review(self, review_data: str) -> Dict[str, Any]:
        """Analisa um review e retorna resultado estruturado."""
        try:
            client = openai.AsyncOpenAI()
            
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": f"Analyze this review: {review_data}"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                "validation_status": "error",
                "error_message": f"Processing error: {str(e)}",
                "sentiment": None,
                "sentiment_score": None,
                "categories": [],
                "urgency": None,
                "key_issues": [],
                "customer_id": "",
                "customer_name": "",
                "product_name": "",
                "confidence_score": 0.0
            }


def create_review_analyzer_agent():
    """Cria e configura o agente Review Analyzer."""
    return ReviewAnalyzerAgent()