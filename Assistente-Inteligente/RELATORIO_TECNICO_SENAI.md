# RELATÓRIO TÉCNICO — ASSISTENTE INTELIGENTE MULTIAGENTE

**Projeto:** Assistente Inteligente — SENAI  
**Área:** Machine Learning e Deep Learning  
**Data:** 28 de outubro de 2026  
**Ambiente:** Windows, Python, Ollama e execução via terminal

## 1. Objetivo

Desenvolver um assistente inteligente local em Python, capaz de receber perguntas, classificá-las por meio de um modelo de linguagem (LLM) e encaminhá-las a um de dois agentes especializados: um agente de programação Python e outro de conhecimentos gerais. A orquestração é feita com LangGraph e a integração com o modelo local utiliza LangChain e Ollama.

## 2. Tecnologias e componentes

- **Python:** linguagem principal da aplicação.
- **Ollama:** execução local dos modelos de linguagem.
- **Llama 3.2 3B:** modelo utilizado pelo classificador na versão validada.
- **LangChain / langchain-ollama:** interface de comunicação com a LLM.
- **LangGraph:** controle de estados, nós e roteamento condicional.
- **JSON Schema:** restrição estrutural da resposta do classificador a `{"categoria": "python"}` ou `{"categoria": "geral"}`.
- **PowerShell / terminal:** execução interativa e testes.

## 3. Arquitetura

```text
Pergunta do usuário
        |
        v
Estado do LangGraph (TypedDict)
        |
        v
Classificador LLM (Llama 3.2 3B)
        |
        v
Categoria em JSON Schema
        |
        +-----------------+
        |                 |
        v                 v
   Agente Python      Agente Geral
        |                 |
        +--------+--------+
                 |
                 v
          Resposta no terminal
```

O estado da aplicação contém `pergunta`, `categoria` e `resposta`. O `StateGraph` registra os nós com `add_node`, liga o início ao classificador com `add_edge` e seleciona o agente por `add_conditional_edges`. Após a execução do agente, o fluxo termina em `END`. O grafo é preparado com `compile` e executado por `invoke`.

## 4. Organização do código

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
├── README.md
└── .gitignore
```

## 5. Desenvolvimento e ajustes

A implementação inicial utilizou o Llama 3.2 1B. Foram observadas saídas fora do formato esperado, classificações incorretas e respostas que tentavam solucionar a pergunta em vez de classificá-la. Foram experimentadas instruções textuais, geração estruturada em JSON Schema e uma classificação binária SIM/NÃO. A estratégia binária falhou nos seis testes apresentados porque o modelo produziu respostas extensas ou incompatíveis com o formato exigido.

A versão posterior utilizou **Llama 3.2 3B e JSON Schema**, com validação do objeto JSON e das categorias permitidas. Essa configuração apresentou resultados satisfatórios nos testes fornecidos. A classificação continua sendo realizada pela LLM; o código apenas valida a estrutura e utiliza a categoria retornada para encaminhar a pergunta.

## 6. Testes e resultados observados

### 6.1. Classificação

- **20 perguntas avaliadas:** 10 com categoria esperada `python` e 10 com categoria esperada `geral`.
- **Acertos observados:** 20/20 (**100% no conjunto testado**).
- **Saídas JSON inválidas:** nenhuma nas 20 execuções apresentadas.
- **Tentativas extras:** nenhuma nas 20 execuções apresentadas.

As perguntas abrangeram instalação de pacotes, funções, Pandas, dicionários, FastAPI, redes neurais em Python, geografia, ciências e conceitos de aprendizado de máquina.

### 6.2. Integração

Quatro perguntas passaram pelo fluxo completo, incluindo classificação, roteamento e geração de resposta:

| Pergunta resumida | Categoria esperada | Categoria obtida | Resultado |
|---|---|---|---|
| Função que calcula o dobro | python | python | Correto |
| Instalação de bibliotecas com pip | python | python | Correto |
| Capital da França | geral | geral | Correto |
| Conceito de fotossíntese | geral | geral | Correto |

**Resultado de roteamento:** 4/4 (**100% nesse conjunto**). As quatro execuções também produziram respostas, sem erro de integração reportado.

### 6.3. Dependências

O comando `python -m pip check` retornou `No broken requirements found.`, indicando que o pip não detectou incompatibilidades declaradas entre os pacotes instalados.

## 7. Avaliação das respostas e limitações

O sistema gerou respostas adequadas em exemplos como cálculo do dobro, instalação de Pandas, capital da França e fotossíntese. Em testes anteriores, contudo, foram observados erros conceituais, como caracterizar Java como linguagem de baixo nível e explicar incorretamente o uso de dados de teste no treinamento supervisionado.

**Limitações identificadas:**

- O acerto de 20/20 não garante precisão universal; algumas perguntas do teste coincidem com exemplos presentes no prompt do classificador.
- O sistema não verifica automaticamente a veracidade de todas as respostas geradas.
- Os exemplos de código não são executados nem validados semanticamente pela aplicação.
- O tempo de resposta depende do hardware local e do tamanho do modelo.
- O formato JSON garante a estrutura, mas não a correção semântica da categoria.

## 8. Reprodução da aplicação

1. Instalar Python e Ollama no computador.
2. Na pasta do projeto, criar e ativar um ambiente virtual.
3. Instalar dependências com `python -m pip install -r requirements.txt`.
4. Baixar o modelo com `ollama pull llama3.2:3b`.
5. Executar `python main.py`.
6. Para validar a classificação, executar `python teste_classificador.py`.
7. Para validar a integração, executar `python teste_integracao.py`.

**Nota:** o Ollama e os pesos do modelo não são incluídos no ZIP de código-fonte. A execução pressupõe que os modelos configurados nos arquivos Python estejam disponíveis localmente.

## 9. Melhorias futuras

- Testar o classificador com perguntas inéditas, inclusive ambíguas, que não estejam nos exemplos do prompt.
- Avaliar precisão factual das respostas com rubricas e referências verificáveis.
- Validar a sintaxe de exemplos Python sem executar código não confiável.
- Registrar tempo de resposta e consumo de recursos.
- Padronizar a configuração do modelo em um único arquivo e melhorar o tratamento de falhas.

## 10. Conclusão

O projeto demonstrou uma arquitetura multiagente local, com classificação de perguntas por LLM, roteamento condicional com LangGraph e geração de respostas por dois agentes especializados. Nos registros apresentados, o classificador acertou 20 de 20 perguntas e o fluxo integrado encaminhou corretamente quatro de quatro perguntas. Esses resultados sustentam a conclusão de que a implementação principal está funcional, embora a precisão das respostas e a generalização do classificador exijam validação adicional.
