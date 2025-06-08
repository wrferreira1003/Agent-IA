# 🔧 Guia de Configuração do Notion

## 📋 Checklist Rápido

### ✅ Etapa 1: Criar a Integração (se não fez ainda)
1. Acesse: https://www.notion.so/my-integrations
2. Clique **"+ New integration"**
3. Nome da integração: **"Capitão IA"**
4. Workspace: Selecione seu workspace
5. Clique **"Submit"**
6. **COPIE** o "Internal Integration Token" (API Key)
7. **COLE** no arquivo `.env` na linha `NOTION_API_KEY=`

### ✅ Etapa 2: Compartilhar a Página com a Integração
1. Abra sua página: https://www.notion.so/Projeto-PETCOMPARA-APP-79508c00b6324c9bbecd7ff2dcc7db4a

2. **Encontre o botão de compartilhamento** (pode ser):
   - **"Share"** (canto superior direito)
   - **"Compartilhar"** 
   - Ícone de pessoa 👤
   - Três pontos **"•••"**

3. **Na janela que abrir**, procure por:
   - **"Add people, emails, groups or integrations"**
   - **"Invite people"**
   - Campo de texto para adicionar pessoas

4. **Digite** "Capitão IA" ou o nome da sua integração

5. **Selecione** a integração da lista

6. **Defina permissões**:
   - **"Full access"** (recomendado)
   - ou **"Can edit"**

7. Clique **"Invite"** ou **"Add"**

## 🔍 Não encontra a integração?

Se não aparecer "Capitão IA" na busca:

### Opção A: Verificar se a integração existe
```bash
# Teste se sua API key funciona
curl -X POST 'https://api.notion.com/v1/search' \
  -H 'Authorization: Bearer SEU_NOTION_API_KEY' \
  -H 'Content-Type: application/json' \
  -H 'Notion-Version: 2022-06-28'
```

### Opção B: Recriar a integração
1. Vá para: https://www.notion.so/my-integrations
2. Se já existe uma integração, **delete** e crie nova
3. Certifique-se de copiar a API key correta

## 🧪 Testar se funcionou

Depois de configurar, teste:

```bash
# Teste direto no Docker
docker-compose exec api python test_notion_connection.py

# Ou via API
curl http://localhost:8000/api/v1/test_notion
```

## ❌ Problemas Comuns

### Erro: "Could not find page"
- ✅ A integração foi adicionada à página específica?
- ✅ A API key está correta no `.env`?
- ✅ A página realmente existe e está acessível?

### Erro: "Unauthorized" 
- ✅ A API key é válida?
- ✅ A integração tem as permissões corretas?

### Erro: "Integration not found"
- ✅ O nome da integração está correto?
- ✅ A integração está no mesmo workspace da página?

## 📞 Se ainda não funcionar

1. **Screenshot** da tela de compartilhamento
2. **Verifique** se a integração aparece em: https://www.notion.so/my-integrations
3. **Copie** o erro exato que aparece
4. **Teste** com uma página nova e simples primeiro

---

💡 **Dica**: A configuração mais comum que funciona é criar uma integração nova com nome simples como "test" e testar com uma página nova primeiro.