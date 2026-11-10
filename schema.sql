
-- Banco de dados do sistema de livros

CREATE TABLE IF NOT EXISTS livro (
    id     INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor  TEXT NOT NULL,
    ano    INTEGER NOT NULL,
    isbn   TEXT NOT NULL UNIQUE
);
