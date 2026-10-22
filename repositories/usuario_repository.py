from database.connection import BancoMySQL


class UsuarioRepository:
    def __init__(self, banco: BancoMySQL | None = None):
        self.banco = banco or BancoMySQL()

    def listar(self):
        return self.banco.buscar_todos(
            """
            SELECT
                u.id,
                u.email,
                u.data_nascimento,
                u.papel,
                u.imagem_perfil_id,
                i.caminho AS imagem_caminho
            FROM usuarios u
            LEFT JOIN imagens i ON i.id = u.imagem_perfil_id
            ORDER BY u.email
            """
        )

    def buscar_por_id(self, usuario_id: int):
        return self.banco.buscar_um(
            """
            SELECT
                u.id,
                u.email,
                u.senha_hash,
                u.data_nascimento,
                u.papel,
                u.imagem_perfil_id,
                i.caminho AS imagem_caminho
            FROM usuarios u
            LEFT JOIN imagens i ON i.id = u.imagem_perfil_id
            WHERE u.id = %s
            """,
            (usuario_id,),
        )

    def buscar_por_email(self, email: str):
        return self.banco.buscar_um(
            """
            SELECT
                u.id,
                u.email,
                u.senha_hash,
                u.data_nascimento,
                u.papel,
                u.imagem_perfil_id,
                i.caminho AS imagem_caminho
            FROM usuarios u
            LEFT JOIN imagens i ON i.id = u.imagem_perfil_id
            WHERE u.email = %s
            """,
            (email,),
        )

    def criar(self, email: str, senha_hash: str, data_nascimento: str, papel: str):
        cursor = self.banco.executar(
            """
            INSERT INTO usuarios (email, senha_hash, data_nascimento, papel)
            VALUES (%s, %s, %s, %s)
            """,
            (email, senha_hash, data_nascimento, papel),
        )
        return cursor.lastrowid

    def atualizar(self, usuario_id: int, email: str, data_nascimento: str, papel: str):
        self.banco.executar(
            """
            UPDATE usuarios
            SET email = %s, data_nascimento = %s, papel = %s
            WHERE id = %s
            """,
            (email, data_nascimento, papel, usuario_id),
        )

    def atualizar_perfil(self, usuario_id: int, email: str, data_nascimento: str):
        self.banco.executar(
            """
            UPDATE usuarios
            SET email = %s, data_nascimento = %s
            WHERE id = %s
            """,
            (email, data_nascimento, usuario_id),
        )

    def atualizar_senha(self, usuario_id: int, senha_hash: str):
        self.banco.executar(
            """
            UPDATE usuarios
            SET senha_hash = %s
            WHERE id = %s
            """,
            (senha_hash, usuario_id),
        )

    def atualizar_imagem_perfil(self, usuario_id: int, imagem_perfil_id: int | None):
        self.banco.executar(
            """
            UPDATE usuarios
            SET imagem_perfil_id = %s
            WHERE id = %s
            """,
            (imagem_perfil_id, usuario_id),
        )

    def excluir(self, usuario_id: int):
        self.banco.executar("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
