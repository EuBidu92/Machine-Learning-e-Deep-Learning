from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agentes.classificador import classificar_pergunta
from agentes.agente_python import agente_python
from agentes.agente_geral import agente_geral


# 1. Definição do estado compartilhado
class EstadoAssistente(TypedDict):
    pergunta: str
    categoria: str
    resposta: str


# 2. Função responsável pelo roteamento
def escolher_rota(estado: EstadoAssistente):
    return estado["categoria"]


# 3. Criação do grafo
grafo = StateGraph(EstadoAssistente)


# 4. Adição dos nós
grafo.add_node("classificador", classificar_pergunta)

grafo.add_node("python", agente_python)

grafo.add_node("geral", agente_geral)


# 5. Definição do início
grafo.add_edge(START, "classificador")


# 6. Roteamento condicional
grafo.add_conditional_edges(
    "classificador",
    escolher_rota,
    {
        "python": "python",
        "geral": "geral"
    }
)


# 7. Definição do encerramento
grafo.add_edge("python", END)

grafo.add_edge("geral", END)


# 8. Compilação do grafo
app = grafo.compile()