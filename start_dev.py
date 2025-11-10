#!/usr/bin/env python3
"""
Script de inicialização do ReviewFlow AI
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    return True

def check_env_file():
    """Verifica se o arquivo .env existe."""
    if not os.path.exists('.env'):
        print("⚠️  Arquivo .env não encontrado")
        print("📋 Copiando .env.example para .env")
        
        if os.path.exists('.env.example'):
            if platform.system() == "Windows":
                subprocess.run(['copy', '.env.example', '.env'], shell=True)
            else:
                subprocess.run(['cp', '.env.example', '.env'])
            
            print("✅ Arquivo .env criado")
            print("🔧 Configure sua OPENAI_API_KEY no arquivo .env")
        else:
            print("❌ Arquivo .env.example não encontrado")
            return False
    return True

def install_dependencies():
    """Instala as dependências."""
    print("📦 Instalando dependências...")
    
    try:
        # Tentar usar requirements de produção primeiro
        if os.path.exists('requirements-production.txt'):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-production.txt'])
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_directories():
    """Cria diretórios necessários."""
    directories = ['logs', 'data', 'temp']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Diretório '{directory}' criado")

def run_development_server():
    """Inicia o servidor de desenvolvimento."""
    print("\n🚀 Iniciando servidor de desenvolvimento...")
    print("📡 API disponível em: http://localhost:8000")
    print("📚 Documentação em: http://localhost:8000/docs")
    print("🔍 Health check em: http://localhost:8000/health")
    print("\n💡 Use Ctrl+C para parar o servidor")
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Servidor parado")

def main():
    """Função principal."""
    print("🤖 ReviewFlow AI - Inicializador de Desenvolvimento")
    print("=" * 50)
    
    # Verificações preliminares
    if not check_python_version():
        return
    
    if not check_env_file():
        return
    
    # Instalação e configuração
    create_directories()
    
    if not install_dependencies():
        return
    
    # Iniciar servidor
    run_development_server()

if __name__ == "__main__":
    main()