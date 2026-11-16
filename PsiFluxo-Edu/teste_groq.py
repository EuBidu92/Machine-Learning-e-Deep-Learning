
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    cliente = OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
        timeout=30
    )

    modelo = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    print("Testando modelo:", modelo)

    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "user",
                "content": "Responda apenas: conexão funcionando."
            }
        ],
        max_tokens=50
    )

    print("SUCESSO!")
    print(resposta.choices[0].message.content)

except Exception as erro:
    print("ERRO:", type(erro).__name__)
    print("STATUS HTTP:", getattr(erro, "status_code", "não informado"))

    resposta = getattr(erro, "response", None)

    if resposta is not None:
        try:
            dados = resposta.json()
            detalhe = dados.get("error", {})

            print("CÓDIGO:", detalhe.get("code"))
            print("TIPO:", detalhe.get("type"))
            print("MENSAGEM:", detalhe.get("message"))

        except Exception:
            print("Não foi possível interpretar o erro.")
