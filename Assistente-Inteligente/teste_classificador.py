from agentes.classificador import classificar_pergunta

testes = [
    ("Como instalar bibliotecas com pip?", "python"),
    ("Como criar uma função em Python?", "python"),
    ("Como utilizar Pandas para analisar dados?", "python"),
    ("Como criar um dicionário em Python?", "python"),
    ("Como treinar um modelo usando scikit-learn?", "python"),
    ("O que é Python?", "python"),
    ("Qual é a diferença entre Python e Java?", "python"),
    ("Como criar uma API usando FastAPI?", "python"),
    ("Como implementar uma rede neural utilizando Python?", "python"),
    ("Como tratar exceções em Python?", "python"),

    ("O que é Machine Learning?", "geral"),
    ("Qual é a capital do Brasil?", "geral"),
    ("O que é aprendizado supervisionado?", "geral"),
    ("O que é uma rede neural?", "geral"),
    ("Qual é a capital da Argentina?", "geral"),
    ("Quem descobriu a penicilina?", "geral"),
    ("O que é fotossíntese?", "geral"),
    ("Qual é a diferença entre clima e tempo?", "geral"),
    ("O que é inteligência artificial?", "geral"),
    ("Qual é a diferença entre aprendizado supervisionado e não supervisionado?", "geral"),
]

acertos = 0

for pergunta, esperado in testes:
    try:
        resultado = classificar_pergunta({"pergunta": pergunta})
        obtido = resultado["categoria"]
    except Exception as erro:
        obtido = f"ERRO: {erro}"

    correto = obtido == esperado

    if correto:
        acertos += 1

    print(f"\nPergunta: {pergunta}")
    print(f"Esperado: {esperado}")
    print(f"Obtido: {obtido}")
    print(f"Resultado: {'ACERTO' if correto else 'ERRO'}")

print("\n" + "=" * 50)
print(f"RESULTADO FINAL: {acertos}/{len(testes)}")
print(f"PRECISÃO: {acertos / len(testes) * 100:.1f}%")