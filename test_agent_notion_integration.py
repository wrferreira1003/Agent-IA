#!/usr/bin/env python3
"""
Teste de integração completa entre o agente e as ferramentas do Notion.
Verifica se o modelo Gemini está usando as ferramentas corretamente.
"""

import sys
import asyncio
sys.path.append('.')

from app.agents.main_agent import ChatAgent

async def test_agent_tool_integration():
    """Testa se o agente consegue usar as ferramentas do Notion"""
    print("🤖 TESTE DE INTEGRAÇÃO: AGENTE + FERRAMENTAS NOTION")
    print("=" * 60)
    
    try:
        # Inicializa o agente
        print("🚀 Inicializando agente...")
        agent = ChatAgent()
        print("✅ Agente inicializado com sucesso")
        
        # Lista de testes com diferentes tipos de perguntas
        test_cases = [
            {
                "name": "Consulta direta ao Notion",
                "prompt": "O que você tem no Notion? Me mostre o conteúdo disponível.",
                "expect_tool": "search_notion_pages"
            },
            {
                "name": "Pergunta sobre documentação",
                "prompt": "Quais informações existem sobre REST API com Django Ninja?",
                "expect_tool": "search_notion_pages"
            },
            {
                "name": "Criação de página",
                "prompt": "Crie uma página no Notion com título 'Teste de Integração' e conteúdo 'Esta página foi criada pelo teste de integração do agente.'",
                "expect_tool": "create_notion_page"
            },
            {
                "name": "Pergunta sem ferramenta",
                "prompt": "Qual é a capital do Brasil?",
                "expect_tool": None
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Teste {i}/{len(test_cases)}: {test_case['name']}")
            print("-" * 50)
            print(f"Prompt: {test_case['prompt']}")
            
            try:
                # Executa o teste
                response = await agent.get_response(test_case['prompt'])
                
                # Analisa o resultado
                used_tool = None
                if "search_notion_pages" in response.lower() or "página do notion" in response.lower():
                    used_tool = "search_notion_pages"
                elif "create_notion_page" in response.lower() or "página criada" in response.lower():
                    used_tool = "create_notion_page"
                
                # Verifica se a ferramenta esperada foi usada
                tool_correct = (test_case['expect_tool'] == used_tool)
                
                result = {
                    "test": test_case['name'],
                    "success": True,
                    "tool_used": used_tool,
                    "tool_expected": test_case['expect_tool'],
                    "tool_correct": tool_correct,
                    "response_length": len(response),
                    "error": None
                }
                
                print(f"✅ Resposta recebida: {len(response)} caracteres")
                print(f"🔧 Ferramenta usada: {used_tool or 'Nenhuma'}")
                print(f"🎯 Ferramenta esperada: {test_case['expect_tool'] or 'Nenhuma'}")
                print(f"✓ Correto: {'✅ Sim' if tool_correct else '❌ Não'}")
                
                # Mostra uma prévia da resposta
                preview = response[:200] + "..." if len(response) > 200 else response
                print(f"📝 Preview: {preview}")
                
            except Exception as e:
                result = {
                    "test": test_case['name'],
                    "success": False,
                    "tool_used": None,
                    "tool_expected": test_case['expect_tool'],
                    "tool_correct": False,
                    "response_length": 0,
                    "error": str(e)
                }
                print(f"❌ Erro: {e}")
            
            results.append(result)
        
        # Análise dos resultados
        print("\n" + "=" * 60)
        print("📊 ANÁLISE DOS RESULTADOS")
        print("=" * 60)
        
        successful_tests = sum(1 for r in results if r['success'])
        correct_tools = sum(1 for r in results if r['tool_correct'])
        
        print(f"📈 Testes executados: {len(results)}")
        print(f"✅ Testes bem-sucedidos: {successful_tests}/{len(results)}")
        print(f"🔧 Ferramentas corretas: {correct_tools}/{len(results)}")
        
        # Detalhes por teste
        for result in results:
            status = "✅" if result['success'] else "❌"
            tool_status = "🎯" if result['tool_correct'] else "❌"
            print(f"  {status} {tool_status} {result['test']}")
            if result['error']:
                print(f"      Erro: {result['error']}")
        
        # Conclusão
        success_rate = successful_tests / len(results) * 100
        tool_accuracy = correct_tools / len(results) * 100
        
        print(f"\n📊 Taxa de sucesso: {success_rate:.1f}%")
        print(f"🎯 Precisão das ferramentas: {tool_accuracy:.1f}%")
        
        if success_rate >= 75 and tool_accuracy >= 50:
            print("\n🎉 INTEGRAÇÃO FUNCIONANDO BEM!")
            return True
        else:
            print("\n⚠️ INTEGRAÇÃO PRECISA DE AJUSTES")
            return False
            
    except Exception as e:
        print(f"❌ Erro crítico no teste: {e}")
        return False

async def test_direct_model_tools():
    """Testa se o modelo tem as ferramentas registradas corretamente"""
    print("\n🔧 TESTE DE REGISTRO DAS FERRAMENTAS")
    print("=" * 60)
    
    try:
        from app.agents.models.gemini import GeminiModel
        
        model = GeminiModel()
        
        print(f"🔧 Número de ferramentas registradas: {len(model.tools)}")
        
        for i, tool in enumerate(model.tools, 1):
            print(f"  {i}. {tool.__name__}")
            print(f"     Descrição: {tool.__doc__}")
        
        # Verifica se as ferramentas esperadas estão presentes
        tool_names = [tool.__name__ for tool in model.tools]
        expected_tools = ['create_notion_page', 'search_notion_pages']
        
        missing_tools = [t for t in expected_tools if t not in tool_names]
        extra_tools = [t for t in tool_names if t not in expected_tools]
        
        print(f"\n✅ Ferramentas esperadas presentes: {len(expected_tools) - len(missing_tools)}/{len(expected_tools)}")
        
        if missing_tools:
            print(f"❌ Ferramentas faltando: {missing_tools}")
        
        if extra_tools:
            print(f"ℹ️ Ferramentas extras: {extra_tools}")
        
        return len(missing_tools) == 0
        
    except Exception as e:
        print(f"❌ Erro ao verificar ferramentas: {e}")
        return False

async def main():
    """Executa todos os testes de integração"""
    print("🚀 SUITE COMPLETA DE TESTES DE INTEGRAÇÃO")
    print("=" * 80)
    
    # Teste 1: Registro das ferramentas
    tools_ok = await test_direct_model_tools()
    
    # Teste 2: Integração completa
    integration_ok = await test_agent_tool_integration()
    
    # Resultado final
    print("\n" + "=" * 80)
    print("🏁 RESULTADO FINAL")
    print("=" * 80)
    print(f"🔧 Registro de ferramentas: {'✅ OK' if tools_ok else '❌ FALHA'}")
    print(f"🤖 Integração do agente: {'✅ OK' if integration_ok else '❌ FALHA'}")
    
    if tools_ok and integration_ok:
        print("\n🎉 SISTEMA TOTALMENTE INTEGRADO E FUNCIONANDO!")
        print("\n💡 O modelo Gemini está usando as ferramentas do Notion corretamente!")
    else:
        print("\n⚠️ SISTEMA PRECISA DE CORREÇÕES")
        
        if not tools_ok:
            print("   - Problema no registro das ferramentas")
        if not integration_ok:
            print("   - Problema na integração do agente")

if __name__ == "__main__":
    asyncio.run(main())