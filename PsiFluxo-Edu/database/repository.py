"""Persistência SQLite sem dependências extras."""
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

def conectar(caminho):
    Path(caminho).parent.mkdir(parents=True,exist_ok=True)
    conn=sqlite3.connect(caminho)
    conn.row_factory=sqlite3.Row
    return conn

def inicializar(caminho):
    with conectar(caminho) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS resultados (id INTEGER PRIMARY KEY, criado_em TEXT NOT NULL, tema TEXT NOT NULL, nivel TEXT NOT NULL, acertos INTEGER NOT NULL, total INTEGER NOT NULL)')

def salvar(caminho,tema,nivel,acertos,total):
    with conectar(caminho) as conn:
        conn.execute('INSERT INTO resultados (criado_em,tema,nivel,acertos,total) VALUES (?,?,?,?,?)',(datetime.now(timezone.utc).isoformat(),tema,nivel,acertos,total))

def progresso(caminho):
    with conectar(caminho) as conn:
        resumo=conn.execute('SELECT COUNT(*) tentativas, COALESCE(SUM(acertos),0) acertos, COALESCE(SUM(total),0) questoes FROM resultados').fetchone()
        historico=conn.execute('SELECT criado_em,tema,nivel,acertos,total FROM resultados ORDER BY id DESC LIMIT 20').fetchall()
        return {'tentativas':resumo['tentativas'],'acertos':resumo['acertos'],'questoes':resumo['questoes'],'percentual':round(100*resumo['acertos']/resumo['questoes'],1) if resumo['questoes'] else 0,'historico':[dict(r) for r in historico]}
