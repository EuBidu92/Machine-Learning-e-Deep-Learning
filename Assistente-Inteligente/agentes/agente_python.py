from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


llm_python = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    num_predict=500
)


def agente_python(estado):

    pergunta = estado["pergunta"]

    instrucoes = """
Você é um professor de programação Python.

Responda em português brasileiro.

REGRAS:

1. Responda exatamente ao assunto perguntado.

2. Explique o conceito em no máximo
   três frases curtas.

3. Quando apropriado, apresente apenas
   um exemplo de código Python.

4. O exemplo deve ser simples, correto
   e diretamente relacionado à pergunta.

5. Explique o exemplo brevemente.

6. Não repita exemplos.

7. Não inclua saudações ou conclusões genéricas.

8. Não invente comandos, bibliotecas ou resultados.

9. Se a pergunta mencionar Pandas,
   utilize Pandas no exemplo.

10. Se a pergunta mencionar pip,
    explique o comando de instalação.

11. Não acrescente assuntos que não foram solicitados.

FORMATO:

Explicação:
[Explicação objetiva]

Exemplo:
[Um exemplo, quando necessário]

Funcionamento:
[Breve explicação]
"""

    mensagens = [
        SystemMessage(content=instrucoes),
        HumanMessage(content=pergunta)
    ]

    resposta = llm_python.invoke(mensagens)

    return {
        "resposta": resposta.content
    }