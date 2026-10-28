from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


llm_geral = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    num_predict=500
)


def agente_geral(estado):

    pergunta = estado["pergunta"]

    instrucoes = """
Você é um assistente educacional de conhecimentos gerais.

Responda em português brasileiro.

REGRAS:

1. Responda diretamente à pergunta.

2. Utilize linguagem simples e objetiva.

3. Prefira explicações curtas.

4. Não repita informações.

5. Não invente fatos, números ou datas.

6. Se não souber uma informação,
   reconheça sua limitação.

7. Não inclua saudações desnecessárias.

8. Não acrescente assuntos que não foram solicitados.

9. Em perguntas factuais, priorize precisão.

10. Evite afirmações excessivamente específicas
    quando não tiver segurança sobre elas.
"""

    mensagens = [
        SystemMessage(content=instrucoes),
        HumanMessage(content=pergunta)
    ]

    resposta = llm_geral.invoke(mensagens)

    return {
        "resposta": resposta.content
    }