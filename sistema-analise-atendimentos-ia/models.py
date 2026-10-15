from sqlalchemy import Column, Date, Integer, Numeric, String, Text

from database import Base


class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    atendente = Column(String(100), nullable=False)
    data_atendimento = Column(Date, nullable=False)
    status = Column(String(30), nullable=False)
    descricao = Column(Text, nullable=True)
    tempo_atendimento = Column(Integer, nullable=True)
    satisfacao = Column(Numeric(2, 1), nullable=True)
