# PsiFluxo Edu — Registro de validação e evidências

**Projeto Final SENAI | Revisão: 16/11/2026**

## 1. Contexto

Este documento atualiza o registro anterior, que ainda mencionava Gemini como integração principal, dependências não instaladas e testes não executados. A configuração principal atual é **Ollama local com `llama3.2:3b`**. Os resultados abaixo são baseados nos registros de execução apresentados pelo desenvolvedor no Windows; não representam uma nova execução feita durante esta revisão documental.

## 2. Ambiente informado

- Sistema: Windows, PowerShell, ambiente virtual `.venv` ativo.
- Python: 3.14.6, conforme ambiente informado para o projeto.
- Dependências declaradas em `requirements.txt`: `Flask>=3.1,<4`, `python-dotenv>=1,<2`, `openai>=2,<3`, `pydantic>=2,<3`, `pytest>=9,<10`.
- Provedor principal: `AI_PROVIDER=ollama`.
- Modelo: `OLLAMA_MODEL=llama3.2:3b`.
- Endpoint local: `OLLAMA_BASE_URL=http://127.0.0.1:11434/v1`.

## 3. Resultados apresentados em 16/11/2026

### Instalação e consistência das dependências

Comando:

```powershell
python -m pip install -r requirements.txt
python -m pip check
```

**Resultado informado:** dependências instaladas e `No broken requirements found.`

### Testes automatizados

Comando:

```powershell
python -m pytest -v
```

**Resultado apresentado:** `14 passed in 4.13s`.

Testes aprovados:

1. `test_home`
2. `test_saude`
3. `test_requer_json`
4. `test_tema_curto`
5. `test_nivel_invalido`
6. `test_explicacao`
7. `test_sem_chave`
8. `test_erro_provedor`
9. `test_quiz_e_correcao`
10. `test_quiz_quantidade_invalida`
11. `test_correcao_sem_quiz`
12. `test_quiz_json_ruim`
13. `test_progresso_vazio`
14. `test_quiz_resposta_incompleta`

Os testes usam cliente de teste Flask e, nas operações com IA, `unittest.mock.patch`. Assim, validam o comportamento da aplicação sob respostas simuladas, sem exigir inferência real durante a suíte.

### Integração real

Em etapas anteriores do desenvolvimento, foram apresentados registros de geração e correção de questões com Ollama e respostas HTTP 200, além de consulta ao progresso. Isso é uma evidência distinta dos testes com mocks. **Não foi realizada uma nova chamada ao Ollama na elaboração deste documento**; antes da defesa, recomenda-se repetir `python teste_ollama.py` e uma demonstração completa pela interface.

### Empacotamento

Foi apresentado um ZIP de entrega chamado `PsiFluxo-Edu-Entrega-Final.zip` com **22.900 bytes** e uma listagem contendo 23 arquivos, incluindo `app.py`, `README.md`, `requirements.txt`, `.env.example`, `.gitignore`, pastas de código, testes e documentação. A inspeção da listagem não equivale a reinstalar e executar o projeto a partir do ZIP; esse teste de reinstalação ainda é recomendado.

## 4. O que os testes comprovam — e o que não comprovam

| Verificação | Evidência | Limite |
|---|---|---|
| Rotas Flask | Testes Pytest aprovados | Não comprova disponibilidade contínua em produção |
| Validação de dados | Casos de entrada inválida e quiz | Não comprova precisão factual do texto gerado |
| Correção | Teste de acerto, erro e segunda correção | Depende do gabarito produzido pela IA |
| SQLite | Testes com banco temporário e consulta de progresso | Não há isolamento por usuário |
| Serviço de IA | Registros manuais anteriores com Ollama | Precisa de nova verificação no ambiente de apresentação |
| Dependências | `pip check` sem conflitos | Não substitui teste de execução a partir do ZIP |

## 5. Códigos HTTP relevantes

- `200`: operação concluída.
- `400`: dados inválidos.
- `409`: tentativa de correção sem quiz ativo ou após correção.
- `413`: requisição excedeu o limite configurado.
- `415`: conteúdo enviado não é JSON.
- `502`: falha de comunicação ou saída inválida da IA.
- `503`: configuração de IA ausente ou inválida.

## 6. Limitações conhecidas

- Sem autenticação de estudantes e sem progresso individualizado.
- Quiz ativo guardado em memória; reinício do processo remove o quiz pendente.
- Histórico de perguntas limitado à sessão e a 12 enunciados; verificação textual não impede paráfrases.
- A escolha da abordagem pedagógica usa o tamanho do histórico; após alcançar o limite de 12, a alternância pode ficar estacionada.
- `PedidoQuiz` aceita `quantidade` até 5, mas o gerador atual retorna uma questão por chamada.
- A validação do Pydantic garante estrutura, não correção pedagógica ou factual.
- O endpoint `/api/saude` confirma resposta do Flask e configuração nominal, não disponibilidade real do modelo.
- Não é uma aplicação pronta para exposição pública sem segurança adicional.

## 7. Procedimento reproduzível de validação

Na raiz do projeto, com `.venv` ativo:

```powershell
python -m pip install -r requirements.txt
python -m pip check
python -m pytest -v
ollama list
python teste_ollama.py
python app.py
```

Antes de `teste_ollama.py`, confirmar que o serviço Ollama está em execução e que `.env` contém as variáveis da configuração principal. Acessar `http://127.0.0.1:5000`, gerar uma explicação, responder uma questão e consultar o progresso. Registrar data, resultado e eventuais erros da nova execução.

## 8. Situação da entrega

- **Documentação técnica:** atualizada para a arquitetura atual.
- **Testes automatizados:** 14/14 aprovados no registro apresentado.
- **Conflitos de dependência:** nenhum no registro apresentado.
- **Integração Ollama:** evidência manual anterior; repetir antes da apresentação.
- **Publicação no GitHub:** não confirmada por esta documentação.
- **Prontidão para produção:** não declarada; projeto classificado como MVP local.

**Nota de segurança:** nunca publicar `.env`, chaves de provedores, `.venv` ou bancos de dados de desenvolvimento sem revisão.
