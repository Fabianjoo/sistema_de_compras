-- Cria o banco de dados
CREATE DATABASE loja;
USE loja;

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT,
    preco DECIMAL(10,2),
    quantidade INT
);

-- Insere dados de exemplo
INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES
('teclado', 'Teclado mecânico RGB', 250.00, 10),
('mouse', 'Mouse gamer', 120.00, 15),
('monitor', 'Monitor 24 polegadas', 850.00, 5);
