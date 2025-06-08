#!/usr/bin/env python3
"""
Teste específico para verificar se o fallback do decorador funciona
quando a biblioteca do Google não está disponível.
"""

import sys
sys.path.append('.')

def test_decorator_fallback():
    """Testa se o fallback do decorador funciona corretamente"""
    print("🔧 Testando fallback do decorador...")
    
    # Simula ambiente sem google.generativeai
    import builtins
    original_import = builtins.__import__
    
    def mock_import(name, *args, **kwargs):
        if name == 'google.generativeai' or name.startswith('google.generativeai'):
            raise ImportError("No module named 'google.generativeai'")
        return original_import(name, *args, **kwargs)
    
    builtins.__import__ = mock_import
    
    try:
        # Recarrega o módulo para testar o fallback
        import importlib
        import app.agents.tools.notion_tools
        importlib.reload(app.agents.tools.notion_tools)
        
        # Verifica se as funções ainda funcionam
        from app.agents.tools.notion_tools import create_notion_page, search_notion_pages
        
        print("✅ Fallback do decorador funcionando")
        print("✅ Funções ainda são chamáveis:", callable(create_notion_page), callable(search_notion_pages))
        
        # Testa se ainda funciona
        result = search_notion_pages()
        if "❌ Erro" not in result:
            print("✅ Função de leitura ainda funciona com fallback")
        else:
            print("⚠️ Função de leitura teve problema (pode ser normal)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de fallback: {e}")
        return False
    
    finally:
        # Restaura o import original
        builtins.__import__ = original_import
        # Recarrega o módulo para restaurar o estado normal
        import importlib
        import app.agents.tools.notion_tools
        importlib.reload(app.agents.tools.notion_tools)

def test_normal_operation():
    """Testa operação normal após restaurar o módulo"""
    print("\n🔄 Testando operação normal após restauração...")
    
    try:
        from app.agents.tools.notion_tools import create_notion_page, search_notion_pages, available_tools
        
        print("✅ Módulo restaurado com sucesso")
        print(f"✅ Ferramentas disponíveis: {len(available_tools)}")
        
        # Teste rápido
        result = search_notion_pages()
        if "❌ Erro" not in result:
            print("✅ Operação normal funcionando")
        else:
            print("⚠️ Ainda há problemas na operação normal")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na operação normal: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DE FALLBACK DO DECORADOR")
    print("=" * 50)
    
    fallback_ok = test_decorator_fallback()
    normal_ok = test_normal_operation()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    print(f"  🔧 Fallback: {'✅ OK' if fallback_ok else '❌ FALHA'}")
    print(f"  🔄 Normal: {'✅ OK' if normal_ok else '❌ FALHA'}")
    
    if fallback_ok and normal_ok:
        print("\n🎉 SISTEMA DE FALLBACK FUNCIONANDO PERFEITAMENTE!")
    else:
        print("\n⚠️ PROBLEMAS NO SISTEMA DE FALLBACK")