import logging
import os
from datetime import date

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ai_service import gerar_analise_ia
from analytics import (
    atendente_maior_numero,
    categorias_com_maior_demanda,
    desempenho_atendentes,
    maiores_avaliacoes,
    menores_avaliacoes,
    por_atendente,
    por_categoria,
    por_periodo,
    por_status,
    resumo_geral,
    satisfacao_media,
    tempo_medio,
)
from database import get_db
from models import Atendimento
from schemas import AtendimentoCreate, AtendimentoResponse, AtendimentoUpdate

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sistema de Análise de Atendimentos",
    description=(
        "API REST com MySQL, SQLAlchemy, Pandas e integração de IA "
        "por LangChain + Groq."
    ),
    version="2.0.0",
)


class PerguntaIA(BaseModel):
    pergunta: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Pergunta sobre os indicadores agregados dos atendimentos.",
    )


@app.get("/", tags=["Início"])
def inicio():
    return {
        "mensagem": "API do Sistema de Análise de Atendimentos",
        "documentacao": "/docs",
        "endpoint_ia": "POST /ia/analisar",
    }


@app.get("/health", tags=["Saúde"])
def health():
    return {"status": "online"}


@app.get("/atendimentos", response_model=list[AtendimentoResponse], tags=["Atendimentos"])
def listar_atendimentos(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    try:
        return db.query(Atendimento).order_by(Atendimento.id).offset(skip).limit(limit).all()
    except SQLAlchemyError:
        logger.exception("Erro ao listar atendimentos")
        raise HTTPException(status_code=503, detail="Não foi possível consultar o banco de dados.")


@app.get("/atendimentos/{atendimento_id}", response_model=AtendimentoResponse, tags=["Atendimentos"])
def obter_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if atendimento is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")
    return atendimento


@app.post("/atendimentos", response_model=AtendimentoResponse, status_code=status.HTTP_201_CREATED, tags=["Atendimentos"])
def criar_atendimento(dados: AtendimentoCreate, db: Session = Depends(get_db)):
    atendimento = Atendimento(**dados.model_dump())
    try:
        db.add(atendimento)
        db.commit()
        db.refresh(atendimento)
        return atendimento
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao criar atendimento")
        raise HTTPException(status_code=503, detail="Não foi possível salvar o atendimento.")


@app.put("/atendimentos/{atendimento_id}", response_model=AtendimentoResponse, tags=["Atendimentos"])
def atualizar_atendimento(atendimento_id: int, dados: AtendimentoUpdate, db: Session = Depends(get_db)):
    atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if atendimento is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(atendimento, campo, valor)

    try:
        db.commit()
        db.refresh(atendimento)
        return atendimento
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao atualizar atendimento")
        raise HTTPException(status_code=503, detail="Não foi possível atualizar o atendimento.")


@app.delete("/atendimentos/{atendimento_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Atendimentos"])
def excluir_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if atendimento is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")
    try:
        db.delete(atendimento)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro ao excluir atendimento")
        raise HTTPException(status_code=503, detail="Não foi possível excluir o atendimento.")


@app.get("/analises/resumo", tags=["Análises"])
def api_resumo(db: Session = Depends(get_db)):
    return resumo_geral(db)


@app.get("/analises/categorias", tags=["Análises"])
def api_categorias(db: Session = Depends(get_db)):
    return por_categoria(db)


@app.get("/analises/status", tags=["Análises"])
def api_status(db: Session = Depends(get_db)):
    return por_status(db)


@app.get("/analises/atendentes", tags=["Análises"])
def api_atendentes(db: Session = Depends(get_db)):
    return por_atendente(db)


@app.get("/analises/atendente-destaque", tags=["Análises"])
def api_atendente_destaque(db: Session = Depends(get_db)):
    return atendente_maior_numero(db)


@app.get("/analises/tempo-medio", tags=["Análises"])
def api_tempo_medio(db: Session = Depends(get_db)):
    return tempo_medio(db)


@app.get("/analises/satisfacao", tags=["Análises"])
def api_satisfacao(db: Session = Depends(get_db)):
    return satisfacao_media(db)


@app.get("/analises/avaliacoes/maiores", tags=["Análises"])
def api_maiores_avaliacoes(db: Session = Depends(get_db)):
    return maiores_avaliacoes(db)


@app.get("/analises/avaliacoes/menores", tags=["Análises"])
def api_menores_avaliacoes(db: Session = Depends(get_db)):
    return menores_avaliacoes(db)


@app.get("/analises/periodo", tags=["Análises"])
def api_periodo(
    data_inicio: date,
    data_fim: date,
    db: Session = Depends(get_db),
):
    if data_inicio > data_fim:
        raise HTTPException(status_code=422, detail="data_inicio deve ser anterior ou igual a data_fim.")
    return por_periodo(db, data_inicio, data_fim)


@app.get("/analises/desempenho-atendentes", tags=["Análises"])
def api_desempenho_atendentes(db: Session = Depends(get_db)):
    return desempenho_atendentes(db)


@app.get("/analises/demanda-categorias", tags=["Análises"])
def api_demanda_categorias(db: Session = Depends(get_db)):
    return categorias_com_maior_demanda(db)


@app.post("/ia/analisar", tags=["Inteligência Artificial"])
def analisar_com_ia(dados: PerguntaIA, db: Session = Depends(get_db)):
    if not os.getenv("GROQ_API_KEY", "").strip():
        raise HTTPException(
            status_code=503,
            detail="A chave GROQ_API_KEY não está configurada no arquivo .env.",
        )
    try:
        return gerar_analise_ia(dados.pergunta, db)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except RuntimeError as erro:
        logger.warning("Configuração da IA incompleta: %s", erro)
        raise HTTPException(status_code=503, detail="Serviço de IA não configurado corretamente.")
    except Exception:
        # Não devolve detalhes internos nem credenciais ao cliente.
        logger.exception("Falha ao executar análise de IA")
        raise HTTPException(
            status_code=502,
            detail="Não foi possível concluir a análise de IA. Consulte o terminal do servidor.",
        )
