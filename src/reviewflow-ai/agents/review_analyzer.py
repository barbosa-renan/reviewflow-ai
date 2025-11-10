"""
Review Analyzer Agent - Responsável por analisar sentimento e categorizar reviews.
"""

from autogen_ext.agents import Agent


def create_review_analyzer_agent():
    """Cria e configura o agente Review Analyzer."""
    
    prompt = """
You are a Review Analyzer agent for an e-commerce company. Your job is to analyze customer reviews and extract structured information.

IMPORTANT: Before processing, validate that the input contains required fields. If validation fails, return an error message.

INPUT FORMAT VALIDATION:
Required fields: text, customer_id, customer_name, product_name
Optional fields: id, product_id, purchase_date, rating

INPUT FORMAT:
{
  "id": "string (auto-generated if missing)",
  "text": "string (minimum 10 characters)",
  "customer_id": "string (e.g., 'CUST-12345')",
  "customer_name": "string",
  "product_name": "string", 
  "product_id": "string (optional)",
  "purchase_date": "string (optional)",
  "rating": "number 1-5 (optional)"
}

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

    agent = Agent(
        name="review_analyzer",
        instructions=prompt,
        model="gpt-4o-mini"
    )
    
    return agent


def create_review_analyzer_tool():
    """Cria a ferramenta do Review Analyzer para uso por outros agentes."""
    agent = create_review_analyzer_agent()
    
    return agent.as_tool(
        tool_name="review_analyzer",
        tool_description="Analyzes customer reviews and extracts structured information including sentiment, categories, urgency, and key issues."
    )