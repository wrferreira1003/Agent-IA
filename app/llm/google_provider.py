import google.generativeai as genai
from app.llm.base import LLMProvider
from os import getenv

class GoogleProvider(LLMProvider):
    def __init__(self):
        genai.configure(api_key=getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def gerar_resposta(self, mensagem: str, contexto: str = "") -> str:
        prompt = f"Contexto:\n{contexto}\n\nPergunta: {mensagem}"
        resposta = self.model.generate_content(prompt)
        return resposta.text.strip()