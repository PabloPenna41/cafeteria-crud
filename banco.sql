CREATE DATABASE gestao_cafeteria;
USE gestao_cafeteria;

-- Tabela para o sistema de login
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

-- Tabela para o CRUD do cardápio da cafeteria
CREATE TABLE cardapio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_item VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL, -- Ex: Café, Doce, Salgado, Bebida Gelada
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE
);

-- Inserindo um usuário administrador padrão (Senha: admin123)
INSERT INTO usuarios (nome, usuario, senha) VALUES ('Gerente', 'admin', 'admin123');
