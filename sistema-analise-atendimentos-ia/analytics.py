import pandas as pd
from sqlalchemy.orm import Session

from models import Atendimento


def carregar_dados(db: Session) -> pd.DataFrame:
    registros = db.query(Atendimento).all()
    linhas = [
        {
            "id": r.id,
            "cliente": r.cliente,
            "categoria": r.categoria,
            "atendente": r.atendente,
            "data_atendimento": r.data_atendimento,
            "status": r.status,
            "descricao": r.descricao,
            "tempo_atendimento": r.tempo_atendimento,
            "satisfacao": float(r.satisfacao) if r.satisfacao is not None else None,
        }
        for r in registros
    ]
    colunas = [
        "id", "cliente", "categoria", "atendente", "data_atendimento",
        "status", "descricao", "tempo_atendimento", "satisfacao"
    ]
    df = pd.DataFrame(linhas, columns=colunas)
    if not df.empty:
        df["data_atendimento"] = pd.to_datetime(df["data_atendimento"], errors="coerce")
        df["tempo_atendimento"] = pd.to_numeric(df["tempo_atendimento"], errors="coerce")
        df["satisfacao"] = pd.to_numeric(df["satisfacao"], errors="coerce")
    return df


def resumo_geral(db: Session) -> dict:
    df = carregar_dados(db)
    if df.empty:
        return {"total_atendimentos": 0, "mensagem": "Não há atendimentos cadastrados."}
    return {
        "total_atendimentos": int(len(df)),
        "por_status": {str(k): int(v) for k, v in df["status"].value_counts().items()},
        "por_categoria": {str(k): int(v) for k, v in df["categoria"].value_counts().items()},
        "por_atendente": {str(k): int(v) for k, v in df["atendente"].value_counts().items()},
        "tempo_medio_atendimento": round(float(df["tempo_atendimento"].mean()), 2) if df["tempo_atendimento"].notna().any() else None,
        "quantidade_com_tempo_registrado": int(df["tempo_atendimento"].notna().sum()),
        "satisfacao_media": round(float(df["satisfacao"].mean()), 2) if df["satisfacao"].notna().any() else None,
        "quantidade_com_satisfacao": int(df["satisfacao"].notna().sum()),
        "quantidade_sem_satisfacao": int(df["satisfacao"].isna().sum()),
    }


def por_categoria(db: Session) -> dict:
    df = carregar_dados(db)
    return {str(k): int(v) for k, v in df["categoria"].value_counts().items()} if not df.empty else {}


def por_status(db: Session) -> dict:
    df = carregar_dados(db)
    return {str(k): int(v) for k, v in df["status"].value_counts().items()} if not df.empty else {}


def por_atendente(db: Session) -> dict:
    df = carregar_dados(db)
    return {str(k): int(v) for k, v in df["atendente"].value_counts().items()} if not df.empty else {}


def atendente_maior_numero(db: Session) -> dict:
    dados = por_atendente(db)
    if not dados:
        return {"mensagem": "Não há dados para comparar."}
    maior = max(dados.values())
    return {"atendentes_com_maior_volume": [k for k, v in dados.items() if v == maior], "quantidade": maior}


def tempo_medio(db: Session) -> dict:
    df = carregar_dados(db)
    if df.empty or not df["tempo_atendimento"].notna().any():
        return {"tempo_medio": None, "quantidade_com_tempo_registrado": 0}
    return {"tempo_medio": round(float(df["tempo_atendimento"].mean()), 2),
            "quantidade_com_tempo_registrado": int(df["tempo_atendimento"].notna().sum())}


def satisfacao_media(db: Session) -> dict:
    df = carregar_dados(db)
    validos = df["satisfacao"].dropna() if not df.empty else pd.Series(dtype=float)
    return {"satisfacao_media": round(float(validos.mean()), 2) if not validos.empty else None,
            "quantidade_com_satisfacao": int(validos.count()),
            "quantidade_sem_satisfacao": int(len(df) - validos.count()) if not df.empty else 0}


def maiores_avaliacoes(db: Session) -> dict:
    df = carregar_dados(db)
    if df.empty:
        return {"resultados": []}
    validos = df.dropna(subset=["satisfacao"])
    if validos.empty:
        return {"resultados": []}
    maximo = validos["satisfacao"].max()
    return {"nota_maxima": float(maximo), "quantidade": int((validos["satisfacao"] == maximo).sum())}


def menores_avaliacoes(db: Session) -> dict:
    df = carregar_dados(db)
    if df.empty:
        return {"resultados": []}
    validos = df.dropna(subset=["satisfacao"])
    if validos.empty:
        return {"resultados": []}
    minimo = validos["satisfacao"].min()
    return {"nota_minima": float(minimo), "quantidade": int((validos["satisfacao"] == minimo).sum())}


def por_periodo(db: Session, data_inicio, data_fim) -> dict:
    df = carregar_dados(db)
    if df.empty:
        return {"total_atendimentos": 0, "data_inicio": str(data_inicio), "data_fim": str(data_fim)}
    filtrado = df[
        (df["data_atendimento"].dt.date >= data_inicio)
        & (df["data_atendimento"].dt.date <= data_fim)
    ]
    return {"data_inicio": str(data_inicio), "data_fim": str(data_fim),
            "total_atendimentos": int(len(filtrado)),
            "por_status": {str(k): int(v) for k, v in filtrado["status"].value_counts().items()}}


def desempenho_atendentes(db: Session) -> dict:
    df = carregar_dados(db)
    if df.empty:
        return {"resultados": []}
    agrupado = df.groupby("atendente").agg(
        total_atendimentos=("id", "count"),
        tempo_medio=("tempo_atendimento", "mean"),
        satisfacao_media=("satisfacao", "mean"),
    ).reset_index()
    resultados = []
    for _, row in agrupado.iterrows():
        tempo = row["tempo_medio"]
        satisfacao = row["satisfacao_media"]
        resultados.append({
            "atendente": str(row["atendente"]),
            "total_atendimentos": int(row["total_atendimentos"]),
            "tempo_medio": round(float(tempo), 2) if pd.notna(tempo) else None,
            "satisfacao_media": round(float(satisfacao), 2) if pd.notna(satisfacao) else None,
        })
    return {"resultados": resultados}


def categorias_com_maior_demanda(db: Session) -> dict:
    dados = por_categoria(db)
    if not dados:
        return {"categorias_com_maior_demanda": [], "quantidade": 0}
    maior = max(dados.values())
    return {"categorias_com_maior_demanda": [k for k, v in dados.items() if v == maior], "quantidade": maior}


def desempenho_categorias(db: Session) -> dict:
    """Calcula indicadores agregados de atendimento por categoria."""
    df = carregar_dados(db)

    if df.empty:
        return {"resultados": []}

    # Exclui categorias ausentes do agrupamento, pois não representam
    # uma categoria identificada.
    df_validos = df.dropna(subset=["categoria"]).copy()

    if df_validos.empty:
        return {"resultados": []}

    agrupado = df_validos.groupby("categoria").agg(
        total_atendimentos=("id", "count"),
        quantidade_com_tempo_registrado=("tempo_atendimento", "count"),
        tempo_medio=("tempo_atendimento", "mean"),
        quantidade_com_satisfacao=("satisfacao", "count"),
        satisfacao_media=("satisfacao", "mean"),
    ).reset_index()

    resultados = []

    for _, row in agrupado.iterrows():
        tempo = row["tempo_medio"]
        satisfacao = row["satisfacao_media"]

        resultados.append({
            "categoria": str(row["categoria"]),
            "total_atendimentos": int(row["total_atendimentos"]),
            "quantidade_com_tempo_registrado": int(
                row["quantidade_com_tempo_registrado"]
            ),
            "tempo_medio": (
                round(float(tempo), 2) if pd.notna(tempo) else None
            ),
            "quantidade_com_satisfacao": int(
                row["quantidade_com_satisfacao"]
            ),
            "satisfacao_media": (
                round(float(satisfacao), 2)
                if pd.notna(satisfacao)
                else None
            ),
        })

    return {"resultados": resultados}
