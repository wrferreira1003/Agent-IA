#!/usr/bin/env python3
"""
Testes unitários mais detalhados para as funções do Notion.
Execute: python test_notion_unit.py
"""

import sys
sys.path.append('.')

from app.agents.tools.notion_tools import create_notion_page_impl, read_notion_page, available_tools
import unittest
from unittest.mock import patch, MagicMock

class TestNotionFunctions(unittest.TestCase):
    """Testes unitários para as funções do Notion"""

    def test_available_tools_structure(self):
        """Testa se as ferramentas estão disponíveis corretamente"""
        self.assertIsInstance(available_tools, list)
        self.assertEqual(len(available_tools), 2)
        
        tool_names = [tool.__name__ for tool in available_tools]
        self.assertIn('create_notion_page', tool_names)
        self.assertIn('search_notion_pages', tool_names)

    def test_read_notion_page_success_format(self):
        """Testa se a leitura retorna o formato correto"""
        result = read_notion_page()
        
        # Verifica se não há erro
        self.assertNotIn("❌ Erro", result)
        
        # Verifica se contém elementos esperados
        self.assertIn("📄 Página do Notion:", result)
        self.assertIn("🔗 URL:", result)
        self.assertIn("📅 Criado:", result)
        self.assertIn("✏️ Última edição:", result)
        self.assertIn("📝 Blocos encontrados:", result)

    def test_create_notion_page_inputs(self):
        """Testa criação com diferentes tipos de entrada"""
        # Teste com conteúdo normal
        result1 = create_notion_page_impl("Teste Normal", "Conteúdo normal")
        self.assertIn("sucesso", result1.lower())
        
        # Teste com caracteres especiais
        result2 = create_notion_page_impl("Teste: Especial & ÇÃO", "Conteúdo com acentos: ção, ão")
        self.assertIn("sucesso", result2.lower())
        
        # Teste com conteúdo longo
        long_content = "Lorem ipsum " * 100
        result3 = create_notion_page_impl("Teste Longo", long_content)
        self.assertIn("sucesso", result3.lower())

    def test_notion_decorators(self):
        """Testa se os decoradores estão funcionando"""
        from app.agents.tools.notion_tools import create_notion_page, search_notion_pages
        
        # Verifica se as funções decoradas existem
        self.assertTrue(callable(create_notion_page))
        self.assertTrue(callable(search_notion_pages))
        
        # Verifica se têm docstrings
        self.assertIsNotNone(create_notion_page.__doc__)
        self.assertIsNotNone(search_notion_pages.__doc__)

    @patch('app.agents.tools.notion_tools.notion')
    def test_create_notion_page_error_handling(self, mock_notion):
        """Testa tratamento de erros na criação"""
        # Simula erro na API
        mock_notion.pages.create.side_effect = Exception("API Error")
        
        result = create_notion_page_impl("Test", "Content")
        self.assertIn("Falha", result)
        self.assertIn("API Error", result)

    @patch('app.agents.tools.notion_tools.notion')
    def test_read_notion_page_error_handling(self, mock_notion):
        """Testa tratamento de erros na leitura"""
        # Simula erro na API
        mock_notion.pages.retrieve.side_effect = Exception("Permission denied")
        
        result = read_notion_page()
        self.assertIn("❌ Erro", result)
        self.assertIn("Permission denied", result)

    def test_block_processing(self):
        """Testa se diferentes tipos de bloco são processados"""
        # Este teste verifica se a função funciona em uma página real
        result = read_notion_page()
        
        # Se não há erro, verifica se o processamento funciona
        if "❌ Erro" not in result:
            # Deve ter processado pelo menos alguns blocos
            self.assertIn("📝 Blocos encontrados:", result)

class TestNotionConfiguration(unittest.TestCase):
    """Testes para configuração do Notion"""

    def test_settings_import(self):
        """Testa se as configurações podem ser importadas"""
        from app.core.config import settings
        
        self.assertTrue(hasattr(settings, 'NOTION_API_KEY'))
        self.assertTrue(hasattr(settings, 'NOTION_DATABASE_ID'))

    def test_notion_client_initialization(self):
        """Testa se o cliente do Notion é inicializado corretamente"""
        from app.agents.tools.notion_tools import notion
        
        self.assertIsNotNone(notion)
        self.assertTrue(hasattr(notion, 'pages'))
        self.assertTrue(hasattr(notion, 'blocks'))

def run_specific_tests():
    """Executa testes específicos com relatório detalhado"""
    print("🧪 EXECUTANDO TESTES UNITÁRIOS DETALHADOS")
    print("=" * 60)
    
    # Testa configuração
    print("\n1. Testando configuração...")
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestNotionConfiguration)
        runner = unittest.TextTestRunner(verbosity=0, stream=open('/dev/null', 'w'))
        result = runner.run(suite)
        if result.wasSuccessful():
            print("   ✅ Configuração OK")
        else:
            print("   ❌ Problemas na configuração")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Testa estrutura das funções
    print("\n2. Testando estrutura das funções...")
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestNotionFunctions)
        runner = unittest.TextTestRunner(verbosity=0, stream=open('/dev/null', 'w'))
        result = runner.run(suite)
        success_count = result.testsRun - len(result.failures) - len(result.errors)
        print(f"   ✅ {success_count}/{result.testsRun} testes passaram")
        
        if result.failures:
            print(f"   ⚠️ {len(result.failures)} falhas")
        if result.errors:
            print(f"   ❌ {len(result.errors)} erros")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste funcional real
    print("\n3. Testando funcionalidade real...")
    try:
        result = read_notion_page()
        if "❌ Erro" not in result:
            print("   ✅ Leitura funcional")
        else:
            print("   ❌ Problema na leitura")
            
        result = create_notion_page_impl("Teste Unit", "Conteúdo de teste unitário")
        if "sucesso" in result.lower():
            print("   ✅ Criação funcional")
        else:
            print("   ❌ Problema na criação")
            
    except Exception as e:
        print(f"   ❌ Erro funcional: {e}")

if __name__ == "__main__":
    run_specific_tests()
    
    print("\n" + "=" * 60)
    print("Para executar testes completos com unittest:")
    print("python -m unittest test_notion_unit -v")