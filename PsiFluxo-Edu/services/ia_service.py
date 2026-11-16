
"""Integração do PsiFluxo Edu com provedores de IA.

Provedores:
- Ollama (local)
- Gemini
- Groq
- OpenRouter
- xAI (Grok)
"""

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


class ConfiguracaoIAError(Exception):
    """Erro de configuração da inteligência artificial."""
    pass


class ServicoIAError(Exception):
    """Erro de comunicação ou resposta da inteligência artificial."""
    pass


# Esquema para gerar exatamente uma questão.
ESQUEMA_QUESTAO = {
    "type": "object",
    "properties": {
        "questoes": {
            "type": "array",
            "minItems": 1,
            "maxItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "enunciado": {
                        "type": "string"
                    },
                    "alternativas": {
                        "type": "array",
                        "minItems": 4,
                        "maxItems": 4,
                        "items": {
                            "type": "string"
                        }
                    },
                    "correta": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 3
                    },
                    "explicacao": {
                        "type": "string"
                    }
                },
                "required": [
                    "enunciado",
                    "alternativas",
                    "correta",
                    "explicacao"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": ["questoes"],
    "additionalProperties": False
}


def gerar_resposta(
    mensagens: list[dict[str, str]]
) -> str:

    provedor = os.getenv(
        "AI_PROVIDER", "ollama"
    ).strip().lower()

    # =====================================
    # GEMINI
    # =====================================

    if provedor == "gemini":

        chave = os.getenv(
            "GEMINI_API_KEY", ""
        ).strip()

        if not chave:
            raise ConfiguracaoIAError(
                "GEMINI_API_KEY ausente"
            )

        modelo = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        instrucao = "\n".join(
            mensagem["content"]
            for mensagem in mensagens
            if mensagem["role"] == "system"
        )

        contents = [
            {
                "role": (
                    "model"
                    if mensagem["role"] == "assistant"
                    else "user"
                ),
                "parts": [
                    {"text": mensagem["content"]}
                ]
            }
            for mensagem in mensagens
            if mensagem["role"] != "system"
        ]

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1600
            }
        }

        if instrucao:
            payload["systemInstruction"] = {
                "parts": [{"text": instrucao}]
            }

        url = (
            "https://generativelanguage.googleapis.com/"
            f"v1beta/models/{modelo}:generateContent"
        )

        requisicao = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": chave
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(
                requisicao,
                timeout=60
            ) as resposta:
                dados = json.load(resposta)

            texto = "".join(
                parte.get("text", "")
                for parte in dados["candidates"][0]["content"]["parts"]
            )

        except Exception as erro:
            raise ServicoIAError(
                "Falha na comunicação com Gemini"
            ) from erro

    # =====================================
    # OLLAMA / GROQ / OPENROUTER / XAI
    # =====================================

    elif provedor in (
        "ollama",
        "groq",
        "openrouter",
        "xai"
    ):

        configuracoes = {
            "ollama": {
                "chave": None,
                "modelo": "OLLAMA_MODEL",
                "padrao": "llama3.2:3b",
                "base": os.getenv(
                    "OLLAMA_BASE_URL",
                    "http://127.0.0.1:11434/v1"
                ),
                "timeout": 180
            },
            "groq": {
                "chave": "GROQ_API_KEY",
                "modelo": "GROQ_MODEL",
                "padrao": "llama-3.1-8b-instant",
                "base": "https://api.groq.com/openai/v1",
                "timeout": 60
            },
            "openrouter": {
                "chave": "OPENROUTER_API_KEY",
                "modelo": "OPENROUTER_MODEL",
                "padrao": "",
                "base": "https://openrouter.ai/api/v1",
                "timeout": 60
            },
            "xai": {
                "chave": "XAI_API_KEY",
                "modelo": "XAI_MODEL",
                "padrao": "grok-4.7",
                "base": "https://api.x.ai/v1",
                "timeout": 60
            }
        }

        config = configuracoes[provedor]

        # Ollama não exige chave real.
        if provedor == "ollama":
            chave = "ollama"
        else:
            chave = os.getenv(
                config["chave"], ""
            ).strip()

            if not chave:
                raise ConfiguracaoIAError(
                    f'{config["chave"]} ausente'
                )

        modelo = os.getenv(
            config["modelo"],
            config["padrao"]
        ).strip()

        if not modelo:
            raise ConfiguracaoIAError(
                f'{config["modelo"]} ausente'
            )

        # Identifica solicitações de exercícios.
        conteudo = " ".join(
            mensagem.get("content", "")
            for mensagem in mensagens
        ).lower()

        gerar_questao = (
            "questoes" in conteudo
            and "alternativas" in conteudo
        )

        try:
            cliente = OpenAI(
                api_key=chave,
                base_url=config["base"],
                timeout=config["timeout"],
                max_retries=1
            )

            parametros = {
                "model": modelo,
                "messages": mensagens,
                "max_tokens": (
                    3500
                    if provedor == "ollama"
                    else 1600
                )
            }

            if provedor != "xai":
                parametros["temperature"] = 0.3

            # =====================================
            # JSON ESTRUTURADO PARA OLLAMA
            # =====================================

            if provedor == "ollama" and gerar_questao:

                parametros["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "questao_educacional",
                        "strict": True,
                        "schema": ESQUEMA_QUESTAO
                    }
                }

                print(
                    "[IA] Ollama: modo JSON estruturado ativado",
                    flush=True
                )

            # =====================================
            # CHAMADA AO MODELO
            # =====================================

            resposta = cliente.chat.completions.create(
                **parametros
            )

            texto = resposta.choices[0].message.content

        except Exception as erro:
            print(
                f"[IA] Erro no provedor {provedor}: {erro}",
                flush=True
            )

            raise ServicoIAError(
                f"Falha na comunicação com {provedor}"
            ) from erro

    else:
        raise ConfiguracaoIAError(
            f"AI_PROVIDER inválido: {provedor}"
        )

    if not texto or not texto.strip():
        raise ServicoIAError(
            "Resposta vazia do modelo"
        )

    return texto.strip()
