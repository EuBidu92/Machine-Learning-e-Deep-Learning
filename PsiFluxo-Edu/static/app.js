
const $ = (id) => document.getElementById(id);

const out = $("resultado");
const status = $("status");

let questaoAtual = null;
let respostaSelecionada = null;
let corrigida = false;

function el(tag, texto, classe = "") {
    const elemento = document.createElement(tag);

    if (texto !== undefined && texto !== null) {
        elemento.textContent = texto;
    }

    if (classe) {
        elemento.className = classe;
    }

    return elemento;
}

function limpar() {
    out.replaceChildren();
    status.textContent = "";
}

async function api(caminho, metodo = "GET", corpo = null) {
    const resposta = await fetch(caminho, {
        method: metodo,
        headers: corpo
            ? { "Content-Type": "application/json" }
            : {},
        body: corpo ? JSON.stringify(corpo) : undefined
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(
            dados.erro || "Não foi possível concluir a solicitação."
        );
    }

    return dados;
}

function ocupado(valor) {
    document.querySelectorAll("button").forEach((botao) => {
        botao.disabled = valor;
    });

    status.textContent = valor
        ? "Aguarde, a inteligência artificial está processando..."
        : "";
}

async function executar(funcao) {
    ocupado(true);

    try {
        await funcao();
    } catch (erro) {
        status.textContent = erro.message;
    } finally {
        ocupado(false);
    }
}

function pedido() {
    return {
        tema: $("tema").value.trim(),
        nivel: $("nivel").value
    };
}

function adicionarBotao(texto, classe, acao) {
    const botao = el("button", texto, classe);
    botao.type = "button";
    botao.addEventListener("click", acao);
    out.appendChild(botao);
    return botao;
}

// EXPLICAÇÃO

$("explicar").addEventListener("click", () => {
    executar(async () => {
        const dados = await api(
            "/api/explicar",
            "POST",
            pedido()
        );

        limpar();

        out.appendChild(
            el("h2", "Explicação: " + dados.tema)
        );

        out.appendChild(
            el("p", dados.resposta, "texto-explicacao")
        );
    });
});

// GERAR UMA QUESTÃO

async function gerarQuestao() {
    const dados = await api(
        "/api/exercicios",
        "POST",
        {
            ...pedido(),
            quantidade: 1
        }
    );

    if (!dados.questoes || dados.questoes.length !== 1) {
        throw new Error(
            "A IA não retornou uma questão válida."
        );
    }

    questaoAtual = dados.questoes[0];
    respostaSelecionada = null;
    corrigida = false;

    mostrarQuestao();
}

function mostrarQuestao() {
    limpar();

    const questao = questaoAtual;

    out.appendChild(
        el("h2", "Questão de " + $("tema").value.trim())
    );

    out.appendChild(
        el("p", "Selecione uma alternativa e clique em Corrigir.",
           "subtitulo-questao")
    );

    const cartao = el("div", null, "cartao-questao");

    cartao.appendChild(
        el("h3", questao.enunciado)
    );

    const alternativas = el("div", null, "alternativas");

    questao.alternativas.forEach((texto, indice) => {
        const rotulo = el("label", null, "alternativa");

        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "resposta";
        radio.value = indice;

        radio.addEventListener("change", () => {
            respostaSelecionada = indice;

            document.querySelectorAll(".alternativa")
                .forEach((item) => {
                    item.classList.remove("selecionada");
                });

            rotulo.classList.add("selecionada");
        });

        const letra = String.fromCharCode(65 + indice);

        rotulo.appendChild(radio);
        rotulo.appendChild(
            el("span", `${letra}. ${texto}`)
        );

        alternativas.appendChild(rotulo);
    });

    cartao.appendChild(alternativas);
    out.appendChild(cartao);

    adicionarBotao(
        "Corrigir resposta",
        "botao-principal",
        () => {
            if (respostaSelecionada === null) {
                status.textContent =
                    "Selecione uma alternativa antes de corrigir.";
                return;
            }

            executar(corrigirResposta);
        }
    );
}

// CORREÇÃO INDIVIDUAL

async function corrigirResposta() {
    if (corrigida || respostaSelecionada === null) {
        return;
    }

    const resultado = await api(
        "/api/corrigir",
        "POST",
        {
            respostas: [respostaSelecionada]
        }
    );

    corrigida = true;
    mostrarCorrecao(resultado);
}

function mostrarCorrecao(resultado) {
    limpar();

    const detalhe = resultado.detalhes[0];
    const acertou = detalhe.acertou;

    out.appendChild(
        el(
            "h2",
            acertou ? "Resposta correta!" : "Resposta incorreta",
            acertou ? "texto-sucesso" : "texto-erro"
        )
    );

    const cartao = el("div", null, "cartao-questao");

    cartao.appendChild(
        el("h3", detalhe.enunciado)
    );

    detalhe.alternativas.forEach((alternativa, indice) => {
        const linha = el("div", null, "alternativa resultado");

        const letra = String.fromCharCode(65 + indice);

        linha.textContent = `${letra}. ${alternativa}`;

        if (indice === detalhe.correta) {
            linha.classList.add("correta");
        } else if (indice === respostaSelecionada) {
            linha.classList.add("incorreta");
        }

        cartao.appendChild(linha);
    });

    out.appendChild(cartao);

    const feedback = el("div", null, "feedback");

    feedback.appendChild(
        el("h3", "Explicação da resposta")
    );

    feedback.appendChild(
        el("p", detalhe.explicacao)
    );

    out.appendChild(feedback);

    out.appendChild(
        el(
            "p",
            `Resultado: ${resultado.acertos}/${resultado.total} ` +
            `(${resultado.percentual}%)`,
            "pontuacao"
        )
    );

    adicionarBotao(
        "Próxima questão",
        "botao-principal",
        () => executar(gerarQuestao)
    );
}

$("gerar").addEventListener("click", () => {
    executar(gerarQuestao);
});

// PROGRESSO

$("progresso").addEventListener("click", () => {
    executar(async () => {
        const dados = await api("/api/progresso");

        limpar();

        out.appendChild(
            el("h2", "Meu progresso")
        );

        out.appendChild(
            el(
                "p",
                `${dados.tentativas} tentativas | ` +
                `${dados.acertos}/${dados.questoes} acertos | ` +
                `${dados.percentual}%`,
                "pontuacao"
            )
        );

        dados.historico.forEach((item) => {
            out.appendChild(
                el(
                    "p",
                    `${item.tema} (${item.nivel}): ` +
                    `${item.acertos}/${item.total} - ` +
                    new Date(item.criado_em)
                        .toLocaleDateString("pt-BR")
                )
            );
        });
    });
});
