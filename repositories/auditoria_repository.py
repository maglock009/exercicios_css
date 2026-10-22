from database.connection import BancoMySQL


class AuditoriaRepository:
    def __init__(self, banco: BancoMySQL | None = None):
        self.banco = banco or BancoMySQL()

    def listar_com_email(self):
        return self.banco.buscar_todos(
            """
            SELECT
                a.id,
                a.entidade_id,
                u.email AS entidade_email,
                a.acao,
                a.detalhes,
                a.data_evento
            FROM auditoria a
            INNER JOIN usuarios u ON u.id = a.entidade_id
            ORDER BY a.data_evento DESC, a.id DESC
            """
        )

    def registrar(self, entidade_id: int, acao: str, detalhes: str, data_evento: str):
        cursor = self.banco.executar(
            """
            INSERT INTO auditoria (entidade_id, acao, detalhes, data_evento)
            VALUES (%s, %s, %s, %s)
            """,
            (entidade_id, acao, detalhes, data_evento),
        )
        return cursor.lastrowid
