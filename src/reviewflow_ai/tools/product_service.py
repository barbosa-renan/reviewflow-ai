"""
Funções mock para simular dados de produtos.
Em produção, essas funções se conectariam a um banco de dados real.
"""

from typing import Optional
from ..models.data_models import ProductInfo


def get_product_info(product_id: str) -> Optional[ProductInfo]:
    """
    Mock function para recuperar informações do produto baseado no ID.
    
    Args:
        product_id (str): Identificador único do produto
        
    Returns:
        ProductInfo | None: Informações do produto ou None se não encontrado
    """
    
    mock_products = {
        "PROD-001": {
            "product_id": "PROD-001",
            "product_name": "Smartphone XYZ Pro",
            "category": "Eletrônicos",
            "subcategory": "Smartphones",
            "brand": "TechBrand",
            "price": 1200.00,
            "original_price": 1499.00,
            "discount_percentage": 20,
            "stock_status": "Em estoque",
            "stock_quantity": 45,
            "average_rating": 4.2,
            "total_reviews": 328,
            "description": "Smartphone top de linha com câmera de 108MP, 5G, tela AMOLED 6.7\"",
            "warranty_months": 12,
            "warranty_type": "Garantia do fabricante",
            "shipping_weight_kg": 0.5,
            "dimensions": "16cm x 8cm x 0.9cm",
            "common_issues": [
                {
                    "issue": "Tela quebrada no transporte",
                    "frequency": "Média",
                    "resolution": "Troca imediata + reforço na embalagem"
                },
                {
                    "issue": "Bateria com desempenho abaixo do esperado",
                    "frequency": "Baixa",
                    "resolution": "Atualização de firmware ou troca"
                }
            ],
            "return_policy_days": 30,
            "supplier": "TechBrand Brasil",
            "manufacturing_origin": "China",
            "release_date": "2025-01-15"
        },
        
        "PROD-002": {
            "product_id": "PROD-002",
            "product_name": "Notebook Pro 15",
            "category": "Eletrônicos",
            "subcategory": "Notebooks",
            "brand": "CompuMax",
            "price": 3500.00,
            "original_price": 4200.00,
            "discount_percentage": 17,
            "stock_status": "Estoque baixo",
            "stock_quantity": 8,
            "average_rating": 4.7,
            "total_reviews": 156,
            "description": "Notebook profissional Intel i7, 16GB RAM, SSD 512GB, tela 15.6\" Full HD",
            "warranty_months": 24,
            "warranty_type": "Garantia estendida incluída",
            "shipping_weight_kg": 3.2,
            "dimensions": "36cm x 24cm x 2cm",
            "common_issues": [
                {
                    "issue": "Demora na entrega (produto importado)",
                    "frequency": "Alta",
                    "resolution": "Comunicação proativa sobre prazo + compensação"
                },
                {
                    "issue": "Teclado com teclas soltas",
                    "frequency": "Baixa",
                    "resolution": "Troca do teclado em assistência técnica"
                }
            ],
            "return_policy_days": 30,
            "supplier": "CompuMax Internacional",
            "manufacturing_origin": "Taiwan",
            "release_date": "2024-08-20"
        },
        
        "PROD-003": {
            "product_id": "PROD-003",
            "product_name": "Fone Bluetooth ABC Premium",
            "category": "Eletrônicos",
            "subcategory": "Áudio",
            "brand": "SoundWave",
            "price": 350.00,
            "original_price": 450.00,
            "discount_percentage": 22,
            "stock_status": "Em estoque",
            "stock_quantity": 120,
            "average_rating": 4.5,
            "total_reviews": 892,
            "description": "Fone Bluetooth com cancelamento de ruído, bateria 30h, resistente à água",
            "warranty_months": 12,
            "warranty_type": "Garantia do fabricante",
            "shipping_weight_kg": 0.3,
            "dimensions": "18cm x 15cm x 8cm (com case)",
            "common_issues": [
                {
                    "issue": "Problema de conexão Bluetooth",
                    "frequency": "Média",
                    "resolution": "Tutorial de reset + troca se persistir"
                },
                {
                    "issue": "Bateria não dura o anunciado",
                    "frequency": "Baixa",
                    "resolution": "Orientação de uso correto + troca"
                }
            ],
            "return_policy_days": 7,
            "supplier": "SoundWave Brasil",
            "manufacturing_origin": "Brasil",
            "release_date": "2024-11-10"
        },
        
        "PROD-004": {
            "product_id": "PROD-004",
            "product_name": "Smart TV 55\" 4K Ultra",
            "category": "Eletrônicos",
            "subcategory": "TVs",
            "brand": "VisionTech",
            "price": 2800.00,
            "original_price": 3500.00,
            "discount_percentage": 20,
            "stock_status": "Em estoque",
            "stock_quantity": 22,
            "average_rating": 4.6,
            "total_reviews": 445,
            "description": "Smart TV 55\" 4K, HDR, Android TV, 3 HDMI, 2 USB",
            "warranty_months": 12,
            "warranty_type": "Garantia do fabricante + suporte técnico",
            "shipping_weight_kg": 18.5,
            "dimensions": "123cm x 71cm x 8cm",
            "common_issues": [
                {
                    "issue": "Tela danificada no transporte",
                    "frequency": "Média",
                    "resolution": "Troca imediata + seguro de transporte"
                },
                {
                    "issue": "Problema com aplicativos travando",
                    "frequency": "Baixa",
                    "resolution": "Atualização de software + suporte técnico"
                },
                {
                    "issue": "Atraso na entrega por tamanho",
                    "frequency": "Alta",
                    "resolution": "Prazo realista + rastreamento prioritário"
                }
            ],
            "return_policy_days": 30,
            "supplier": "VisionTech Indústria",
            "manufacturing_origin": "Brasil",
            "release_date": "2025-03-01"
        },
        
        "PROD-005": {
            "product_id": "PROD-005",
            "product_name": "Mouse Wireless Ergonômico",
            "category": "Informática",
            "subcategory": "Periféricos",
            "brand": "ErgoTech",
            "price": 120.00,
            "original_price": 150.00,
            "discount_percentage": 20,
            "stock_status": "Em estoque",
            "stock_quantity": 250,
            "average_rating": 4.3,
            "total_reviews": 1024,
            "description": "Mouse wireless ergonômico, 6 botões, DPI ajustável, bateria recarregável",
            "warranty_months": 6,
            "warranty_type": "Garantia do fabricante",
            "shipping_weight_kg": 0.2,
            "dimensions": "12cm x 8cm x 5cm",
            "common_issues": [
                {
                    "issue": "Bateria não carrega",
                    "frequency": "Baixa",
                    "resolution": "Troca imediata do produto"
                },
                {
                    "issue": "Conexão USB instável",
                    "frequency": "Média",
                    "resolution": "Envio de novo adaptador USB + troca se necessário"
                }
            ],
            "return_policy_days": 7,
            "supplier": "ErgoTech Supply",
            "manufacturing_origin": "China",
            "release_date": "2024-06-15"
        }
        # Adicione mais produtos conforme necessário
    }
    
    product_data = mock_products.get(product_id)
    if product_data:
        return ProductInfo(**product_data)
    return None


def get_product_info_json(product_id: str) -> Optional[str]:
    """
    Versão que retorna JSON string para compatibilidade com agentes.
    """
    product = get_product_info(product_id)
    if product:
        return product.model_dump_json(indent=2, ensure_ascii=False)
    return None