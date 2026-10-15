# Sistema de Análise de Atendimentos — versão com IA

Projeto educacional com MySQL, SQLAlchemy, Python, Pandas, FastAPI, LangChain e Groq API.

## Funcionalidades

- CRUD de atendimentos: criar, listar, consultar, atualizar e excluir.
- Indicadores agregados com Pandas.
- Análises por categoria, status, atendente e período.
- Médias de tempo e satisfação, com tratamento de valores ausentes.
- Endpoint de análise em linguagem natural com LangChain + Groq.
- Segredos carregados por variáveis de ambiente; `.env` é ignorado pelo Git.

## Requisitos

- Windows 10/11
- Python 3.10 ou superior
- MySQL 8
- Chave de API Groq
- Conexão com a internet para a LLM

## 1. Preparar o MySQL

Abra o MySQL Workbench ou o cliente MySQL e execute o arquivo `banco.sql` para criar o banco e a tabela caso ainda não existam.

**Importante:** `CREATE TABLE IF NOT EXISTS` não apaga nem substitui os registros existentes. Não execute inserts demonstrativos se não quiser dados de exemplo.

## 2. Criar o ambiente virtual

No terminal PowerShell, dentro desta pasta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação, use temporariamente nesta sessão:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Configurar variáveis de ambiente

Copie `.env.example` para `.env`:

```powershell
Copy-Item .env.example .env
```

Edite `.env` e informe sua senha local do MySQL e sua chave Groq. Não compartilhe nem envie o `.env` ao GitHub.

Exemplo de nomes de variáveis (use seus valores locais):

```dotenv
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=atendimentos_db
GROQ_API_KEY=sua_chave_groq
GROQ_MODEL=llama-3.3-70b-versatile
```

A senha é codificada de forma segura para compor a URL SQLAlchemy, incluindo caracteres especiais como `@`.

## 4. Iniciar a API

```powershell
python -m uvicorn main:app --reload
```

Acesse:
- Swagger: http://127.0.0.1:8000/docs
- Raiz: http://127.0.0.1:8000/
- Saúde da API: http://127.0.0.1:8000/health

## 5. Testar o endpoint de IA

No Swagger, abra `POST /ia/analisar` e envie:

```json
{
  "pergunta": "Analise a distribuição por categoria e status, a satisfação média e o tempo médio. Informe as limitações dos dados e sugira melhorias."
}
```

A resposta contém a pergunta, os indicadores fornecidos ao modelo, a análise gerada, o modelo e um aviso para conferir a interpretação.

## Endpoints principais

### CRUD
- `GET /atendimentos`
- `GET /atendimentos/{atendimento_id}`
- `POST /atendimentos`
- `PUT /atendimentos/{atendimento_id}`
- `DELETE /atendimentos/{atendimento_id}`

### Análises
- `GET /analises/resumo`
- `GET /analises/categorias`
- `GET /analises/status`
- `GET /analises/atendentes`
- `GET /analises/atendente-destaque`
- `GET /analises/tempo-medio`
- `GET /analises/satisfacao`
- `GET /analises/avaliacoes/maiores`
- `GET /analises/avaliacoes/menores`
- `GET /analises/periodo?data_inicio=2026-09-01&data_fim=2026-09-30`
- `GET /analises/desempenho-atendentes`
- `GET /analises/demanda-categorias`

### IA
- `POST /ia/analisar`

## Fluxo da integração de IA

Banco MySQL → SQLAlchemy/Python → Pandas → FastAPI → LangChain → Groq LLM → resposta JSON.

A aplicação calcula os indicadores em Python e os devolve junto com a resposta para permitir conferência. O modelo recebe dados agregados, sem nomes de clientes ou descrições individuais. As instruções pedem que ele não invente fatos e declare limitações.

**Limitação:** prompts não garantem ausência absoluta de alucinações. A resposta deve ser conferida pelos indicadores retornados. Como a chamada é feita a um provedor externo, os indicadores agregados enviados à Groq saem do ambiente local. Avalie a política de privacidade da organização antes de usar dados reais.

## GitHub: cuidados com segredos

- `.env` está no `.gitignore`.
- Envie `.env.example`, nunca `.env`.
- Antes de cada `git push`, revise `git status` e `git diff --cached`.
- Se uma chave ou senha for publicada, revogue/rotacione-a. Apagar o arquivo em um commit posterior não remove o segredo do histórico.
