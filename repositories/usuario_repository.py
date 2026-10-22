from database.connection import BancoMySQL


class UsuarioRepository:
    def __init__(self, banco: BancoMySQL | None = None):
        self.banco = banco or BancoMySQL()

    def listar(self):
        return self.banco.buscar_todos(
            """
            SELECT id, email, data_nascimento, papel
            FROM usuarios
            ORDER BY email
            """
        )

    def buscar_por_id(self, usuario_id: int):
        return self.banco.buscar_um(
            """
            SELECT id, email, senha_hash, data_nascimento, papel
            FROM usuarios
            WHERE id = %s
            """,
            (usuario_id,),
        )

    def buscar_por_email(self, email: str):
        return self.banco.buscar_um(
            """
            SELECT id, email, senha_hash, data_nascimento, papel
            FROM usuarios
            WHERE email = %s
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

    def excluir(self, usuario_id: int):
        self.banco.executar("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
