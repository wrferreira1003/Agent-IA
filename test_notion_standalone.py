#!/usr/bin/env python3
"""
Teste isolado das funções do Notion para verificar se estão funcionando corretamente.
Execute: python test_notion_standalone.py
"""

import os
import sys
sys.path.append('.')

from app.agents.tools.notion_tools import create_notion_page_impl, read_notion_page

def test_notion_read():
    """Testa a função de leitura da página do Notion"""
    print("🔍 Testando leitura da página do Notion...")
    print("-" * 50)
    
    try:
        result = read_notion_page()
        
        if "❌ Erro" in result:
            print("❌ FALHA: Erro ao ler página do Notion")
            print(f"Detalhes: {result}")
            return False
        else:
            print("✅ SUCESSO: Página lida com sucesso")
            print(f"Conteúdo obtido: {len(result)} caracteres")
            print(f"Preview: {result[:200]}...")
            return True
            
    except Exception as e:
        print(f"❌ FALHA: Exceção durante leitura - {e}")
        return False

def test_notion_create():
    """Testa a função de criação de página no Notion"""
    print("\n📝 Testando criação de página no Notion...")
    print("-" * 50)
    
    try:
        title = "Teste de Criação - Função Isolada"
        content = "Esta é uma página de teste criada pela função isolada de criação do Notion."
        
        result = create_notion_page_impl(title, content)
        
        if "Falha" in result:
            print("❌ FALHA: Erro ao criar página no Notion")
            print(f"Detalhes: {result}")
            return False
        else:
            print("✅ SUCESSO: Página criada com sucesso")
            print(f"Resultado: {result}")
            return True
            
    except Exception as e:
        print(f"❌ FALHA: Exceção durante criação - {e}")
        return False

def test_configuration():
    """Verifica se as configurações do Notion estão corretas"""
    print("\n⚙️ Verificando configurações do Notion...")
    print("-" * 50)
    
    try:
        from app.core.config import settings
        
        # Verifica se as variáveis estão definidas
        api_key = getattr(settings, 'NOTION_API_KEY', None)
        db_id = getattr(settings, 'NOTION_DATABASE_ID', None)
        
        if not api_key:
            print("❌ NOTION_API_KEY não está definida")
            return False
        
        if not db_id:
            print("❌ NOTION_DATABASE_ID não está definida")
            return False
        
        print(f"✅ NOTION_API_KEY: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
        print(f"✅ NOTION_DATABASE_ID: {db_id}")
        
        # Verifica se o cliente pode ser inicializado
        import notion_client
        client = notion_client.Client(auth=api_key)
        print("✅ Cliente Notion inicializado com sucesso")
        
        return True
        
    except Exception as e:
        print(f"❌ FALHA: Erro na configuração - {e}")
        return False

def main():
    """Executa todos os testes das funções do Notion"""
    print("🚀 TESTE ISOLADO DAS FUNÇÕES DO NOTION")
    print("=" * 60)
    
    # Testa configuração
    config_ok = test_configuration()
    
    if not config_ok:
        print("\n❌ TESTE INTERROMPIDO: Configurações incorretas")
        print("\nVerifique se o arquivo .env contém:")
        print("NOTION_API_KEY=your_notion_api_key")
        print("NOTION_DATABASE_ID=your_page_id")
        return
    
    # Testa leitura
    read_ok = test_notion_read()
    
    # Testa criação
    create_ok = test_notion_create()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL:")
    print(f"  🔧 Configuração: {'✅ OK' if config_ok else '❌ FALHA'}")
    print(f"  📖 Leitura: {'✅ OK' if read_ok else '❌ FALHA'}")
    print(f"  📝 Criação: {'✅ OK' if create_ok else '❌ FALHA'}")
    
    if all([config_ok, read_ok, create_ok]):
        print("\n🎉 TODAS AS FUNÇÕES DO NOTION ESTÃO FUNCIONANDO!")
    else:
        print("\n⚠️ ALGUMAS FUNÇÕES APRESENTARAM PROBLEMAS")
        
        if not read_ok:
            print("\n💡 Para corrigir problemas de leitura:")
            print("1. Verifique se a integração tem acesso à página")
            print("2. Confirme o ID da página no NOTION_DATABASE_ID")
            
        if not create_ok:
            print("\n💡 Para corrigir problemas de criação:")
            print("1. Verifique se a integração tem permissões de escrita")
            print("2. Confirme se o ID é de uma página (não database)")

if __name__ == "__main__":
    main()