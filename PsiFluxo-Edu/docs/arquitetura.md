# PsiFluxo Edu — Arquitetura técnica

**Projeto Final SENAI | Proposta 1 — Aplicação Educacional Inteligente**  
**Revisão:** 16/11/2026 | **Escopo:** protótipo de demonstração local (MVP)

## 1. Visão geral

O PsiFluxo Edu é uma aplicação web que utiliza uma LLM para explicar temas de estudo e gerar questões de múltipla escolha. A aplicação valida as entradas e a estrutura das questões, corrige respostas por regras Python e persiste os resultados em SQLite. A configuração principal é **Ollama local + `llama3.2:3b`**. O serviço de IA também contém integrações configuráveis para Gemini, Groq, OpenRouter e xAI; elas não são necessárias para a demonstração local com Ollama.

```text
Navegador (templates/index.html + static/app.js + static/style.css)
       │ HTTP / JSON
       ▼
Flask (app.py) ── validação Pydantic
       │
       ├── educacional/tutor.py ─────────────┐
       ├── educacional/exercicios.py ────────┤
       │                                     ▼
       │                           services/ia_service.py
       │                                     │
       │                           Ollama / Llama 3.2 3B
       │
       └── database/repository.py ── SQLite (resultados)
```

## 2. Responsabilidade dos arquivos

| Caminho | Responsabilidade |
|---|---|
| `app.py` | Fábrica `create_app`, rotas, sessão, quiz temporário, tratamento de erros e configuração Flask |
| `educacional/tutor.py` | Modelo `PedidoExplicacao` e prompt de explicação |
| `educacional/exercicios.py` | Modelos `PedidoQuiz` e `Questao`, prompt de geração, validação, histórico e correção |
| `services/ia_service.py` | Seleção do provedor e comunicação com a LLM; esquema de JSON para questões no Ollama |
| `services/groq_service.py` | Integração auxiliar/legada específica de Groq, não necessária ao fluxo principal |
| `database/repository.py` | Inicialização, inserção e consulta de resultados SQLite |
| `prompts/explicacao.py` | Função auxiliar de construção de mensagens; o tutor atual constrói seu próprio prompt |
| `templates/index.html` | Estrutura da interface |
| `static/app.js` | Chamadas `fetch`, estados da questão, correção e progresso |
| `static/style.css` | Estilos e adaptação para telas menores |
| `testes/test_api.py` | Testes automatizados com cliente Flask, banco temporário e mocks da IA |

## 3. Rotas HTTP

| Método | Endpoint | Resultado |
|---|---|---|
| GET | `/` | Página principal |
| GET | `/api/saude` | Estado básico do Flask e nome do provedor configurado; **não** testa inferência real |
| POST | `/api/explicar` | Valida tema/nível, solicita explicação e devolve JSON |
| POST | `/api/exercicios` | Gera **uma questão por chamada**, valida e envia enunciado/alternativas sem gabarito |
| POST | `/api/corrigir` | Compara resposta ao gabarito no servidor, registra nota e devolve feedback |
| GET | `/api/progresso` | Totais agregados e até 20 registros recentes |

Exemplos de entrada:

```json
{"tema":"Python","nivel":"iniciante"}
```

Para `/api/exercicios`, acrescente `"quantidade":1`. Para `/api/corrigir`, envie `{"respostas":[0]}` (índices válidos: 0 a 3).

## 4. Fluxo de explicação

1. O JavaScript envia o tema e o nível para `/api/explicar`.
2. `PedidoExplicacao.model_validate()` verifica os campos.
3. `educacional/tutor.py` monta mensagens com papéis `system` e `user`.
4. `services/ia_service.py` lê `AI_PROVIDER`, seleciona modelo e endpoint e envia as mensagens.
5. O Flask retorna a explicação; o JavaScript insere o texto com `textContent`.

## 5. Fluxo de exercícios e correção

1. `/api/exercicios` valida `PedidoQuiz` e lê o histórico da sessão.
2. Ao mudar tema ou nível, o histórico é reiniciado.
3. `gerar_quiz()` escolhe uma abordagem pedagógica, inclui até 12 enunciados anteriores no prompt e solicita exatamente uma questão.
4. Para Ollama, o serviço de IA configura um esquema de saída JSON. O módulo de exercícios interpreta o JSON e valida `Questao` (enunciado, quatro alternativas distintas, índice correto e explicação).
5. Se o conteúdo for inválido, o gerador pode tentar novamente até três vezes. Falhas de comunicação não são necessariamente recuperadas por esse mecanismo.
6. O servidor guarda o gabarito em `app.quiz_store`, associado a um `quiz_id` gerado por `secrets.token_urlsafe`; a sessão guarda o identificador.
7. O navegador recebe **somente enunciado e alternativas**.
8. `/api/corrigir` recupera o questionário, valida a resposta, compara índices em Python, grava resultado no SQLite, remove o quiz da memória e retorna o feedback.
9. `/api/progresso` lê os registros persistidos.

**Observação:** `PedidoQuiz` permite `quantidade` entre 1 e 5, mas o fluxo atual de `gerar_quiz()` sempre produz **uma questão por chamada**. A interface usa `quantidade: 1`.

## 6. Decisões técnicas e justificativas

- **Flask:** API pequena e simples, adequada ao MVP; `create_app()` permite configuração independente para testes.
- **Ollama + Llama 3.2 3B:** execução local após download do modelo, sem chave externa obrigatória; depende de recursos e desempenho do computador.
- **Biblioteca `openai`:** cliente compatível com a API exposta pelo Ollama; **não significa** que a inferência utilize modelos OpenAI.
- **Pydantic:** contratos de entrada e de saída, rejeição de campos extras e validação estrutural de questões.
- **Prompts com papéis:** separação entre orientações da aplicação e pedido do aluno; não elimina por completo prompt injection.
- **Correção determinística:** pontuação reproduzível sem segunda chamada à LLM; a exatidão do gabarito depende do conteúdo gerado.
- **SQLite:** banco local sem servidor separado, com persistência de tentativas.
- **Sessão + dicionário em memória:** solução simples para quiz ativo; perde quizzes ao reiniciar o processo e não atende requisitos de produção distribuída.
- **Pytest com mocks:** testes rápidos e repetíveis sem precisar executar inferência em cada teste.

## 7. Controles e limites

- `SECRET_KEY` assina a sessão; se não for configurada, o programa gera uma chave ao iniciar, invalidando sessões em reinícios.
- Cookies de sessão usam `HttpOnly` e `SameSite=Lax`; o corpo de requisição tem limite de 20 KB.
- Gabarito não é enviado ao navegador antes da correção.
- A consulta ao progresso é **global**, não por estudante; não há autenticação.
- Histórico de perguntas na sessão limitado a 12 enunciados; comparação textual simples não detecta toda repetição semântica.
- A escolha de abordagem usa `len(historico) % len(ABORDAGENS)`; após o histórico atingir o limite, a abordagem pode deixar de alternar. Melhoria: contador separado.
- A validação JSON/Pydantic verifica formato e restrições, **não a verdade factual** da questão.
- O sistema não possui RAG, LangGraph, MCP ou treinamento supervisionado próprio.
- O Flask executa em `127.0.0.1:5000` com `debug=False` no modo local previsto pelo código.

## 8. Execução e validação

```powershell
python -m pip install -r requirements.txt
ollama pull llama3.2:3b
Copy-Item .env.example .env
# Confira AI_PROVIDER=ollama, OLLAMA_MODEL=llama3.2:3b e OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
python -m pytest -v
python -m pip check
python teste_ollama.py
python app.py
```

Acesse `http://127.0.0.1:5000`. O Ollama deve estar em execução. A evidência de testes e suas ressalvas estão em `docs/validacao.md`.
