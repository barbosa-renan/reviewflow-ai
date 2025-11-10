"""
Funções mock para simular dados de clientes.
Em produção, essas funções se conectariam a um banco de dados real.
"""

from typing import Optional, Dict, Any
from ..models.data_models import CustomerHistory, CustomerTier


def get_customer_history(customer_id: str) -> Optional[CustomerHistory]:
    """
    Mock function para recuperar informações do cliente baseado no ID.
    
    Args:
        customer_id (str): Identificador único do cliente
        
    Returns:
        CustomerHistory | None: Informações do cliente ou None se não encontrado
    """
    
    mock_customers = {
        "CUST-12345": {
            "customer_id": "CUST-12345",
            "customer_name": "João Silva",
            "email": "joao.silva@email.com",
            "phone": "+55 11 98765-4321",
            "registration_date": "2023-05-10",
            "customer_tier": "Gold",
            "total_purchases": 15,
            "total_spent": 4500.00,
            "lifetime_value": "High",
            "previous_complaints": 1,
            "complaint_history": [
                {
                    "date": "2024-08-15",
                    "issue": "Atraso na entrega",
                    "resolution": "Compensação com desconto de 15%",
                    "status": "Resolvido"
                }
            ],
            "recent_purchases": [
                {
                    "order_id": "ORD-789",
                    "product": "Smartphone XYZ",
                    "date": "2025-10-15",
                    "value": 1200.00,
                    "status": "Entregue"
                },
                {
                    "order_id": "ORD-756",
                    "product": "Fone Bluetooth ABC",
                    "date": "2025-09-20",
                    "value": 350.00,
                    "status": "Entregue"
                }
            ],
            "preferred_payment": "Cartão de Crédito",
            "average_order_value": 300.00
        },
        
        "CUST-67890": {
            "customer_id": "CUST-67890",
            "customer_name": "Maria Santos",
            "email": "maria.santos@email.com",
            "phone": "+55 21 91234-5678",
            "registration_date": "2025-01-15",
            "customer_tier": "Silver",
            "total_purchases": 3,
            "total_spent": 890.00,
            "lifetime_value": "Medium",
            "previous_complaints": 0,
            "complaint_history": [],
            "recent_purchases": [
                {
                    "order_id": "ORD-801",
                    "product": "Notebook Pro 15",
                    "date": "2025-10-20",
                    "value": 450.00,
                    "status": "Em trânsito"
                },
                {
                    "order_id": "ORD-745",
                    "product": "Mouse Wireless",
                    "date": "2025-08-10",
                    "value": 120.00,
                    "status": "Entregue"
                }
            ],
            "preferred_payment": "PIX",
            "average_order_value": 296.67
        },
        
        "CUST-11111": {
            "customer_id": "CUST-11111",
            "customer_name": "Carlos Oliveira",
            "email": "carlos.oliveira@email.com",
            "phone": "+55 31 99876-5432",
            "registration_date": "2024-11-20",
            "customer_tier": "Platinum",
            "total_purchases": 28,
            "total_spent": 12500.00,
            "lifetime_value": "Very High",
            "previous_complaints": 2,
            "complaint_history": [
                {
                    "date": "2025-06-10",
                    "issue": "Produto com defeito",
                    "resolution": "Troca imediata + desconto na próxima compra",
                    "status": "Resolvido"
                },
                {
                    "date": "2025-03-05",
                    "issue": "Atendimento inadequado",
                    "resolution": "Pedido de desculpas + cupom de R$100",
                    "status": "Resolvido"
                }
            ],
            "recent_purchases": [
                {
                    "order_id": "ORD-888",
                    "product": "Smart TV 55\"",
                    "date": "2025-10-25",
                    "value": 2800.00,
                    "status": "Processando"
                },
                {
                    "order_id": "ORD-850",
                    "product": "Soundbar Premium",
                    "date": "2025-09-30",
                    "value": 980.00,
                    "status": "Entregue"
                }
            ],
            "preferred_payment": "Cartão de Crédito",
            "average_order_value": 446.43
        },
        
        "CUST-22222": {
            "customer_id": "CUST-22222",
            "customer_name": "Ana Paula Costa",
            "email": "ana.costa@email.com",
            "phone": "+55 85 98123-4567",
            "registration_date": "2025-10-01",
            "customer_tier": "Bronze",
            "total_purchases": 1,
            "total_spent": 89.90,
            "lifetime_value": "Low",
            "previous_complaints": 0,
            "complaint_history": [],
            "recent_purchases": [
                {
                    "order_id": "ORD-900",
                    "product": "Capa para Celular",
                    "date": "2025-10-28",
                    "value": 89.90,
                    "status": "Entregue"
                }
            ],
            "preferred_payment": "Boleto",
            "average_order_value": 89.90
        },
        
        "CUST-33333": {
            "customer_id": "CUST-33333",
            "customer_name": "Pedro Henrique Lima",
            "email": "pedro.lima@email.com",
            "phone": "+55 41 97654-3210",
            "registration_date": "2024-03-22",
            "customer_tier": "Gold",
            "total_purchases": 12,
            "total_spent": 5600.00,
            "lifetime_value": "High",
            "previous_complaints": 3,
            "complaint_history": [
                {
                    "date": "2025-09-01",
                    "issue": "Produto errado enviado",
                    "resolution": "Troca + frete grátis",
                    "status": "Resolvido"
                },
                {
                    "date": "2025-05-15",
                    "issue": "Cobrança duplicada",
                    "resolution": "Estorno imediato",
                    "status": "Resolvido"
                },
                {
                    "date": "2024-12-20",
                    "issue": "Atraso de 10 dias",
                    "resolution": "Desconto de 20% aplicado",
                    "status": "Resolvido"
                }
            ],
            "recent_purchases": [
                {
                    "order_id": "ORD-920",
                    "product": "Teclado Mecânico RGB",
                    "date": "2025-10-30",
                    "value": 450.00,
                    "status": "Em separação"
                },
                {
                    "order_id": "ORD-890",
                    "product": "Webcam Full HD",
                    "date": "2025-10-05",
                    "value": 280.00,
                    "status": "Entregue"
                }
            ],
            "preferred_payment": "Cartão de Débito",
            "average_order_value": 466.67
        }
    }
    
    customer_data = mock_customers.get(customer_id)
    if customer_data:
        return CustomerHistory(**customer_data)
    return None


def get_customer_history_json(customer_id: str) -> Optional[str]:
    """
    Versão que retorna JSON string para compatibilidade com agentes.
    """
    customer = get_customer_history(customer_id)
    if customer:
        return customer.model_dump_json(indent=2, ensure_ascii=False)
    return None