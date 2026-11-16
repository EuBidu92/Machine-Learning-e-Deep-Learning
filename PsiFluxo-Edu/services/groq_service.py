"""Adaptado da integração OpenAI-compatible/Groq do PsiFluxo original."""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

class ConfiguracaoIAError(Exception):
    pass

class ServicoIAError(Exception):
    pass


def gerar_resposta(mensagens: list[dict[str, str]]) -> str:
    chave = os.getenv("GROQ_API_KEY", "").strip()
    if not chave:
        raise ConfiguracaoIAError("GROQ_API_KEY ausente")
    try:
        cliente = OpenAI(api_key=chave, base_url="https://api.groq.com/openai/v1", timeout=25.0, max_retries=1)
        resultado = cliente.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=mensagens, temperature=0.3, max_tokens=700,
        )
        texto = resultado.choices[0].message.content
        if not texto or not texto.strip():
            raise ServicoIAError("Resposta vazia")
        return texto.strip()
    except ServicoIAError:
        raise
    except Exception as exc:
        raise ServicoIAError("Erro de comunicação com o modelo") from exc
