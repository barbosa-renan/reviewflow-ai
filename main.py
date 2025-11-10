"""
Main entry point para ReviewFlow AI - gerencia PYTHONPATH automaticamente
"""
import sys
import os

# Adicionar o diretório atual ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Agora importar e executar o app
from app import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )