
"""Geração de questões progressivas e correção determinística."""

import json
import re

from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)

from services.ia_service import gerar_resposta, ServicoIAError


class PedidoQuiz(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    tema: str = Field(min_length=3, max_length=200)

    nivel: Literal[
        "iniciante",
        "intermediario",
        "avancado"
    ] = "iniciante"

    quantidade: int = Field(
        default=1,
        ge=1,
        le=5,
        strict=True
    )


class Questao(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enunciado: str = Field(min_length=10, max_length=700)

    alternativas: list[str] = Field(
        min_length=4,
        max_length=4
    )

    correta: int = Field(ge=0, le=3)

    explicacao: str = Field(
        min_length=10,
        max_length=900
    )

    @field_validator("alternativas")
    @classmethod
    def validar_alternativas(cls, valores):
        if any(
            not isinstance(item, str)
            or len(item.strip()) < 2
            or len(item) > 400
            for item in valores
        ):
            raise ValueError("Alternativa inválida")

        if len(set(
            item.strip().lower()
            for item in valores
        )) != 4:
            raise ValueError("Alternativas repetidas")

        return valores


ABORDAGENS = [
    "Conceitos fundamentais e definições específicas",
    "Aplicações práticas e exemplos reais",
    "Comparação entre conceitos relacionados",
    "Situações-problema e tomada de decisão",
    "Identificação de erros e interpretações",
    "Análise de cenários e consequências",
    "Relações entre diferentes conceitos",
    "Aplicação do conhecimento em situações novas"
]


def gerar_quiz(
    pedido: PedidoQuiz,
    historico: list[str] | None = None
) -> list[Questao]:
    """Gera uma questão considerando perguntas anteriores."""

    historico = historico or []

    numero = len(historico)

    abordagem = ABORDAGENS[
        numero % len(ABORDAGENS)
    ]

    anteriores = "\n".join(
        f"- {pergunta}"
        for pergunta in historico[-12:]
    )

    sistema = (
        "Você é um professor brasileiro especializado "
        "em avaliação educacional. "

        "Crie exatamente UMA questão de múltipla escolha. "

        "A questão deve avaliar a compreensão do estudante "
        "e explorar aspectos específicos do tema. "

        "Evite perguntas excessivamente genéricas. "

        "Não repita questões anteriores nem reformule "
        "uma pergunta já apresentada com outras palavras. "

        "Varie conceitos, exemplos, aplicações e situações. "

        "Crie exatamente QUATRO alternativas diferentes. "

        "Apenas uma alternativa deve estar correta. "

        "Retorne exclusivamente um objeto JSON contendo "
        "a propriedade questoes com uma lista de um elemento. "

        "Cada questão deve conter os campos enunciado, "
        "alternativas, correta e explicacao. "

        "Alternativas deve ser uma lista de quatro strings. "

        "Correta deve ser um número inteiro entre 0 e 3. "

        "A explicação deve justificar a resposta correta. "

        "Escreva em português brasileiro."
    )

    ultimo_erro = None

    for tentativa in range(1, 4):

        usuario = (
            f"Tema: {pedido.tema}\n"
            f"Nível: {pedido.nivel}\n"
            f"Questão número: {numero + 1}\n"
            f"Abordagem obrigatória: {abordagem}\n\n"
            "QUESTÕES ANTERIORES QUE NÃO PODEM SER REPETIDAS:\n"
            f"{anteriores or 'Nenhuma'}\n\n"
            "Gere UMA questão inédita com quatro alternativas."
        )

        texto = gerar_resposta([
            {
                "role": "system",
                "content": sistema
            },
            {
                "role": "user",
                "content": usuario
            }
        ])

        try:
            limpo = re.sub(
                r"^```(?:json)?\s*|\s*```$",
                "",
                texto.strip(),
                flags=re.IGNORECASE
            ).strip()

            inicio = limpo.find("{")
            fim = limpo.rfind("}")

            if inicio < 0 or fim < inicio:
                raise ValueError("JSON não encontrado")

            dados = json.loads(
                limpo[inicio:fim + 1]
            )

            lista = dados["questoes"]

            if not isinstance(lista, list) or len(lista) != 1:
                raise ValueError(
                    "Esperada exatamente uma questão"
                )

            questao = Questao.model_validate(
                lista[0]
            )

            normalizada = " ".join(
                questao.enunciado.lower().split()
            )

            anteriores_normalizadas = {
                " ".join(pergunta.lower().split())
                for pergunta in historico
            }

            if normalizada in anteriores_normalizadas:
                raise ValueError(
                    "Questão repetida"
                )

            print(
                f"[QUIZ] Questão {numero + 1} "
                f"gerada | Abordagem: {abordagem}",
                flush=True
            )

            return [questao]

        except (ValueError, TypeError, KeyError) as erro:
            ultimo_erro = erro

            print(
                f"[QUIZ] Tentativa {tentativa}/3: {erro}",
                flush=True
            )

    raise ServicoIAError(
        "Não foi possível gerar uma questão válida."
    ) from ultimo_erro


def corrigir(
    questoes: list[dict],
    respostas: list[int]
):
    if (
        len(respostas) != len(questoes)
        or any(
            type(resposta) != int
            or resposta not in range(4)
            for resposta in respostas
        )
    ):
        raise ValueError("Respostas inválidas")

    detalhes = [
        {
            "enunciado": questao["enunciado"],
            "resposta": resposta,
            "correta": questao["correta"],
            "acertou": resposta == questao["correta"],
            "explicacao": questao["explicacao"],
            "alternativas": questao["alternativas"]
        }
        for questao, resposta in zip(
            questoes, respostas
        )
    ]

    acertos = sum(
        item["acertou"]
        for item in detalhes
    )

    return {
        "acertos": acertos,
        "total": len(questoes),
        "percentual": round(
            acertos * 100 / len(questoes), 1
        ),
        "detalhes": detalhes
    }
