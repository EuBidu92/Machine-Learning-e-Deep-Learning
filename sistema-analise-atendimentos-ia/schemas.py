from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

StatusAtendimento = Literal["Concluído", "Em andamento", "Pendente"]


class AtendimentoCreate(BaseModel):
    cliente: str = Field(..., min_length=1, max_length=100)
    categoria: str = Field(..., min_length=1, max_length=50)
    atendente: str = Field(..., min_length=1, max_length=100)
    data_atendimento: date
    status: StatusAtendimento
    descricao: str | None = Field(default=None, max_length=5000)
    tempo_atendimento: int | None = Field(default=None, ge=0)
    satisfacao: float | None = Field(default=None, ge=0, le=5)

    @field_validator("cliente", "categoria", "atendente")
    @classmethod
    def nao_vazio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo não pode ficar vazio.")
        return value


class AtendimentoUpdate(BaseModel):
    cliente: str | None = Field(default=None, min_length=1, max_length=100)
    categoria: str | None = Field(default=None, min_length=1, max_length=50)
    atendente: str | None = Field(default=None, min_length=1, max_length=100)
    data_atendimento: date | None = None
    status: StatusAtendimento | None = None
    descricao: str | None = Field(default=None, max_length=5000)
    tempo_atendimento: int | None = Field(default=None, ge=0)
    satisfacao: float | None = Field(default=None, ge=0, le=5)

    @field_validator("cliente", "categoria", "atendente")
    @classmethod
    def nao_vazio_quando_informado(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("O campo não pode ficar vazio.")
        return value


class AtendimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente: str
    categoria: str
    atendente: str
    data_atendimento: date
    status: str
    descricao: str | None = None
    tempo_atendimento: int | None = None
    satisfacao: float | None = None
