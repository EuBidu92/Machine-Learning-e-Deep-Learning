import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client(tmp_path):
    return create_app({'TESTING':True,'SECRET_KEY':'test-secret','DATABASE':str(tmp_path/'test.db')}).test_client()

def test_home(client): assert client.get('/').status_code==200

def test_saude(client): assert client.get('/api/saude').json['status']=='ok'

def test_requer_json(client): assert client.post('/api/explicar',data='texto').status_code==415

def test_tema_curto(client): assert client.post('/api/explicar',json={'tema':'a'}).status_code==400

def test_nivel_invalido(client): assert client.post('/api/explicar',json={'tema':'Python','nivel':'expert'}).status_code==400

def test_explicacao(client):
    with patch('educacional.tutor.gerar_resposta',return_value='Uma explicação'):
        r=client.post('/api/explicar',json={'tema':'Python','nivel':'iniciante'})
    assert r.status_code==200 and r.json['resposta']=='Uma explicação'

def test_sem_chave(client):
    from services.ia_service import ConfiguracaoIAError
    with patch('educacional.tutor.gerar_resposta',side_effect=ConfiguracaoIAError('GEMINI_API_KEY ausente')):
        assert client.post('/api/explicar',json={'tema':'Python'}).status_code==503

def test_erro_provedor(client):
    from services.ia_service import ServicoIAError
    with patch('educacional.tutor.gerar_resposta',side_effect=ServicoIAError('erro')):
        assert client.post('/api/explicar',json={'tema':'Python'}).status_code==502

def test_quiz_e_correcao(client):
    import json
    questoes={'questoes':[{'enunciado':'Qual alternativa está correta sobre Python?','alternativas':['Uma linguagem','Um navegador','Um sistema','Uma planilha'],'correta':0,'explicacao':'Python é uma linguagem de programação.'}]}
    with patch('educacional.exercicios.gerar_resposta',return_value=json.dumps(questoes)):
        r=client.post('/api/exercicios',json={'tema':'Python','quantidade':1})
    assert r.status_code==200
    assert 'correta' not in r.json['questoes'][0]
    assert client.post('/api/corrigir',json={'respostas':[5]}).status_code==400
    r=client.post('/api/corrigir',json={'respostas':[0]})
    assert r.status_code==200 and r.json['acertos']==1
    assert client.post('/api/corrigir',json={'respostas':[0]}).status_code==409
    assert client.get('/api/progresso').json['percentual']==100

def test_quiz_quantidade_invalida(client):
    assert client.post('/api/exercicios',json={'tema':'Python','quantidade':7}).status_code==400

def test_correcao_sem_quiz(client):
    assert client.post('/api/corrigir',json={'respostas':[0]}).status_code==409

def test_quiz_json_ruim(client):
    with patch('educacional.exercicios.gerar_resposta',return_value='texto não JSON'):
        assert client.post('/api/exercicios',json={'tema':'Python','quantidade':1}).status_code==502

def test_progresso_vazio(client): assert client.get('/api/progresso').json['tentativas']==0

def test_quiz_resposta_incompleta(client):
    import json
    questoes={'questoes':[{'enunciado':'Qual alternativa está correta sobre Python?','alternativas':['Uma linguagem','Um navegador','Um sistema','Uma planilha'],'correta':0,'explicacao':'Python é uma linguagem de programação.'}]}
    with patch('educacional.exercicios.gerar_resposta',return_value=json.dumps(questoes)):
        client.post('/api/exercicios',json={'tema':'Python','quantidade':1})
    assert client.post('/api/corrigir',json={'respostas':[]}).status_code==400
    assert client.post('/api/corrigir',json={'respostas':[1]}).json['acertos']==0
