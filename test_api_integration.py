#!/usr/bin/env python3
"""
Teste de integração da API com as ferramentas do Notion.
Testa se o endpoint funciona corretamente com chamadas de ferramentas.
"""

import sys
import asyncio
import requests
import time
sys.path.append('.')

def test_api_health():
    """Testa se a API está funcionando"""
    print("🏥 Testando saúde da API...")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ API está online")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        return False

def test_notion_endpoints():
    """Testa os endpoints específicos do Notion"""
    print("\n💬 Testando endpoints do Notion...")
    
    base_url = "http://localhost:8000"
    
    # Testa o endpoint de teste direto do Notion
    print("\n📋 Teste 1: Endpoint test_notion")
    print("-" * 50)
    
    try:
        response = requests.get(f"{base_url}/api/v1/test_notion", timeout=30)
        if response.status_code == 200:
            data = response.json()
            notion_result = data.get('notion_test', '')
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Resposta: {len(notion_result)} caracteres")
            
            if "❌ Erro" in notion_result:
                print("❌ Erro na conexão com Notion")
                print(f"Detalhes: {notion_result[:200]}...")
                return False
            else:
                print("✅ Conexão com Notion funcionando")
                print(f"Preview: {notion_result[:150]}...")
        else:
            print(f"❌ Falha: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    # Testa o endpoint do agente com ferramentas
    print("\n📋 Teste 2: Endpoint test_agent_tools")
    print("-" * 50)
    
    try:
        response = requests.get(f"{base_url}/api/v1/test_agent_tools", timeout=30)
        if response.status_code == 200:
            data = response.json()
            agent_response = data.get('agent_response', '')
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Resposta: {len(agent_response)} caracteres")
            print(f"Preview: {agent_response[:200]}...")
            
            # Verifica se o agente usou as ferramentas
            if "notion" in agent_response.lower() or "petcompara" in agent_response.lower():
                print("✅ Agente usou ferramentas do Notion")
                return True
            else:
                print("⚠️ Agente não usou ferramentas do Notion")
                return False
        else:
            print(f"❌ Falha: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_chat_endpoint_with_notion():
    """Testa o endpoint de chat com ferramentas do Notion"""
    print("\n💬 Testando endpoint de perguntas...")
    
    base_url = "http://localhost:8000"
    chat_url = f"{base_url}/api/v1/perguntar"
    
    test_cases = [
        {
            "name": "Consulta sobre projeto",
            "request": {
                "cliente_id": 1,
                "pergunta": "O que você sabe sobre o projeto no Notion?"
            },
            "expect_notion": True
        },
        {
            "name": "Pergunta simples",
            "request": {
                "cliente_id": 1,
                "pergunta": "Qual é a capital da França?"
            },
            "expect_notion": False
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Teste {i}/{len(test_cases)}: {test_case['name']}")
        print("-" * 50)
        
        try:
            print(f"📤 Enviando: {test_case['request']['pergunta']}")
            
            start_time = time.time()
            response = requests.post(
                chat_url, 
                json=test_case['request'],
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('resposta', '')
                
                # Verifica se usou ferramentas do Notion
                used_notion = any(keyword in response_text.lower() for keyword in [
                    'notion', 'página', 'search_notion_pages', 'create_notion_page',
                    'rest api', 'django ninja', 'url: https://'
                ])
                
                result = {
                    "name": test_case['name'],
                    "success": True,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "response_length": len(response_text),
                    "used_notion": used_notion,
                    "expected_notion": test_case['expect_notion'],
                    "notion_correct": used_notion == test_case['expect_notion'],
                    "error": None
                }
                
                print(f"✅ Status: {response.status_code}")
                print(f"⏱️ Tempo: {response_time:.2f}s")
                print(f"📝 Resposta: {len(response_text)} caracteres")
                print(f"🔧 Usou Notion: {'✅ Sim' if used_notion else '❌ Não'}")
                print(f"🎯 Esperado: {'✅ Sim' if test_case['expect_notion'] else '❌ Não'}")
                print(f"✓ Correto: {'✅ Sim' if result['notion_correct'] else '❌ Não'}")
                
                # Preview da resposta
                preview = response_text[:150] + "..." if len(response_text) > 150 else response_text
                print(f"📄 Preview: {preview}")
                
            else:
                result = {
                    "name": test_case['name'],
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "response_length": 0,
                    "used_notion": False,
                    "expected_notion": test_case['expect_notion'],
                    "notion_correct": False,
                    "error": f"HTTP {response.status_code}"
                }
                
                print(f"❌ Falha: HTTP {response.status_code}")
                print(f"📄 Resposta: {response.text}")
        
        except requests.exceptions.RequestException as e:
            result = {
                "name": test_case['name'],
                "success": False,
                "status_code": None,
                "response_time": None,
                "response_length": 0,
                "used_notion": False,
                "expected_notion": test_case['expect_notion'],
                "notion_correct": False,
                "error": str(e)
            }
            
            print(f"❌ Erro de conexão: {e}")
        
        results.append(result)
    
    # Análise dos resultados
    print("\n" + "=" * 60)
    print("📊 ANÁLISE DOS RESULTADOS DA API")
    print("=" * 60)
    
    successful_tests = sum(1 for r in results if r['success'])
    correct_notion = sum(1 for r in results if r['notion_correct'])
    
    print(f"📈 Testes executados: {len(results)}")
    print(f"✅ Testes bem-sucedidos: {successful_tests}/{len(results)}")
    print(f"🔧 Uso correto do Notion: {correct_notion}/{len(results)}")
    
    if successful_tests > 0:
        avg_time = sum(r['response_time'] for r in results if r['response_time']) / successful_tests
        print(f"⏱️ Tempo médio de resposta: {avg_time:.2f}s")
    
    # Detalhes por teste
    for result in results:
        status = "✅" if result['success'] else "❌"
        notion_status = "🎯" if result['notion_correct'] else "❌"
        print(f"  {status} {notion_status} {result['name']}")
        if result['error']:
            print(f"      Erro: {result['error']}")
    
    success_rate = successful_tests / len(results) * 100
    notion_accuracy = correct_notion / len(results) * 100
    
    print(f"\n📊 Taxa de sucesso: {success_rate:.1f}%")
    print(f"🎯 Precisão Notion: {notion_accuracy:.1f}%")
    
    return success_rate >= 75 and notion_accuracy >= 66

def main():
    """Executa todos os testes da API"""
    print("🚀 TESTE DE INTEGRAÇÃO DA API COM NOTION")
    print("=" * 70)
    
    # Verifica se a API está online
    api_online = test_api_health()
    
    if not api_online:
        print("\n❌ API não está acessível")
        print("\n💡 Para iniciar a API:")
        print("   docker-compose up --build")
        print("   ou")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return
    
    # Testa os endpoints específicos do Notion
    notion_endpoints_ok = test_notion_endpoints()
    
    # Testa o endpoint de chat/pergunta
    chat_working = test_chat_endpoint_with_notion()
    
    # Resultado final
    print("\n" + "=" * 70)
    print("🏁 RESULTADO FINAL")
    print("=" * 70)
    print(f"🏥 API Online: {'✅ OK' if api_online else '❌ FALHA'}")
    print(f"🔧 Endpoints Notion: {'✅ OK' if notion_endpoints_ok else '❌ FALHA'}")
    print(f"💬 Chat + Notion: {'✅ OK' if chat_working else '❌ FALHA'}")
    
    if api_online and notion_endpoints_ok and chat_working:
        print("\n🎉 API TOTALMENTE FUNCIONAL COM NOTION!")
        print("\n💡 O endpoint está processando ferramentas corretamente!")
    else:
        print("\n⚠️ API PRECISA DE CORREÇÕES")

if __name__ == "__main__":
    main()