CREATE DATABASE IF NOT EXISTS atendimentos_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE atendimentos_db;

CREATE TABLE IF NOT EXISTS atendimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    atendente VARCHAR(100) NOT NULL,
    data_atendimento DATE NOT NULL,
    status VARCHAR(30) NOT NULL,
    descricao TEXT NULL,
    tempo_atendimento INT NULL,
    satisfacao DECIMAL(2,1) NULL,
    INDEX idx_atendimentos_data (data_atendimento),
    INDEX idx_atendimentos_categoria (categoria),
    INDEX idx_atendimentos_status (status),
    CONSTRAINT chk_tempo_nao_negativo
      CHECK (tempo_atendimento IS NULL OR tempo_atendimento >= 0),
    CONSTRAINT chk_satisfacao_intervalo
      CHECK (satisfacao IS NULL OR (satisfacao >= 0 AND satisfacao <= 5))
);

-- Opcional: descomente e execute somente se quiser inserir dados demonstrativos.
-- Não execute se já possuir os registros reais do seu projeto.
-- INSERT INTO atendimentos
-- (cliente, categoria, atendente, data_atendimento, status, descricao, tempo_atendimento, satisfacao)
-- VALUES
-- ('Cliente Exemplo 1', 'Suporte', 'Atendente A', '2026-09-01', 'Concluído', 'Exemplo demonstrativo', 25, 5.0),
-- ('Cliente Exemplo 2', 'Financeiro', 'Atendente B', '2026-09-02', 'Concluído', 'Exemplo demonstrativo', 40, 4.0),
-- ('Cliente Exemplo 3', 'Suporte', 'Atendente A', '2026-09-03', 'Em andamento', 'Exemplo demonstrativo', 15, NULL);
