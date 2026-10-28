from grafo.fluxo import app


testes = [
    {
        "pergunta": "Crie uma função Python que calcule o dobro de um número.",
        "categoria": "python"
    },
    {
        "pergunta": "Explique como instalar bibliotecas usando pip.",
        "categoria": "python"
    },
    {
        "pergunta": "Qual é a capital da França?",
        "categoria": "geral"
    },
    {
        "pergunta": "Explique o que é fotossíntese.",
        "categoria": "geral"
    }
]


acertos = 0

for numero, teste in enumerate(testes, 1):

    print("\n" + "=" * 60)
    print(f"TESTE DE INTEGRAÇÃO {numero}")
    print("=" * 60)

    pergunta = teste["pergunta"]

    estado_inicial = {
        "pergunta": pergunta,
        "categoria": "",
        "resposta": ""
    }

    try:
        resultado = app.invoke(estado_inicial)

        categoria = resultado["categoria"]
        resposta = resultado["resposta"]

        correto = categoria == teste["categoria"]

        if correto:
            acertos += 1

        print("\nPERGUNTA:")
        print(pergunta)

        print("\nCATEGORIA ESPERADA:")
        print(teste["categoria"])

        print("\nCATEGORIA OBTIDA:")
        print(categoria)

        print("\nRESULTADO DA CLASSIFICAÇÃO:")
        print("ACERTO" if correto else "ERRO")

        print("\nRESPOSTA GERADA:")
        print(resposta)

    except Exception as erro:
        print("\nERRO:")
        print(erro)


print("\n" + "=" * 60)
print("RESULTADO FINAL DA INTEGRAÇÃO")
print("=" * 60)

print(f"Classificações corretas: {acertos}/{len(testes)}")
print(f"Taxa de acerto: {acertos / len(testes) * 100:.1f}%")