
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

try:
    cliente = OpenAI(
        api_key=os.environ["XAI_API_KEY"],
        base_url="https://api.x.ai/v1",
        timeout=60
    )

    print("Consultando modelos disponíveis...")
    modelos = cliente.models.list().data
    nomes = [modelo.id for modelo in modelos]

    for nome in nomes:
        print("-", nome)

    configurado = os.getenv("XAI_MODEL", "grok-4.7")

    if configurado not in nomes:
        raise ValueError(
            f"O modelo {configurado} não aparece na lista. "
            "Escolha um modelo de texto disponível."
        )

    print("\nTestando:", configurado)

    resposta = cliente.chat.completions.create(
        model=configurado,
        messages=[
            {
                "role": "user",
                "content": "Responda em português: o que é Python? Use uma frase."
            }
        ]
    )

    print("\nSUCESSO!")
    print(resposta.choices[0].message.content)

except Exception as erro:
    print("\nERRO:", type(erro).__name__)
    print("HTTP:", getattr(erro, "status_code", "não informado"))

    resposta = getattr(erro, "response", None)

    if resposta is not None:
        try:
            detalhe = resposta.json()
            print("DETALHES:", detalhe)
        except Exception:
            print("Resposta de erro indisponível.")
