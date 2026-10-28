# Assistente Inteligente Multiagente — SENAI

Projeto educacional de assistente de IA executado localmente, desenvolvido com Python, LangChain, LangGraph e Ollama. O sistema recebe perguntas pelo terminal, usa uma LLM para selecionar um agente especializado e apresenta a resposta.

## Objetivo

Demonstrar o roteamento inteligente de perguntas entre dois agentes:

- **Agente Python:** linguagem Python, bibliotecas, programação e implementação de soluções em Python.
- **Agente Geral:** conhecimentos gerais, história, ciências e conceitos de inteligência artificial sem foco em implementação Python.

A classificação é feita pela **LLM**, sem regras de palavras-chave no código. O retorno do classificador utiliza um esquema JSON com a propriedade `categoria`, cujos valores possíveis são `python` e `geral`.

## Tecnologias

- Python
- LangChain e `langchain-ollama`
- LangGraph
- Ollama
- Modelo local `llama3.2:3b`

## Arquitetura

```text
Pergunta no terminal
        |
        v
  main.py / app.invoke()
        |
        v
Classificador LLM (JSON Schema)
        |
        +------------+------------+
        |                         |
     "python"                   "geral"
        |                         |
        v                         v
  Agente Python             Agente Geral
        |                         |
        +------------+------------+
                     |
                     v
               Resposta final
```

O `StateGraph` mantém o estado da pergunta, categoria e resposta. O fluxo possui um nó de classificação e dois nós de agentes. `add_conditional_edges` escolhe o agente com base na categoria retornada pela LLM.

## Estrutura sugerida

```text
Assistente-Inteligente/
├── agentes/
│   ├── __init__.py
│   ├── classificador.py
│   ├── agente_python.py
│   └── agente_geral.py
├── grafo/
│   ├── __init__.py
│   └── fluxo.py
├── main.py
├── modelo.py
├── teste_ollama.py
├── teste_classificador.py
├── teste_integracao.py
├── requirements.txt
├── .gitignore
└── README.md
```

> Confira a estrutura real antes da entrega e ajuste esta seção se necessário.

## Instalação no Windows (PowerShell)

### 1. Pré-requisitos

Instale o Python e o Ollama. Certifique-se de que os comandos `python` e `ollama` estão disponíveis no terminal.

### 2. Obter o modelo

```powershell
ollama pull llama3.2:3b
ollama list
```

O Ollama deve estar em execução antes de iniciar o assistente.

### 3. Criar e ativar ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se a política de execução do PowerShell bloquear a ativação, use na sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependências

```powershell
python -m pip install -r requirements.txt
```

### 5. Executar

```powershell
python main.py
```

Digite uma pergunta e pressione Enter. Para encerrar, digite `sair`.

## Como o LangGraph é utilizado

- **`TypedDict`**: define as chaves do estado (`pergunta`, `categoria`, `resposta`).
- **`StateGraph`**: cria o fluxo de execução.
- **`add_node()`**: registra o classificador e os agentes.
- **`add_edge()`**: liga o início ao classificador e os agentes ao fim.
- **`add_conditional_edges()`**: direciona a execução conforme a categoria.
- **`compile()`**: prepara o grafo para execução.
- **`invoke()`**: processa a pergunta e retorna o estado final.

## Testes

### Teste de classificação

```powershell
python teste_classificador.py
```

**Resultado observado no desenvolvimento:** 20 acertos em 20 perguntas (100% no conjunto testado). Foram usadas dez perguntas da categoria Python e dez da categoria Geral. Todas as respostas de classificação observadas tinham JSON válido e foram obtidas na primeira tentativa.

### Teste de integração

```powershell
python teste_integracao.py
```

**Resultado observado no desenvolvimento:** 4 acertos em 4 perguntas (100% no conjunto testado), com respostas produzidas pelos agentes esperados.

Esses percentuais representam apenas os conjuntos avaliados; não garantem precisão em perguntas inéditas.

## Exemplos de perguntas

**Python:** `Como instalar bibliotecas com pip?` ou `Crie uma função Python que calcule o dobro de um número.`

**Geral:** `Qual é a capital da França?` ou `O que é fotossíntese?`

## Limitações

- A LLM pode classificar incorretamente perguntas ambíguas ou inéditas.
- Os agentes podem produzir respostas factualmente incorretas ou código incompleto.
- A execução local em CPU pode ser lenta, especialmente com modelos maiores.
- Os resultados de teste não equivalem a validação universal do sistema.
- Exemplos de código gerados devem ser revisados antes de uso.

## Evolução do desenvolvimento

Durante os testes iniciais, o modelo `llama3.2:1b` apresentou inconsistências na classificação. A combinação de `llama3.2:3b`, instruções específicas e saída estruturada em JSON apresentou resultados melhores nos testes executados. As baterias anteriores não utilizaram condições idênticas e não constituem um benchmark controlado.

## Autoria e contexto

Projeto desenvolvido como atividade prática do SENAI, com foco em agentes de IA, processamento de linguagem natural e orquestração de fluxos com LangGraph.
