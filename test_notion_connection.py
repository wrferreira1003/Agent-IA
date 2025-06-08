#!/usr/bin/env python3
"""
Script para testar a conexão com o Notion após configurar as permissões.
Execute: python test_notion_connection.py
"""

import os
import sys
sys.path.append('.')

from app.agents.tools.notion_tools import read_notion_page

def test_notion_connection():
    print("🚀 Testando conexão com o Notion...")
    print("📄 Página: REST API's com Django Ninja")
    print("🔑 Page ID: f75599ed25fa404dac7b7ae4ba84830b")
    print("🌐 URL: https://www.notion.so/REST-API-s-com-Django-Ninja-f75599ed25fa404dac7b7ae4ba84830b")
    print("=" * 50)
    
    result = read_notion_page()
    
    if "Erro" in result:
        print("❌ ERRO: Ainda não há permissão para acessar o Notion")
        print("\n📝 Para resolver:")
        print("1. Abra: https://www.notion.so/REST-API-s-com-Django-Ninja-f75599ed25fa404dac7b7ae4ba84830b")
        print("2. Clique 'Share' no canto superior direito")
        print("3. Clique 'Add people, emails, groups or integrations'")
        print("4. Adicione sua integração 'Capitão IA'")
        print("5. Defina permissões como 'Full access' ou 'Edit'")
        print("6. Execute este script novamente")
    else:
        print("✅ SUCESSO: Conexão com Notion funcionando!")
        print("\n📋 Informações encontradas:")
    
    print("\n" + "=" * 50)
    print(result)
    print("=" * 50)

if __name__ == "__main__":
    test_notion_connection()