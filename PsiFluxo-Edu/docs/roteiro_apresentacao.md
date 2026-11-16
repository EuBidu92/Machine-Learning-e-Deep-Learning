# PsiFluxo Edu — Roteiro de apresentação e demonstração individual

**Projeto Final SENAI | Proposta 1 | Revisão: 16/11/2026**

## 1. Objetivo e tempo

Apresentação individual de aproximadamente **12 minutos**, com 12 slides. Reservar cerca de 9 minutos para introdução, explicações técnicas e conclusão, incluindo **3 minutos de demonstração prática**. O texto sugerido está em `docs/falas_por_slide.md`.

## 2. Preparação antes de apresentar

1. Abrir PowerShell na raiz do projeto e ativar o ambiente virtual, se necessário.
2. Confirmar instalação do Ollama e do modelo `llama3.2:3b` (`ollama list`).
3. Confirmar no `.env`: `AI_PROVIDER=ollama`, `OLLAMA_MODEL=llama3.2:3b` e `OLLAMA_BASE_URL=http://127.0.0.1:11434/v1`.
4. Garantir que o serviço Ollama esteja em execução; se necessário, iniciar `ollama serve` em terminal separado.
5. Executar `python -m pytest -v` e conferir o resultado.
6. Executar `python app.py` e abrir `http://127.0.0.1:5000`.
7. Testar uma explicação real **antes** da apresentação. A rota `/api/saude` confirma Flask, mas não substitui uma inferência real.
8. Abrir o PowerPoint, desativar notificações e ajustar a escala do navegador.
9. Não projetar o conteúdo do `.env` nem chaves de provedores externos.

## 3. Sequência sugerida de slides

| Slide | Tema | Tempo-alvo |
|---|---|---|
| 1 | Apresentação | 40 s |
| 2 | Problema | 50 s |
| 3 | Funcionalidades | 1 min |
| 4 | Tecnologias | 1 min |
| 5 | Arquitetura | 1 min |
| 6 | Integração Ollama | 1 min |
| 7 | Validação e correção | 1 min 10 s |
| 8 | SQLite | 30 s |
| 9 | Testes | 50 s |
| 10 | Demonstração | 3 min |
| 11 | Limitações | 30 s |
| 12 | Conclusão | 20 s |

**Nota:** a soma dos tempos é aproximadamente 11 min 40 s; reserve o restante para transições.

## 4. Demonstração passo a passo

1. Na interface, informar tema **Python** e nível **iniciante**.
2. Clicar em **Explicar conteúdo** e comentar que o prompt é montado em `educacional/tutor.py`.
3. Clicar em **Gerar uma questão**; mostrar quatro alternativas e explicar que o gabarito não é enviado ao navegador.
4. Selecionar uma alternativa e clicar em **Corrigir resposta**; comentar que `corrigir()` compara índices em Python.
5. Mostrar a justificativa e a pontuação. Se houver tempo, clicar em **Próxima questão**.
6. Clicar em **Meu progresso**; explicar que os resultados são persistidos no SQLite e agregados para a aplicação local.

**Plano de contingência:** se a inferência estiver indisponível, mostrar os testes automatizados e a estrutura do código, informando claramente que isso **não** comprova a geração real naquele momento. Não inventar resultados de uma chamada que falhou.

## 5. Perguntas prováveis da banca

**Por que Flask em vez de FastAPI?** O escopo é pequeno, Flask é simples e suficiente para uma API local; a aplicação já utiliza Pydantic para validação.

**Onde está a IA?** Nas explicações e na geração de questões. A pontuação e o armazenamento são feitos por código Python.

**Qual modelo foi utilizado?** Na configuração principal, `llama3.2:3b` via Ollama local. O serviço contempla outros provedores opcionais.

**A biblioteca `openai` significa usar GPT?** Não. É utilizada como cliente de protocolo compatível para comunicar-se com o Ollama.

**O que o Pydantic valida?** Tipo, tamanho, campos exigidos, quantidade e estrutura das alternativas. Não garante a veracidade do conteúdo.

**Como a aplicação evita repetição?** Envia até 12 enunciados anteriores à IA e compara enunciados normalizados; não elimina paráfrases semanticamente semelhantes.

**Por que a correção não é feita pela IA?** Para evitar uma nova inferência e tornar o cálculo determinístico; o gabarito gerado ainda pode conter erro factual.

**Como o gabarito é protegido?** Fica no dicionário `app.quiz_store` do servidor e é associado a um identificador na sessão. O navegador só recebe enunciado e alternativas antes da correção.

**Por que SQLite?** Persiste resultados sem exigir servidor de banco separado, adequado ao MVP local.

**Os testes usam IA real?** Os testes de API usam mocks para cenários controlados. A comunicação com Ollama é verificada separadamente.

**Quais limitações?** Ausência de autenticação e progresso individual, quizzes ativos apenas na memória, possibilidade de erros da LLM e histórico com verificação textual limitada.

**Por que não LangGraph ou RAG?** A proposta escolhida é uma aplicação educacional com LLM e prompts, sem necessidade de fluxo multiagente ou recuperação documental.

## 6. Arquivos úteis para a defesa

- `app.py`: rotas, sessões e fluxo principal.
- `educacional/tutor.py`: prompt de explicação.
- `educacional/exercicios.py`: geração, validação e correção.
- `services/ia_service.py`: configuração e chamadas ao Ollama.
- `database/repository.py`: SQLite.
- `testes/test_api.py`: testes e mocks.
- `docs/arquitetura.md`: justificativas e diagrama textual.
- `docs/validacao.md`: evidências e limitações da validação.

## 7. Checklist final

- [ ] Ambiente virtual e dependências funcionando.
- [ ] Modelo Ollama instalado e serviço ativo.
- [ ] Explicação real testada antes da apresentação.
- [ ] Página e progresso carregando.
- [ ] PowerPoint e navegador abertos.
- [ ] Nenhuma chave de API visível.
- [ ] Capacidade de diferenciar geração por IA, correção Python e persistência SQLite.
