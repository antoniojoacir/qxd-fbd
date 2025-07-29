-- =============================================
--  CRIAÇÃO DO BANCO
-- =============================================

CREATE TABLE enderecos (
	id_endereco SERIAL PRIMARY KEY,
	cep VARCHAR(8) NOT NULL,
	cidade VARCHAR(60) NOT NULL,
	rua VARCHAR(60) NOT NULL,
	uf VARCHAR(2) NOT NULL,
	numero INT
);

CREATE TABLE contatos (
	id_contato SERIAL PRIMARY KEY,
	tipo_contato VARCHAR(20) NOT NULL,
	info_contato VARCHAR(80) UNIQUE NOT NULL
);

CREATE TABLE clientes (
	id_cliente SERIAL PRIMARY KEY,
	cpf VARCHAR(11) UNIQUE NOT NULL,
	pnome VARCHAR(40) NOT NULL,
	unome VARCHAR(40) NOT NULL,
	data_nasc DATE NOT NULL,
	genero VARCHAR(20) NOT NULL,

	-- chaves estrangeiras
	id_contato INT,
	id_endereco INT,

	FOREIGN KEY (id_contato) REFERENCES contatos(id_contato),
	FOREIGN KEY (id_endereco) REFERENCES enderecos(id_endereco)
);

CREATE TABLE eventos (
	id_evento SERIAL PRIMARY KEY,
	titulo VARCHAR(60) NOT NULL,
	data_inicio DATE NOT NULL,
	data_fim DATE NOT NULL,
	horario_inicio TIME NOT NULL,
	horario_fim TIME,

	-- chaves estrangeiras
	id_contato INT,
	id_endereco INT,

	FOREIGN KEY (id_contato) REFERENCES contatos(id_contato),
	FOREIGN KEY (id_endereco) REFERENCES enderecos(id_endereco)
);

CREATE TABLE tickets (
	id_ticket INT PRIMARY KEY,
	numero INT UNIQUE NOT NULL,
	lote VARCHAR(20) NOT NULL,

	-- chaves estrangeiras
	id_cliente INT,
	id_evento INT,

	FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
	FOREIGN KEY (id_evento) REFERENCES eventos(id_evento)
);

CREATE TABLE atracoes (
	id_atracao SERIAL PRIMARY KEY,
	cnpj VARCHAR(14) UNIQUE NOT NULL,
	nome_atracao VARCHAR(60) NOT NULL,
	tipo_atracao VARCHAR(30) NOT NULL,

	-- chaves estrangeiras
	id_contato INT,

	FOREIGN KEY (id_contato) REFERENCES contatos(id_contato)
);

CREATE TABLE se_apresenta (
	id_atracao INT,
	id_evento INT,

	PRIMARY KEY (id_atracao, id_evento),

	FOREIGN KEY (id_atracao) REFERENCES atracoes(id_atracao),
	FOREIGN KEY (id_evento) REFERENCES eventos(id_evento)
);

-- Mock Data Generation for Ticket System Database (V2)
-- Total Records:
-- enderecos: 60 (40 for clients, 20 for events)
-- contatos: 80 (40 for clients, 40 for attractions)
-- clientes: 40
-- atracoes: 40
-- eventos: 20
-- se_apresenta: ~60 (varied distribution)
-- tickets: 40

-- =============================================
--  TABLE: enderecos
-- =============================================
-- Note: 60 addresses created (40 for clients, 20 for events).
-- IDs 1-40 are for clients.
-- IDs 41-60 are for events.
INSERT INTO enderecos (id_endereco, cep, cidade, rua, uf, numero) VALUES
-- Endereços para Clientes (1-40)
(1, '01001000', 'São Paulo', 'Praça da Sé', 'SP', 100),
(2, '20040030', 'Rio de Janeiro', 'Avenida Rio Branco', 'RJ', 200),
(3, '30130000', 'Belo Horizonte', 'Avenida Afonso Pena', 'MG', 300),
(4, '70070000', 'Brasília', 'Eixo Monumental', 'DF', 400),
(5, '40020000', 'Salvador', 'Avenida Sete de Setembro', 'BA', 500),
(6, '50030000', 'Recife', 'Avenida Marquês de Olinda', 'PE', 600),
(7, '60170000', 'Fortaleza', 'Avenida Beira Mar', 'CE', 700),
(8, '80020310', 'Curitiba', 'Rua XV de Novembro', 'PR', 800),
(9, '90010150', 'Porto Alegre', 'Rua dos Andradas', 'RS', 900),
(10, '69005000', 'Manaus', 'Avenida Eduardo Ribeiro', 'AM', 1000),
(11, '11010151', 'Santos', 'Avenida Ana Costa', 'SP', 110),
(12, '29010002', 'Vitória', 'Avenida Jerônimo Monteiro', 'ES', 120),
(13, '49010000', 'Aracaju', 'Praça Fausto Cardoso', 'SE', 130),
(14, '57020000', 'Maceió', 'Avenida da Paz', 'AL', 140),
(15, '58010820', 'João Pessoa', 'Avenida Visconde de Pelotas', 'PB', 150),
(16, '59020000', 'Natal', 'Avenida Deodoro da Fonseca', 'RN', 160),
(17, '64000160', 'Teresina', 'Avenida Frei Serafim', 'PI', 170),
(18, '65010000', 'São Luís', 'Rua do Giz', 'MA', 180),
(19, '78005000', 'Cuiabá', 'Avenida Getúlio Vargas', 'MT', 190),
(20, '79002203', 'Campo Grande', 'Avenida Afonso Pena', 'MS', 200),
(21, '74013010', 'Goiânia', 'Avenida Goiás', 'GO', 210),
(22, '77001002', 'Palmas', 'Avenida Juscelino Kubitschek', 'TO', 220),
(23, '69301110', 'Boa Vista', 'Avenida Jaime Brasil', 'RR', 230),
(24, '69900084', 'Rio Branco', 'Rua Rui Barbosa', 'AC', 240),
(25, '68900070', 'Macapá', 'Avenida Fab', 'AP', 250),
(26, '76801059', 'Porto Velho', 'Avenida Sete de Setembro', 'RO', 260),
(27, '88010000', 'Florianópolis', 'Avenida Beira Mar Norte', 'SC', 270),
(28, '04538133', 'São Paulo', 'Avenida Brigadeiro Faria Lima', 'SP', 280),
(29, '22290160', 'Rio de Janeiro', 'Avenida Pasteur', 'RJ', 290),
(30, '30112021', 'Belo Horizonte', 'Rua da Bahia', 'MG', 300),
(31, '70390100', 'Brasília', 'SQS 108 Bloco A', 'DF', 310),
(32, '41820021', 'Salvador', 'Avenida Tancredo Neves', 'BA', 320),
(33, '52060000', 'Recife', 'Avenida Parnamirim', 'PE', 330),
(34, '60115170', 'Fortaleza', 'Rua Osvaldo Cruz', 'CE', 340),
(35, '80230010', 'Curitiba', 'Avenida Sete de Setembro', 'PR', 350),
(36, '90430000', 'Porto Alegre', 'Rua Padre Chagas', 'RS', 360),
(37, '69057025', 'Manaus', 'Avenida Djalma Batista', 'AM', 370),
(38, '13025151', 'Campinas', 'Rua Coronel Quirino', 'SP', 380),
(39, '89010203', 'Blumenau', 'Rua XV de Novembro', 'SC', 390),
(40, '38400666', 'Uberlândia', 'Avenida Rondon Pacheco', 'MG', 400),
-- Endereços para Eventos (41-60)
(41, '01311300', 'São Paulo', 'Avenida Paulista', 'SP', 1578),
(42, '22410003', 'Rio de Janeiro', 'Rua Vinicius de Moraes', 'RJ', 100),
(43, '30140081', 'Belo Horizonte', 'Rua Sergipe', 'MG', 1211),
(44, '70342000', 'Brasília', 'SHIS QI 5', 'DF', 15),
(45, '40140090', 'Salvador', 'Rua da Paciência', 'BA', 320),
(46, '51020000', 'Recife', 'Avenida Boa Viagem', 'PE', 5550),
(47, '60165080', 'Fortaleza', 'Avenida da Abolição', 'CE', 2500),
(48, '80420000', 'Curitiba', 'Alameda Dr. Carlos de Carvalho', 'PR', 987),
(49, '90570020', 'Porto Alegre', 'Rua Fernando Gomes', 'RS', 178),
(50, '69053040', 'Manaus', 'Rua Pará', 'AM', 455),
(51, '13073300', 'Campinas', 'Avenida Doutor Heitor Penteado', 'SP', 1671),
(52, '88058300', 'Florianópolis', 'Rodovia Armando Calil Bulos', 'SC', 5874),
(53, '29102901', 'Vila Velha', 'Rodovia do Sol', 'ES', 5000),
(54, '74230022', 'Goiânia', 'Avenida T-10', 'GO', 1300),
(55, '65071380', 'São Luís', 'Avenida dos Holandeses', 'MA', 10),
(56, '59090001', 'Natal', 'Avenida Erivan França', 'RN', 80),
(57, '49035500', 'Aracaju', 'Avenida Santos Dumont', 'SE', 999),
(58, '89221006', 'Joinville', 'Rua Orestes Guimarães', 'SC', 634),
(59, '38408100', 'Uberlândia', 'Avenida Nicomedes Alves dos Santos', 'MG', 1800),
(60, '14020260', 'Ribeirão Preto', 'Avenida Presidente Vargas', 'SP', 2121);

-- =============================================
--  TABLE: contatos
-- =============================================
-- Note: 80 contacts created (40 for clients, 40 for attractions).
-- IDs 1-40 are for clients.
-- IDs 41-80 are for attractions/organizers.
INSERT INTO contatos (id_contato, tipo_contato, info_contato) VALUES
-- Contatos de Clientes (1-40)
(1, 'email', 'joao.silva@example.com'), (2, 'telefone', '11987654321'), (3, 'email', 'maria.oliveira@example.com'),
(4, 'telefone', '21912345678'), (5, 'email', 'pedro.santos@example.com'), (6, 'telefone', '31988887777'),
(7, 'email', 'ana.souza@example.com'), (8, 'telefone', '71999998888'), (9, 'email', 'carlos.pereira@example.com'),
(10, 'telefone', '81987651234'), (11, 'email', 'lucas.costa@example.com'), (12, 'telefone', '85998765432'),
(13, 'email', 'sandra.rodrigues@example.com'), (14, 'telefone', '41988776655'), (15, 'email', 'fernando.almeida@example.com'),
(16, 'telefone', '51996554433'), (17, 'email', 'juliana.lima@example.com'), (18, 'telefone', '92981112233'),
(19, 'email', 'marcos.fernandes@example.com'), (20, 'telefone', '11976543210'), (21, 'email', 'beatriz.goncalves@example.com'),
(22, 'telefone', '21987654321'), (23, 'email', 'rafael.carvalho@example.com'), (24, 'telefone', '31991234567'),
(25, 'email', 'amanda.martins@example.com'), (26, 'telefone', '71981234567'), (27, 'email', 'tiago.araujo@example.com'),
(28, 'telefone', '81998761234'), (29, 'email', 'gabriela.barbosa@example.com'), (30, 'telefone', '85987651234'),
(31, 'email', 'rodrigo.melo@example.com'), (32, 'telefone', '41998765432'), (33, 'email', 'camila.ribeiro@example.com'),
(34, 'telefone', '51981234567'), (35, 'email', 'bruno.nunes@example.com'), (36, 'telefone', '92991234567'),
(37, 'email', 'vanessa.gomes@example.com'), (38, 'telefone', '11981234567'), (39, 'email', 'felipe.soares@example.com'),
(40, 'telefone', '21976541234'),
-- Contatos de Atrações/Organizadores (41-80)
(41, 'email', 'contato@rockinrio.com.br'), (42, 'website', 'https://www.lollapaloozabr.com'), (43, 'email', 'comercial@t4f.com.br'),
(44, 'email', 'info@ccxp.com.br'), (45, 'website', 'https://www.tomorrowlandbrasil.com'), (46, 'telefone', '1130331234'),
(47, 'email', 'contato@bandau2.com'), (48, 'website', 'https://www.ivetesangalo.com.br'), (49, 'email', 'shows@skank.com.br'),
(50, 'website', 'https://www.anitta.com'), (51, 'email', 'booking@alok.com.br'), (52, 'website', 'https://www.gusttavolima.com.br'),
(53, 'telefone', '6232258899'), (54, 'email', 'contato@mariliamendonca.com.br'), (55, 'website', 'https://www.jorgeemateus.com.br'),
(56, 'email', 'shows@henriqueejuliano.com.br'), (57, 'website', 'https://www.wesleysafadao.com.br'), (58, 'telefone', '8533445566'),
(59, 'email', 'contato@thiaguinho.net'), (60, 'website', 'https://www.ludmilla.com'), (61, 'email', 'contato@marisamonte.com.br'),
(62, 'website', 'https://www.caetanoveloso.com.br'), (63, 'email', 'gilbertogil@site.com.br'), (64, 'website', 'https://www.djavan.com.br'),
(65, 'email', 'shows@titans.com.br'), (66, 'website', 'https://www.paralamas.com.br'), (67, 'email', 'contato@maneva.com.br'),
(68, 'website', 'https://www.natiruts.com.br'), (69, 'email', 'shows@emicida.com.br'), (70, 'website', 'https://www.projota.com.br'),
(71, 'email', 'shows@racionaismcs.com.br'), (72, 'website', 'https://www.criolo.net'), (73, 'email', 'contato@fabioporchat.com.br'),
(74, 'website', 'https://www.whindersson.com.br'), (75, 'telefone', '11987659999'), (76, 'email', 'contato@paulogustavo.com.br'),
(77, 'website', 'https://www.leandrokarnal.com.br'), (78, 'email', 'palestras@cortella.com.br'), (79, 'website', 'https://www.monjacoen.com.br'),
(80, 'email', 'contato@showdaluna.com.br');

-- =============================================
--  TABLE: clientes - CORRIGIDA
-- =============================================
-- 40 clientes, com a coluna 'genero' adicionada e populada.
INSERT INTO clientes (id_cliente, cpf, pnome, unome, data_nasc, genero, id_contato, id_endereco) VALUES
(1, '11122233344', 'João', 'Silva', '1990-05-15', 'Masculino', 1, 1),
(2, '22233344455', 'Maria', 'Oliveira', '1985-09-20', 'Feminino', 2, 2),
(3, '33344455566', 'Pedro', 'Santos', '1992-02-10', 'Masculino', 3, 3),
(4, '44455566677', 'Ana', 'Souza', '1998-11-30', 'Feminino', 4, 4),
(5, '55566677788', 'Carlos', 'Pereira', '1980-07-25', 'Masculino', 5, 5),
(6, '66677788899', 'Lucas', 'Costa', '2000-01-05', 'Masculino', 6, 6),
(7, '77788899900', 'Sandra', 'Rodrigues', '1988-04-18', 'Feminino', 7, 7),
(8, '88899900011', 'Fernando', 'Almeida', '1995-08-12', 'Masculino', 8, 8),
(9, '99900011122', 'Juliana', 'Lima', '1993-06-22', 'Feminino', 9, 9),
(10, '00011122233', 'Marcos', 'Fernandes', '1983-03-03', 'Masculino', 10, 10),
(11, '12345678901', 'Beatriz', 'Gonçalves', '2001-12-01', 'Feminino', 11, 11),
(12, '23456789012', 'Rafael', 'Carvalho', '1991-10-14', 'Masculino', 12, 12),
(13, '34567890123', 'Amanda', 'Martins', '1999-07-07', 'Feminino', 13, 13),
(14, '45678901234', 'Tiago', 'Araujo', '1987-05-28', 'Masculino', 14, 14),
(15, '56789012345', 'Gabriela', 'Barbosa', '1996-09-09', 'Feminino', 15, 15),
(16, '67890123456', 'Rodrigo', 'Melo', '1982-11-11', 'Masculino', 16, 16),
(17, '78901234567', 'Camila', 'Ribeiro', '1994-01-21', 'Feminino', 17, 17),
(18, '89012345678', 'Bruno', 'Nunes', '1997-03-13', 'Masculino', 18, 18),
(19, '90123456789', 'Vanessa', 'Gomes', '1989-10-24', 'Feminino', 19, 19),
(20, '01234567890', 'Felipe', 'Soares', '1986-08-08', 'Masculino', 20, 20),
(21, '11223344556', 'Larissa', 'Dias', '2002-06-16', 'Feminino', 21, 21),
(22, '22334455667', 'Gustavo', 'Ferreira', '1984-02-24', 'Masculino', 22, 22),
(23, '33445566778', 'Patrícia', 'Alves', '1990-09-19', 'Feminino', 23, 23),
(24, '44556677889', 'Leonardo', 'Monteiro', '1995-12-31', 'Masculino', 24, 24),
(25, '55667788990', 'Daniela', 'Cardoso', '1981-07-17', 'Feminino', 25, 25),
(26, '66778899001', 'Vinícius', 'Pinto', '2003-05-05', 'Masculino', 26, 26),
(27, '77889900112', 'Aline', 'Teixeira', '1988-10-10', 'Feminino', 27, 27),
(28, '88990011223', 'Márcio', 'Correia', '1992-04-04', 'Masculino', 28, 28),
(29, '99001122334', 'Tatiane', 'Santana', '1996-02-29', 'Feminino', 29, 29),
(30, '00112233445', 'Eduardo', 'Bezerra', '1987-09-01', 'Masculino', 30, 30),
(31, '12121212121', 'Cristina', 'Rocha', '1993-08-14', 'Feminino', 31, 31),
(32, '34343434343', 'Ricardo', 'Freitas', '1991-06-03', 'Masculino', 32, 32),
(33, '56565656565', 'Simone', 'Campos', '1998-03-25', 'Feminino', 33, 33),
(34, '78787878787', 'André', 'Vieira', '1985-11-27', 'Masculino', 34, 34),
(35, '90909090909', 'Renata', 'Andrade', '2000-10-02', 'Feminino', 35, 35),
(36, '13131313131', 'Marcelo', 'Duarte', '1982-01-20', 'Masculino', 36, 36),
(37, '24242424242', 'Flávia', 'Moreira', '1997-07-30', 'Feminino', 37, 37),
(38, '35353535353', 'Diego', 'Nascimento', '1989-05-18', 'Masculino', 38, 38),
(39, '46464646464', 'Débora', 'Lopes', '1994-04-12', 'Feminino', 39, 39),
(40, '57575757575', 'Antônio', 'Machado', '1980-12-07', 'Masculino', 40, 40);

-- =============================================
--  TABLE: atracoes
-- =============================================
-- 40 atrações
INSERT INTO atracoes (id_atracao, cnpj, nome_atracao, tipo_atracao, id_contato) VALUES
(1, '11222333000144', 'U2 Cover Brasil', 'Banda Musical', 47), (2, '22333444000155', 'Ivete Sangalo', 'Cantora Solo', 48),
(3, '33444555000166', 'Skank', 'Banda Musical', 49), (4, '44555666000177', 'Anitta', 'Cantora Solo', 50),
(5, '55666777000188', 'Alok', 'DJ', 51), (6, '66777888000199', 'Gusttavo Lima', 'Cantor Solo', 52),
(7, '77888999000100', 'Marília Mendonça Eternamente', 'Show Tributo', 54), (8, '88999000000111', 'Jorge & Mateus', 'Dupla Sertaneja', 55),
(9, '99000111000122', 'Henrique & Juliano', 'Dupla Sertaneja', 56), (10, '00111222000133', 'Wesley Safadão', 'Cantor Solo', 57),
(11, '12345678000199', 'Thiaguinho', 'Cantor Solo', 59), (12, '23456789000100', 'Ludmilla', 'Cantora Solo', 60),
(13, '34567890000111', 'Mágico Renner', 'Mágica e Ilusionismo', 46), (14, '45678901000122', 'Cirque du Soleil', 'Circo', 41),
(15, '56789012000133', 'Porta dos Fundos', 'Comédia Stand-up', 42), (16, '67890123000144', 'DJ Marshmello Cover', 'DJ', 45),
(17, '78901234000155', 'Orquestra Sinfônica Brasileira', 'Música Clássica', 43), (18, '89012345000166', 'Guns N'' Roses Cover', 'Banda Musical', 47),
(19, '90123456000177', 'Capital Inicial', 'Banda Musical', 49), (20, '01234567000188', 'Queen Experience', 'Show Tributo', 53),
(21, '10101010000110', 'Marisa Monte', 'Cantora Solo', 61), (22, '20202020000120', 'Caetano Veloso', 'Cantor Solo', 62),
(23, '30303030000130', 'Gilberto Gil', 'Cantor Solo', 63), (24, '40404040000140', 'Djavan', 'Cantor Solo', 64),
(25, '50505050000150', 'Titãs', 'Banda Musical', 65), (26, '60606060000160', 'Paralamas do Sucesso', 'Banda Musical', 66),
(27, '70707070000170', 'Maneva', 'Banda Musical', 67), (28, '80808080000180', 'Natiruts', 'Banda Musical', 68),
(29, '90909090000190', 'Emicida', 'Rapper', 69), (30, '09876543000100', 'Projota', 'Rapper', 70),
(31, '19283746000110', 'Racionais MCs', 'Grupo de Rap', 71), (32, '57463524000120', 'Criolo', 'Rapper', 72),
(33, '36475869000130', 'Fábio Porchat', 'Comédia Stand-up', 73), (34, '11235813000140', 'Whindersson Nunes', 'Comédia Stand-up', 74),
(35, '22345678000150', 'Paulo Gustavo Eterno', 'Show Tributo', 76), (36, '33456789000160', 'Leandro Karnal', 'Palestrante', 77),
(37, '44567890000170', 'Mário Sérgio Cortella', 'Palestrante', 78), (38, '55678901000180', 'Monja Coen', 'Palestrante', 79),
(39, '66789012000190', 'O Show da Luna!', 'Infantil', 80), (40, '77890123000100', 'Galinha Pintadinha O Show', 'Infantil', 46);

-- =============================================
--  TABLE: eventos
-- =============================================
-- 20 eventos
INSERT INTO eventos (id_evento, titulo, data_inicio, data_fim, horario_inicio, horario_fim, id_contato, id_endereco) VALUES
(1, 'Festival Rock Brasil', '2025-09-18', '2025-09-20', '14:00:00', '04:00:00', 41, 41),
(2, 'Festival Pop Brasil', '2026-03-26', '2026-03-28', '11:00:00', '23:00:00', 42, 42),
(3, 'Festival Sertanejo Raiz', '2025-08-21', '2025-08-23', '18:00:00', '06:00:00', 52, 47),
(4, 'Noite da Comédia', '2025-11-15', '2025-11-15', '20:00:00', '23:30:00', 44, 43),
(5, 'Festival Reggae Paz e Amor', '2025-07-12', '2025-07-12', '16:00:00', '02:00:00', 68, 45),
(6, 'Encontro Lendas da MPB', '2025-10-10', '2025-10-11', '19:00:00', '01:00:00', 62, 48),
(7, 'Festival Rap Nacional', '2026-04-18', '2026-04-18', '17:00:00', '03:00:00', 71, 46),
(8, 'Show Solo: Ivete Sangalo', '2025-09-06', '2025-09-06', '21:00:00', '23:00:00', 48, 51),
(9, 'Show Solo: Gusttavo Lima', '2025-11-29', '2025-11-29', '22:00:00', '00:00:00', 52, 54),
(10, 'Palestra: O Futuro do Pensamento', '2025-08-05', '2025-08-05', '19:30:00', '21:00:00', 77, 49),
(11, 'Tributo ao Rock Internacional', '2026-01-24', '2026-01-24', '21:00:00', '01:00:00', 47, 50),
(12, 'Show Solo: Thiaguinho', '2025-10-04', '2025-10-04', '22:00:00', '23:59:00', 59, 52),
(13, 'Festival Kids', '2025-07-26', '2025-07-27', '14:00:00', '18:00:00', 80, 53),
(14, 'Show Solo: Djavan', '2025-09-27', '2025-09-27', '20:00:00', '22:00:00', 64, 55),
(15, 'Palestra Magna com Monja Coen', '2026-02-10', '2026-02-10', '20:00:00', '21:30:00', 79, 56),
(16, 'A Mágica do Circo', '2025-12-20', '2025-12-21', '17:00:00', '19:00:00', 41, 57),
(17, 'Concerto de Orquestra', '2026-05-09', '2026-05-09', '20:30:00', '22:00:00', 43, 58),
(18, 'Show Solo: Alok', '2025-11-01', '2025-11-01', '23:00:00', '02:00:00', 51, 59),
(19, 'Tributo à Rainha do Sertanejo', '2026-03-07', '2026-03-07', '21:00:00', '23:00:00', 54, 60),
(20, 'Tributo ao Rei do Pop', '2026-06-25', '2026-06-25', '20:00:00', '22:00:00', 53, 44);

-- =============================================
--  TABLE: se_apresenta
-- =============================================
-- Distribuição de shows variada
INSERT INTO se_apresenta (id_atracao, id_evento) VALUES
-- Evento 1: Festival Rock Brasil (6 atrações)
(3, 1), (19, 1), (25, 1), (26, 1), (27, 1), (28, 1),
-- Evento 2: Festival Pop Brasil (5 atrações)
(4, 2), (5, 2), (12, 2), (16, 2), (21, 2),
-- Evento 3: Festival Sertanejo Raiz (5 atrações)
(6, 3), (8, 3), (9, 3), (10, 3), (7, 3),
-- Evento 4: Noite da Comédia (4 atrações)
(15, 4), (33, 4), (34, 4), (35, 4),
-- Evento 5: Festival Reggae Paz e Amor (2 atrações)
(27, 5), (28, 5),
-- Evento 6: Encontro Lendas da MPB (4 atrações)
(21, 6), (22, 6), (23, 6), (24, 6),
-- Evento 7: Festival Rap Nacional (4 atrações)
(29, 7), (30, 7), (31, 7), (32, 7),
-- Evento 8: Show Solo
(2, 8),
-- Evento 9: Show Solo
(6, 9),
-- Evento 10: Palestra (2 palestrantes)
(36, 10), (37, 10),
-- Evento 11: Tributo ao Rock Internacional (3 atrações)
(1, 11), (18, 11), (20, 11),
-- Evento 12: Show Solo
(11, 12),
-- Evento 13: Festival Kids (2 atrações)
(39, 13), (40, 13),
-- Evento 14: Show Solo
(24, 14),
-- Evento 15: Palestra Solo
(38, 15),
-- Evento 16: A Mágica do Circo (2 atrações)
(13, 16), (14, 16),
-- Evento 17: Concerto Solo
(17, 17),
-- Evento 18: Show Solo
(5, 18),
-- Evento 19: Tributo Solo
(7, 19),
-- Evento 20: Tributo (não é uma atração real, apenas um placeholder)
(20, 20);

-- =============================================
--  TABLE: tickets
-- =============================================
INSERT INTO tickets (id_ticket, numero, lote, id_cliente, id_evento) VALUES
(2001, 2026001, 'VIP', 1, 1), (2002, 2026002, 'VIP', 2, 1),
(2003, 2026003, 'INTEIRA', 3, 1), (2004, 2026004, 'PRE-VENDA', 4, 2),
(2005, 2026005, 'MEIA-ENTRADA', 5, 2), (2006, 2026006, 'INTEIRA', 6, 3),
(2007, 2026007, 'VIP', 7, 4), (2008, 2026008, 'INTEIRA', 8, 4),
(2009, 2026009, 'MEIA-ENTRADA', 9, 5), (2010, 2026010, 'PRE-VENDA', 10, 6),
(2011, 2026011, 'INTEIRA', 11, 6), (2012, 2026012, 'MEIA-ENTRADA', 12, 7),
(2013, 2026013, 'INTEIRA', 13, 7), (2014, 2026014, 'PRE-VENDA', 14, 8),
(2015, 2026015, 'MEIA-ENTRADA', 15, 9), (2016, 2026016, 'INTEIRA', 16, 10),
(2017, 2026017, 'INTEIRA', 17, 11), (2018, 2026018, 'MEIA-ENTRADA', 18, 11),
(2019, 2026019, 'INTEIRA', 19, 12), (2020, 2026020, 'MEIA-ENTRADA', 20, 13),
(2021, 2026021, 'PRE-VENDA', 21, 13), (2022, 2026022, 'VIP', 22, 14),
(2023, 2026023, 'INTEIRA', 23, 15), (2024, 2026024, 'INTEIRA', 24, 16),
(2025, 2026025, 'MEIA-ENTRADA', 25, 16), (2026, 2026026, 'PRE-VENDA', 26, 17),
(2027, 2026027, 'INTEIRA', 27, 18), (2028, 2026028, 'MEIA-ENTRADA', 28, 19),
(2029, 2026029, 'INTEIRA', 29, 20), (2030, 2026030, 'PRE-VENDA', 30, 1),
(2031, 2026031, 'MEIA-ENTRADA', 31, 2), (2032, 2026032, 'INTEIRA', 32, 3),
(2033, 2026033, 'INTEIRA', 33, 4), (2034, 2026034, 'PRE-VENDA', 34, 5),
(2035, 2026035, 'INTEIRA', 35, 6), (2036, 2026036, 'MEIA-ENTRADA', 36, 7),
(2037, 2026037, 'INTEIRA', 37, 8), (2038, 2026038, 'MEIA-ENTRADA', 38, 9),
(2039, 2026039, 'VIP', 39, 10), (2040, 2026040, 'INTEIRA', 40, 11);
