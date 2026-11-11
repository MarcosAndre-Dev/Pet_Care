DROP TABLE IF EXISTS tokens;
DROP TABLE IF EXISTS pets;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS tutores;

CREATE TABLE tutores (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL,
    CONSTRAINT uq_tutores_email UNIQUE (email)
);

CREATE TABLE pets (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(60) NOT NULL,
    especie VARCHAR(20) NOT NULL,
    raca VARCHAR(60) NULL,
    data_nascimento DATE NOT NULL,
    peso_kg NUMERIC(5,2) NOT NULL,
    tutor_id BIGINT NOT NULL,
    CONSTRAINT fk_pets_tutor FOREIGN KEY (tutor_id)
        REFERENCES tutores (id) ON DELETE CASCADE
);

CREATE TABLE usuarios (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    CONSTRAINT uq_usuarios_email UNIQUE (email)
);

CREATE TABLE tokens (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL,
    token VARCHAR(64) NOT NULL,
    expira_em TIMESTAMP NOT NULL,
    CONSTRAINT uq_tokens_token UNIQUE (token),
    CONSTRAINT fk_tokens_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios (id) ON DELETE CASCADE
);

INSERT INTO tutores (nome, telefone, email) VALUES
('Marina Alves',    '(61) 99911-2233', 'marina.alves@example.com'),
('Pedro Esmeraldo',   '(61) 98822-3344', 'pedro.esmeraldo@example.com'),
('Camila Rocha',    '(61) 99733-4455', 'camila.rocha@example.com'),
('Rafael Lannes',    '(61) 98644-5566', 'rafael.lannes@example.com'),
('Juliana Prado',   '(61) 99555-6677', 'juliana.prado@example.com');

INSERT INTO pets (nome, especie, raca, data_nascimento, peso_kg, tutor_id) VALUES
('Rex',     'cachorro', 'Labrador',         '2021-03-10', 28.50, 1),
('Mimi',    'gato',     'Siamês',           '2022-07-22',  4.20, 1),
('Bidu',    'cachorro', 'Vira-lata',        '2020-01-15', 15.00, 1),
('Thor',    'cachorro', 'Pastor Alemão',    '2019-11-02', 32.80, 2),
('Luna',    'gato',     NULL,               '2023-02-28',  3.60, 3),
('Pingo',   'ave',      'Calopsita',        '2022-05-05',  0.09, 3),
('Fred',    'roedor',   'Hamster',          '2024-01-20',  0.04, 4),
('Nina',    'cachorro', 'Poodle',           '2021-09-09',  6.50, 4),
('Zeca',    'gato',     'Persa',            '2020-12-12',  4.80, 5),
('Toby',    'outro',    'Coelho',           '2023-06-18',  2.10, 5);

INSERT INTO usuarios (nome, email, senha_hash) VALUES
('Professor Jr', 'professor@petcare.com', '$2y$10$0VGvqgzlau2BJQpDTF/F7.VQ.oTD3aXDPBC9QJhC1nVTPy7IMzS7K');