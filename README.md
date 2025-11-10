# ReviewFlow AI 🤖

Sistema inteligente de gerenciamento de reviews de e-commerce usando agentes AI especializados.

## Visão Geral

O ReviewFlow AI é um sistema multi-agente que automatiza o processamento de reviews de clientes, incluindo:

- **Análise de Sentimento**: Classificação automática de sentimentos e urgência
- **Geração de Respostas**: Respostas personalizadas e empáticas
- **Escalação Inteligente**: Identificação de casos críticos
- **Orquestração Workflow**: Coordenação inteligente entre agentes

## Arquitetura

```
reviewflow-ai/
├── app.py                      # API principal (FastAPI)
├── src/reviewflow-ai/
│   ├── agents/                 # Agentes especializados
│   │   ├── review_analyzer.py     # Análise de sentimento
│   │   ├── response_generator.py  # Geração de respostas
│   │   ├── escalation_manager.py  # Gestão de escalações
│   │   └── workflow_orchestrator.py # Coordenação
│   ├── models/                 # Modelos de dados (Pydantic)
│   │   └── data_models.py
│   ├── tools/                  # Ferramentas utilitárias
│   │   ├── validation.py          # Validação de dados
│   │   ├── customer_service.py    # Serviços de cliente
│   │   └── product_service.py     # Serviços de produto
│   └── config.py              # Configurações
├── requirements.txt           # Dependências
├── Dockerfile                # Container Docker
├── docker-compose.yml        # Orquestração
└── test_api.py              # Testes da API
```

## Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone <repository-url>
cd reviewflow-ai
```

### 2. Configurar Ambiente Virtual
```bash
# Python
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env e adicionar sua chave OpenAI
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Executar a Aplicação

#### Desenvolvimento Local
```bash
python app.py
```

#### Produção com Docker
```bash
# Build e execução
docker-compose up --build

# Apenas execução (após build)
docker-compose up
```

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

#### Health Check
```bash
GET /health
```

#### Processar Review Individual
```bash
POST /api/v1/reviews/process
Content-Type: application/json

{
  "text": "Produto excelente, superou expectativas!",
  "customer_id": "CUST-12345",
  "customer_name": "João Silva",
  "product_name": "Smartphone XYZ Pro",
  "rating": 5
}
```

#### Processamento em Lote
```bash
POST /api/v1/reviews/batch
Content-Type: application/json

[
  {
    "text": "Review 1...",
    "customer_id": "CUST-001",
    // ...
  },
  {
    "text": "Review 2...",
    "customer_id": "CUST-002",
    // ...
  }
]
```

#### Estatísticas
```bash
GET /api/v1/stats
```

## Testes

### Testar API Local
```bash
python test_api.py
```

### Testes Unitários (futuro)
```bash
pytest tests/
```

## Configuração Avançada

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `OPENAI_API_KEY` | Chave da API OpenAI (obrigatório) | - |
| `API_HOST` | Host da API | `0.0.0.0` |
| `API_PORT` | Porta da API | `8000` |
| `OPENAI_MODEL` | Modelo OpenAI a usar | `gpt-4o-mini` |
| `LOG_LEVEL` | Nível de log | `INFO` |
| `MAX_BATCH_SIZE` | Tamanho máximo do lote | `100` |

### Modelos de Dados

O sistema usa **Pydantic** para validação automática:

```python
class ReviewInput(BaseModel):
    text: str = Field(min_length=10)
    customer_id: str
    customer_name: str
    product_name: str
    rating: Optional[int] = Field(None, ge=1, le=5)
```

## 🏭 Deploy em Produção

### Docker
```bash
# Build da imagem
docker build -t reviewflow-ai .

# Executar container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  reviewflow-ai
```

### Docker Compose
```bash
# Configurar .env com suas credenciais
# Executar
docker-compose up -d
```

### Cloud Platforms

#### AWS ECS/Fargate
1. Push da imagem para ECR
2. Criar task definition
3. Deploy no ECS

#### Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name reviewflow-ai \
  --image myregistry.azurecr.io/reviewflow-ai \
  --environment-variables OPENAI_API_KEY=your_key
```

## Monitoramento

### Logs
```bash
# Docker Compose
docker-compose logs -f reviewflow-api

# Logs locais
tail -f logs/app.log
```

### Métricas (futuro)
- Tempo de processamento por review
- Taxa de escalação
- Distribuição de sentimentos
- Performance dos agentes

## 🛠️ Desenvolvimento

### Adicionar Novo Agente

1. Criar arquivo em `src/reviewflow-ai/agents/`
2. Implementar função `create_agent()`
3. Adicionar ao workflow orchestrator
4. Atualizar imports em `__init__.py`

### Conectar Banco de Dados Real

1. Atualizar `tools/customer_service.py`
2. Substituir funções mock por queries reais
3. Adicionar configuração de DB em `config.py`

### Adicionar Cache Redis

1. Instalar `redis` e `aioredis`
2. Configurar em `config.py`
3. Implementar cache nos tools

## Exemplo de Uso

```python
import httpx
import asyncio

async def process_review():
    async with httpx.AsyncClient() as client:
        review = {
            "text": "Produto chegou danificado, preciso de troca urgente!",
            "customer_id": "CUST-123",
            "customer_name": "Maria Silva",
            "product_name": "Notebook Gaming"
        }
        
        response = await client.post(
            "http://localhost:8000/api/v1/reviews/process",
            json=review
        )
        
        result = response.json()
        print(f"Review processado: {result['workflow']['workflow_path']}")

# Executar
asyncio.run(process_review())
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## Suporte

- **Issues**: Use GitHub Issues para reportar bugs
- **Documentação**: Acesse `/docs` quando a API estiver rodando
- **Logs**: Verifique os logs para debugging

---
