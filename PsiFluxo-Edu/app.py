
"""PsiFluxo Edu: tutor inteligente, exercícios e progresso."""

import os
import secrets
from pathlib import Path

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    session
)

from pydantic import ValidationError
from dotenv import load_dotenv

from educacional.tutor import PedidoExplicacao, explicar
from educacional.exercicios import (
    PedidoQuiz,
    gerar_quiz,
    corrigir
)

from services.ia_service import (
    ConfiguracaoIAError,
    ServicoIAError
)

from database.repository import (
    inicializar,
    salvar,
    progresso
)


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


def create_app(config=None):

    app = Flask(__name__)

    app.json.ensure_ascii = False

    app.config.update(
        SECRET_KEY=(
            os.getenv("SECRET_KEY")
            or secrets.token_hex(32)
        ),
        DATABASE=str(
            BASE_DIR / "database" / "progresso.db"
        ),
        MAX_CONTENT_LENGTH=20 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax"
    )

    if config:
        app.config.update(config)

    inicializar(app.config["DATABASE"])

    # Armazenamento temporário dos questionários.
    # O gabarito permanece no servidor.
    app.quiz_store = {}

    # ==========================================
    # PÁGINA PRINCIPAL
    # ==========================================

    @app.get("/")
    def inicio():
        return render_template("index.html")

    # ==========================================
    # VERIFICAÇÃO DO SERVIÇO
    # ==========================================

    @app.get("/api/saude")
    def saude():
        return jsonify(
            status="ok",
            provedor=os.getenv(
                "AI_PROVIDER",
                "ollama"
            )
        )

    # ==========================================
    # EXPLICAÇÃO COM IA
    # ==========================================

    @app.post("/api/explicar")
    def api_explicar():

        if not request.is_json:
            return jsonify(
                erro="Envie JSON."
            ), 415

        try:
            pedido = PedidoExplicacao.model_validate(
                request.get_json()
            )

            resposta = explicar(pedido)

            return jsonify(
                tema=pedido.tema,
                nivel=pedido.nivel,
                resposta=resposta
            )

        except ValidationError as erro:
            return jsonify(
                erro="Dados inválidos.",
                detalhes=erro.errors(
                    include_url=False,
                    include_context=False
                )
            ), 400

        except ConfiguracaoIAError as erro:
            return jsonify(
                erro=str(erro)
            ), 503

        except ServicoIAError:
            return jsonify(
                erro=(
                    "Serviço de IA indisponível "
                    "ou resposta inválida."
                )
            ), 502

    # ==========================================
    # GERAÇÃO PROGRESSIVA DE QUESTÕES
    # ==========================================

    @app.post("/api/exercicios")
    def api_exercicios():

        if not request.is_json:
            return jsonify(
                erro="Envie JSON."
            ), 415

        try:
            pedido = PedidoQuiz.model_validate(
                request.get_json()
            )

            # Histórico da sessão de estudo.
            historico = session.get(
                "historico_questoes", []
            )

            # Identificação do tema e nível.
            chave_estudo = (
                f"{pedido.tema.strip().lower()}"
                f"|{pedido.nivel}"
            )

            # Reinicia histórico quando o assunto muda.
            if session.get("chave_estudo") != chave_estudo:
                historico = []

            # Gera uma questão considerando o histórico.
            questoes = gerar_quiz(
                pedido,
                historico=historico
            )

            # Atualiza o histórico somente após
            # uma geração bem-sucedida.
            historico.append(
                questoes[0].enunciado
            )

            # Mantém as últimas 12 perguntas.
            session["historico_questoes"] = historico[-12:]
            session["chave_estudo"] = chave_estudo

            # Cria um identificador seguro.
            quiz_id = secrets.token_urlsafe(12)

            # Gabarito armazenado no servidor.
            app.quiz_store[quiz_id] = {
                "tema": pedido.tema,
                "nivel": pedido.nivel,
                "questoes": [
                    questao.model_dump()
                    for questao in questoes
                ]
            }

            # A sessão guarda apenas o identificador.
            session["quiz_id"] = quiz_id

            # Não envia o gabarito ao navegador.
            return jsonify(
                questoes=[
                    {
                        "enunciado": questao.enunciado,
                        "alternativas": questao.alternativas
                    }
                    for questao in questoes
                ]
            )

        except ValidationError as erro:
            return jsonify(
                erro="Dados inválidos.",
                detalhes=erro.errors(
                    include_url=False,
                    include_context=False
                )
            ), 400

        except ConfiguracaoIAError as erro:
            return jsonify(
                erro=str(erro)
            ), 503

        except ServicoIAError:
            return jsonify(
                erro=(
                    "Não foi possível gerar uma questão "
                    "válida. Tente novamente."
                )
            ), 502

    # ==========================================
    # CORREÇÃO DA QUESTÃO
    # ==========================================

    @app.post("/api/corrigir")
    def api_corrigir():

        if not request.is_json:
            return jsonify(
                erro="Envie JSON."
            ), 415

        dados = request.get_json(silent=True)

        if (
            not isinstance(dados, dict)
            or set(dados) != {"respostas"}
            or not isinstance(dados["respostas"], list)
        ):
            return jsonify(
                erro="Respostas inválidas."
            ), 400

        quiz_id = session.get("quiz_id")

        quiz = app.quiz_store.get(quiz_id)

        if not quiz:
            return jsonify(
                erro=(
                    "Gere uma questão antes "
                    "de solicitar a correção."
                )
            ), 409

        try:
            resultado = corrigir(
                quiz["questoes"],
                dados["respostas"]
            )

        except ValueError:
            return jsonify(
                erro="Respostas inválidas."
            ), 400

        # Registra a tentativa no SQLite.
        salvar(
            app.config["DATABASE"],
            quiz["tema"],
            quiz["nivel"],
            resultado["acertos"],
            resultado["total"]
        )

        # Remove o questionário corrigido.
        app.quiz_store.pop(quiz_id, None)
        session.pop("quiz_id", None)

        return jsonify(resultado)

    # ==========================================
    # PROGRESSO DO ESTUDANTE
    # ==========================================

    @app.get("/api/progresso")
    def api_progresso():

        dados = progresso(
            app.config["DATABASE"]
        )

        return jsonify(dados)

    # ==========================================
    # TRATAMENTO DE REQUISIÇÕES GRANDES
    # ==========================================

    @app.errorhandler(413)
    def muito_grande(_):

        return jsonify(
            erro="Requisição muito grande."
        ), 413

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
