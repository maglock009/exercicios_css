from datetime import datetime, timedelta

import bcrypt

from database.connection import BancoMySQL


DDL_USUARIOS = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    papel ENUM('administrador', 'usuario') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

DDL_AUDITORIA = """
CREATE TABLE IF NOT EXISTS auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entidade_id INT NOT NULL,
    acao VARCHAR(100) NOT NULL,
    detalhes TEXT NULL,
    data_evento DATETIME NOT NULL,
    CONSTRAINT fk_auditoria_usuario
        FOREIGN KEY (entidade_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

DDL_IMAGENS = """
CREATE TABLE IF NOT EXISTS imagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_original VARCHAR(255) NOT NULL,
    nome_armazenado VARCHAR(255) NOT NULL,
    caminho VARCHAR(500) NOT NULL,
    tipo_mime VARCHAR(100) NOT NULL,
    tamanho INT NOT NULL,
    data_upload DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""


def _hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _garantir_coluna_imagem_perfil(cursor, conexao):
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'usuarios'
          AND COLUMN_NAME = 'imagem_perfil_id'
        """
    )
    if cursor.fetchone()["total"]:
        return

    cursor.execute(
        """
        ALTER TABLE usuarios
        ADD COLUMN imagem_perfil_id INT NULL,
        ADD CONSTRAINT fk_usuarios_imagem_perfil
            FOREIGN KEY (imagem_perfil_id) REFERENCES imagens(id)
            ON DELETE SET NULL
        """
    )
    conexao.commit()


def inicializar_banco():
    banco = BancoMySQL()
    banco.garantir_banco()

    conexao = banco.conectar()
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(DDL_USUARIOS)
        cursor.execute(DDL_AUDITORIA)
        cursor.execute(DDL_IMAGENS)
        conexao.commit()
        _garantir_coluna_imagem_perfil(cursor, conexao)

        cursor.execute("SELECT id FROM usuarios WHERE email = %s", ("Miguel",))
        existente = cursor.fetchone()
        if existente:
            return

        senha_admin = _hash_senha("12345")
        senha_padrao = _hash_senha("senha123")

        usuarios_seed = [
            ("Miguel", senha_admin, "1990-05-12", "administrador"),
            ("ana@exemplo.com", senha_padrao, "1995-03-21", "usuario"),
            ("bruno@exemplo.com", senha_padrao, "1988-11-08", "usuario"),
            ("carla@exemplo.com", senha_padrao, "2001-07-30", "usuario"),
        ]

        cursor.executemany(
            """
            INSERT INTO usuarios (email, senha_hash, data_nascimento, papel)
            VALUES (%s, %s, %s, %s)
            """,
            usuarios_seed,
        )
        conexao.commit()

        cursor.execute("SELECT id FROM usuarios ORDER BY id")
        ids = [row["id"] for row in cursor.fetchall()]

        agora = datetime.now()
        registros = [
            (ids[0], "LOGIN", "Acesso ao sistema", agora - timedelta(days=2)),
            (ids[1], "CADASTRO", "Usuário criado pelo administrador", agora - timedelta(days=1)),
            (ids[2], "EDICAO", "Atualização de perfil", agora - timedelta(hours=5)),
            (ids[3], "LOGIN", "Primeiro acesso", agora),
            (ids[0], "EXPORTACAO", "Consulta de auditoria", agora),
        ]
        cursor.executemany(
            """
            INSERT INTO auditoria (entidade_id, acao, detalhes, data_evento)
            VALUES (%s, %s, %s, %s)
            """,
            registros,
        )
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()
