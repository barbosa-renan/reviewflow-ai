"""
Função para validação de dados de entrada de reviews.
"""

import json
from typing import Dict, Union
from ..models.data_models import ReviewInput


def validate_review_input(review_data: Union[str, Dict]) -> ReviewInput:
    """
    Valida e normaliza dados de entrada de review usando Pydantic.
    
    Args:
        review_data (str | Dict): JSON string ou dicionário com dados do review
        
    Returns:
        ReviewInput: Dados validados e normalizados
        
    Raises:
        ValueError: Se dados obrigatórios estão faltando ou formato inválido
    """
    try:
        if isinstance(review_data, str):
            data = json.loads(review_data)
        else:
            data = review_data
    except json.JSONDecodeError:
        raise ValueError("Formato JSON inválido nos dados do review")
    
    try:
        validated_review = ReviewInput(**data)
        return validated_review
    except Exception as e:
        raise ValueError(f"Erro na validação dos dados: {str(e)}")


def validate_and_serialize_review(review_data: Union[str, Dict]) -> str:
    """
    Valida dados de review e retorna JSON serializado.
    
    Args:
        review_data: Dados do review
        
    Returns:
        str: JSON string validado
    """
    validated_review = validate_review_input(review_data)
    return validated_review.model_dump_json(indent=2, ensure_ascii=False)