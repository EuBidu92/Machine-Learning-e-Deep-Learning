
from services.ia_service import (
    gerar_resposta,
    ConfiguracaoIAError,
    ServicoIAError
)

print("TESTE DE INTEGRAÇÃO - PSIFLUXO EDU")
print("-" * 40)

mensagens = [
    {
        "role": "system",
        "content": (
            "Você é um professor de informática. "
            "Responda sempre em português brasileiro."
        )
    },
    {
        "role": "user",
        "content": (
            "Explique o que é Machine Learning "
            "em três frases simples."
        )
    }
]

try:
    resposta = gerar_resposta(mensagens)

    print("\nCONEXÃO REALIZADA COM SUCESSO!")
    print("\nRESPOSTA DA IA:")
    print(resposta)

except ConfiguracaoIAError as erro:
    print("\nERRO DE CONFIGURAÇÃO:")
    print(erro)

except ServicoIAError as erro:
    print("\nERRO NA COMUNICAÇÃO:")
    print(erro)

    if erro.__cause__:
        print("CAUSA:", erro.__cause__)

except Exception as erro:
    print("\nERRO INESPERADO:")
    print(type(erro).__name__, erro)
