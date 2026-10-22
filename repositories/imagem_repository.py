from database.connection import BancoMySQL


class ImagemRepository:
    def __init__(self, banco: BancoMySQL | None = None):
        self.banco = banco or BancoMySQL()

    def buscar_por_id(self, imagem_id: int):
        return self.banco.buscar_um(
            """
            SELECT id, nome_original, nome_armazenado, caminho, tipo_mime, tamanho, data_upload
            FROM imagens
            WHERE id = %s
            """,
            (imagem_id,),
        )

    def criar(
        self,
        nome_original: str,
        nome_armazenado: str,
        caminho: str,
        tipo_mime: str,
        tamanho: int,
        data_upload: str,
    ):
        cursor = self.banco.executar(
            """
            INSERT INTO imagens (
                nome_original, nome_armazenado, caminho, tipo_mime, tamanho, data_upload
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nome_original, nome_armazenado, caminho, tipo_mime, tamanho, data_upload),
        )
        return cursor.lastrowid

    def excluir(self, imagem_id: int):
        self.banco.executar("DELETE FROM imagens WHERE id = %s", (imagem_id,))
