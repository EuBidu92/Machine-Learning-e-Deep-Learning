import json

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


# =====================================================
# 1. ESQUEMA DE CLASSIFICAÇÃO
# =====================================================

ESQUEMA_CLASSIFICACAO = {
    "type": "object",
    "properties": {
        "categoria": {
            "type": "string",
            "enum": ["python", "geral"]
        }
    },
    "required": ["categoria"],
    "additionalProperties": False
}


# =====================================================
# 2. CONFIGURAÇÃO DO MODELO
# =====================================================

llm_classificador = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    format=ESQUEMA_CLASSIFICACAO,
    num_predict=100
)


# =====================================================
# 3. INSTRUÇÕES DO CLASSIFICADOR
# =====================================================

INSTRUCOES = """
Você é um classificador de perguntas.

Sua única tarefa é selecionar qual agente deve
responder à pergunta do usuário.

Existem duas categorias:

PYTHON:
Perguntas relacionadas à programação Python.

Inclui:
- Sintaxe e comandos Python.
- Criação e correção de código.
- Funções, listas, tuplas e dicionários.
- Instalação de pacotes usando pip.
- Bibliotecas Python como Pandas e NumPy.
- Desenvolvimento de aplicações em Python.

Também pertencem à categoria python:

- O que é Python?
- Quais são as características da linguagem Python?
- Qual é a diferença entre Python e Java?
- Python é uma linguagem compilada ou interpretada?
- Quais são as vantagens de utilizar Python?

GERAL:
Perguntas sobre qualquer outro assunto.

Inclui:
- História.
- Geografia.
- Ciências.
- Matemática.
- Inteligência Artificial em geral.
- Conceitos de Machine Learning.
- Conhecimentos gerais.

EXEMPLOS:

Pergunta: Como instalar bibliotecas com pip?
Categoria: python

Pergunta: Como criar uma função em Python?
Categoria: python

Pergunta: Como utilizar Pandas para analisar dados?
Categoria: python

Pergunta: Como criar um dicionário em Python?
Categoria: python

Pergunta: O que é Python?
Categoria: python

Pergunta: Qual é a diferença entre Python e Java?
Categoria: python

Pergunta: O que é uma rede neural?
Categoria: geral

Pergunta: Como implementar uma rede neural utilizando Python?
Categoria: python

Pergunta: O que é Machine Learning?
Categoria: geral

Pergunta: Qual é a capital do Brasil?
Categoria: geral

Pergunta: Como treinar um modelo usando scikit-learn?
Categoria: python

Pergunta: O que é aprendizado supervisionado?
Categoria: geral

REGRAS IMPORTANTES:

1. Classifique a intenção principal da pergunta.
2. Não responda à pergunta do usuário.
3. Não forneça explicações.
4. Não inclua informações adicionais.
5. Retorne exclusivamente o JSON solicitado.
6. Utilize apenas as categorias "python" ou "geral".

REGRAS DE PRECISÃO:

1. Não apresente informações técnicas sem segurança.

2. Não invente características de linguagens,
bibliotecas ou ferramentas.

3. Em comparações, verifique se as propriedades
atribuídas a cada tecnologia estão corretas.

4. Ao explicar código, descreva exatamente
os elementos presentes no exemplo.

5. Diferencie criação, compilação, treinamento
e avaliação de modelos de Machine Learning.

6. Se não souber uma informação, informe
a limitação em vez de inventar uma resposta.

7. Prefira uma resposta curta e correta
a uma resposta longa e imprecisa.

"""


# =====================================================
# 4. FUNÇÃO DE CLASSIFICAÇÃO
# =====================================================

def classificar_pergunta(estado):

    pergunta = estado["pergunta"]

    print("\n[CLASSIFICADOR LLM - LLAMA 3.2 3B]")

    mensagens = [
        SystemMessage(content=INSTRUCOES),
        HumanMessage(content=pergunta)
    ]

    # Até duas tentativas de classificação
    for tentativa in range(1, 3):

        resposta = llm_classificador.invoke(mensagens)

        texto = str(resposta.content).strip()

        print(f"[DEBUG] Tentativa {tentativa}: {texto}")

        try:
            dados = json.loads(texto)

            # Verifica a estrutura do JSON
            if not isinstance(dados, dict):
                raise ValueError("Resposta não é um objeto JSON.")

            if set(dados.keys()) != {"categoria"}:
                raise ValueError("Estrutura JSON inválida.")

            categoria = dados["categoria"]

            # Verifica a categoria
            if categoria not in ("python", "geral"):
                raise ValueError("Categoria inválida.")

            print("[CLASSIFICADOR] Categoria:", categoria)

            return {
                "categoria": categoria
            }

        except (json.JSONDecodeError, ValueError) as erro:

            print("[AVISO] Resposta inválida:", erro)

            mensagens.append(resposta)

            mensagens.append(
                HumanMessage(
                    content=(
                        "Sua classificação anterior não respeitou "
                        "o formato exigido. "
                        'Responda exclusivamente com '
                        '{"categoria": "python"} ou '
                        '{"categoria": "geral"}.'
                    )
                )
            )

    raise ValueError(
        "A LLM não conseguiu produzir uma classificação válida."
    )