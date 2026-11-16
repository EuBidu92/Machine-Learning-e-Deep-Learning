# PsiFluxo Edu — Assistente Educacional Inteligente

**Projeto Final SENAI — Proposta 1: Aplicação Educacional Inteligente**

## 1. Apresentação

O PsiFluxo Edu é uma aplicação web educacional que utiliza Inteligência Artificial para explicar conteúdos, gerar questões de múltipla escolha, corrigir respostas e acompanhar o desempenho do estudante.

O projeto foi desenvolvido em Python, com Flask, Pydantic, SQLite e integração com modelos de linguagem (LLMs).

A configuração principal utiliza o Ollama com o modelo Llama 3.2 3B, executado localmente.

## 2. Objetivo

Desenvolver um assistente educacional inteligente capaz de apoiar a aprendizagem por meio de explicações adaptadas ao nível do estudante e exercícios gerados dinamicamente.

## 3. Funcionalidades

- Explicações educacionais nos níveis iniciante, intermediário e avançado.
- Geração automática de questões com Inteligência Artificial.
- Apresentação de uma questão por vez.
- Quatro alternativas por questão.
- Correção automática e determinística em Python.
- Feedback explicativo após a resposta.
- Histórico das questões anteriores durante a sessão.
- Alternância entre abordagens pedagógicas para reduzir repetições.
- Registro de desempenho em banco de dados SQLite.
- Consulta ao progresso do estudante.
- Interface web com HTML, CSS e JavaScript.

## 4. Tecnologias

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Flask | Backend e API HTTP |
| Ollama | Execução local da IA |
| Llama 3.2 3B | Modelo de linguagem |
| Pydantic | Validação de dados |
| SQLite | Armazenamento do progresso |
| HTML, CSS e JavaScript | Interface web |
| Pytest | Testes automatizados |
| python-dotenv | Configuração por variáveis de ambiente |

## 5. Arquitetura

O navegador envia solicitações para a API Flask.

O backend valida as entradas utilizando Pydantic e encaminha as solicitações aos módulos educacionais.

Os módulos utilizam o serviço de IA para gerar explicações e questões.

As questões geradas são validadas antes de serem apresentadas ao estudante.

O gabarito permanece armazenado no servidor até a correção.

A correção é realizada por código Python, sem depender de uma nova interpretação da LLM.

O resultado é registrado no SQLite.

**Fluxo:** Navegador → Flask → Pydantic → Módulo educacional → Serviço de IA → Ollama → Resposta.

## 6. Instalação no Windows

### Pré-requisitos

- Python 3.14 ou versão compatível com as dependências.
- Ollama instalado.
- Modelo `llama3.2:3b` disponível.

### Criar ambiente virtual

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Instalar dependências

```powershell
python -m pip install -r requirements.txt
```

### Instalar o modelo de IA

```powershell
ollama pull llama3.2:3b
```

### Configurar ambiente

```powershell
Copy-Item .env.example .env
notepad .env
```

Configuração principal:

```env
AI_PROVIDER=ollama
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
```

O arquivo `.env` deve permanecer privado.

### Executar

Certifique-se de que o Ollama esteja em execução.

```powershell
python app.py
```

Acesse:

http://127.0.0.1:5000

## 7. Endpoints da API

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/` | Interface principal |
| GET | `/api/saude` | Verificação do serviço |
| POST | `/api/explicar` | Geração de explicações |
| POST | `/api/exercicios` | Geração de questões |
| POST | `/api/corrigir` | Correção das respostas |
| GET | `/api/progresso` | Consulta ao desempenho |

### Exemplo: gerar explicação

```json
{
  "tema": "Inteligência Artificial",
  "nivel": "iniciante"
}
```

### Exemplo: gerar questão

```json
{
  "tema": "Inteligência Artificial",
  "nivel": "iniciante",
  "quantidade": 1
}
```

### Exemplo: corrigir

```json
{
  "respostas": [2]
}
```

## 8. Geração progressiva de questões

O sistema mantém um histórico limitado das perguntas anteriores na sessão do navegador.

Esse histórico é enviado à IA para orientar a geração de novas questões, explorando abordagens como conceitos fundamentais, aplicações práticas, comparações e situações-problema.

O mecanismo reduz a repetição de perguntas, mas não garante diversidade semântica absoluta.

## 9. Testes

Execute:

```powershell
python -m pytest -v
python -m pip check
```

**Resultado da validação realizada em 16/11/2026:**

- 14 testes automatizados aprovados.
- Nenhum conflito de dependências identificado.
- Geração e correção de questões testadas manualmente com Ollama.
- Consulta ao progresso retornando HTTP 200.

Os testes automatizados utilizam simulações em partes da integração; a comunicação real com a IA foi verificada separadamente.

## 10. Segurança e limitações

O PsiFluxo Edu é um protótipo educacional desenvolvido para demonstração local.

Limitações conhecidas:

- Não possui autenticação de usuários.
- Não separa o progresso por estudante.
- Os questionários ativos ficam armazenados temporariamente na memória do servidor.
- O histórico de questões é limitado à sessão.
- A qualidade factual e pedagógica das respostas depende do modelo de IA.
- O sistema não deve ser publicado diretamente na internet sem controles adicionais de segurança.

## 11. Demonstração

1. Iniciar o Ollama e a aplicação Flask.
2. Abrir a interface web.
3. Solicitar uma explicação sobre um tema.
4. Gerar uma questão.
5. Selecionar uma alternativa.
6. Visualizar a correção e a explicação.
7. Avançar para outra questão.
8. Consultar o progresso registrado.

## 12. Conclusão

O PsiFluxo Edu demonstra a integração entre Inteligência Artificial generativa, desenvolvimento web, validação de dados e persistência de informações.

A aplicação permite que o estudante interaja com um tutor inteligente, pratique conhecimentos por meio de questões dinâmicas e acompanhe seu desempenho.

O projeto constitui uma prova de conceito funcional para aplicações educacionais apoiadas por modelos de linguagem.# PsiFluxo Edu — Assistente Educacional Inteligente

**Projeto Final SENAI — Proposta 1: Aplicação Educacional Inteligente**

## 1. Apresentação

O PsiFluxo Edu é uma aplicação web educacional que utiliza Inteligência Artificial para explicar conteúdos, gerar questões de múltipla escolha, corrigir respostas e acompanhar o desempenho do estudante.

O projeto foi desenvolvido em Python, com Flask, Pydantic, SQLite e integração com modelos de linguagem (LLMs).

A configuração principal utiliza o Ollama com o modelo Llama 3.2 3B, executado localmente.

## 2. Objetivo

Desenvolver um assistente educacional inteligente capaz de apoiar a aprendizagem por meio de explicações adaptadas ao nível do estudante e exercícios gerados dinamicamente.

## 3. Funcionalidades

- Explicações educacionais nos níveis iniciante, intermediário e avançado.
- Geração automática de questões com Inteligência Artificial.
- Apresentação de uma questão por vez.
- Quatro alternativas por questão.
- Correção automática e determinística em Python.
- Feedback explicativo após a resposta.
- Histórico das questões anteriores durante a sessão.
- Alternância entre abordagens pedagógicas para reduzir repetições.
- Registro de desempenho em banco de dados SQLite.
- Consulta ao progresso do estudante.
- Interface web com HTML, CSS e JavaScript.

## 4. Tecnologias

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Flask | Backend e API HTTP |
| Ollama | Execução local da IA |
| Llama 3.2 3B | Modelo de linguagem |
| Pydantic | Validação de dados |
| SQLite | Armazenamento do progresso |
| HTML, CSS e JavaScript | Interface web |
| Pytest | Testes automatizados |
| python-dotenv | Configuração por variáveis de ambiente |

## 5. Arquitetura

O navegador envia solicitações para a API Flask.

O backend valida as entradas utilizando Pydantic e encaminha as solicitações aos módulos educacionais.

Os módulos utilizam o serviço de IA para gerar explicações e questões.

As questões geradas são validadas antes de serem apresentadas ao estudante.

O gabarito permanece armazenado no servidor até a correção.

A correção é realizada por código Python, sem depender de uma nova interpretação da LLM.

O resultado é registrado no SQLite.

**Fluxo:** Navegador → Flask → Pydantic → Módulo educacional → Serviço de IA → Ollama → Resposta.

## 6. Instalação no Windows

### Pré-requisitos

- Python 3.14 ou versão compatível com as dependências.
- Ollama instalado.
- Modelo `llama3.2:3b` disponível.

### Criar ambiente virtual

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Instalar dependências

```powershell
python -m pip install -r requirements.txt
```

### Instalar o modelo de IA

```powershell
ollama pull llama3.2:3b
```

### Configurar ambiente

```powershell
Copy-Item .env.example .env
notepad .env
```

Configuração principal:

```env
AI_PROVIDER=ollama
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
```

O arquivo `.env` deve permanecer privado.

### Executar

Certifique-se de que o Ollama esteja em execução.

```powershell
python app.py
```

Acesse:

http://127.0.0.1:5000

## 7. Endpoints da API

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/` | Interface principal |
| GET | `/api/saude` | Verificação do serviço |
| POST | `/api/explicar` | Geração de explicações |
| POST | `/api/exercicios` | Geração de questões |
| POST | `/api/corrigir` | Correção das respostas |
| GET | `/api/progresso` | Consulta ao desempenho |

### Exemplo: gerar explicação

```json
{
  "tema": "Inteligência Artificial",
  "nivel": "iniciante"
}
```

### Exemplo: gerar questão

```json
{
  "tema": "Inteligência Artificial",
  "nivel": "iniciante",
  "quantidade": 1
}
```

### Exemplo: corrigir

```json
{
  "respostas": [2]
}
```

## 8. Geração progressiva de questões

O sistema mantém um histórico limitado das perguntas anteriores na sessão do navegador.

Esse histórico é enviado à IA para orientar a geração de novas questões, explorando abordagens como conceitos fundamentais, aplicações práticas, comparações e situações-problema.

O mecanismo reduz a repetição de perguntas, mas não garante diversidade semântica absoluta.

## 9. Testes

Execute:

```powershell
python -m pytest -v
python -m pip check
```

**Resultado da validação realizada em 16/11/2026:**

- 14 testes automatizados aprovados.
- Nenhum conflito de dependências identificado.
- Geração e correção de questões testadas manualmente com Ollama.
- Consulta ao progresso retornando HTTP 200.

Os testes automatizados utilizam simulações em partes da integração; a comunicação real com a IA foi verificada separadamente.

## 10. Segurança e limitações

O PsiFluxo Edu é um protótipo educacional desenvolvido para demonstração local.

Limitações conhecidas:

- Não possui autenticação de usuários.
- Não separa o progresso por estudante.
- Os questionários ativos ficam armazenados temporariamente na memória do servidor.
- O histórico de questões é limitado à sessão.
- A qualidade factual e pedagógica das respostas depende do modelo de IA.
- O sistema não deve ser publicado diretamente na internet sem controles adicionais de segurança.

## 11. Demonstração

1. Iniciar o Ollama e a aplicação Flask.
2. Abrir a interface web.
3. Solicitar uma explicação sobre um tema.
4. Gerar uma questão.
5. Selecionar uma alternativa.
6. Visualizar a correção e a explicação.
7. Avançar para outra questão.
8. Consultar o progresso registrado.

## 12. Conclusão

O PsiFluxo Edu demonstra a integração entre Inteligência Artificial generativa, desenvolvimento web, validação de dados e persistência de informações.

A aplicação permite que o estudante interaja com um tutor inteligente, pratique conhecimentos por meio de questões dinâmicas e acompanhe seu desempenho.

O projeto constitui uma prova de conceito funcional para aplicações educacionais apoiadas por modelos de linguagem.