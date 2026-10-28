from grafo.fluxo import app


def main():

    print("=" * 55)
    print(" ASSISTENTE INTELIGENTE - SENAI")
    print(" Python | LangGraph | LangChain | Ollama")
    print("=" * 55)

    print("\nDigite sua pergunta.")
    print("Para encerrar, digite 'sair'.")

    while True:

        pergunta = input("\nVocê: ").strip()

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("\nAssistente encerrado.")
            break

        if not pergunta:
            print("Digite uma pergunta válida.")
            continue

        estado_inicial = {
            "pergunta": pergunta,
            "categoria": "",
            "resposta": ""
        }

        try:
            resultado = app.invoke(estado_inicial)

            print("\n" + "=" * 55)
            print("AGENTE:", resultado["categoria"].upper())
            print("=" * 55)

            print("\nResposta:")
            print(resultado["resposta"])

        except Exception as erro:
            print("\nErro ao processar pergunta:")
            print(erro)


if __name__ == "__main__":
    main()