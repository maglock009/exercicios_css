from datetime import datetime
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from repositories.imagem_repository import ImagemRepository

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads" / "perfis"
EXTENSOES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
TIPOS_MIME_PERMITIDOS = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}
TAMANHO_MAXIMO_BYTES = 2 * 1024 * 1024


class ImagemService:
    def __init__(self, imagem_repository: ImagemRepository | None = None):
        self.imagens = imagem_repository or ImagemRepository()
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def url_publica(caminho: str | None) -> str | None:
        if not caminho:
            return None
        return f"/static/{caminho}"

    def buscar_por_id(self, imagem_id: int):
        return self.imagens.buscar_por_id(imagem_id)

    def salvar_upload(self, arquivo: FileStorage) -> int:
        if arquivo is None or not arquivo.filename:
            raise ValueError("Nenhum arquivo de imagem foi enviado.")

        nome_seguro = secure_filename(arquivo.filename)
        extensao = Path(nome_seguro).suffix.lower()
        if extensao not in EXTENSOES_PERMITIDAS:
            raise ValueError("Formato de imagem inválido. Use JPG, PNG, GIF ou WEBP.")

        conteudo = arquivo.read()
        if not conteudo:
            raise ValueError("O arquivo de imagem está vazio.")
        if len(conteudo) > TAMANHO_MAXIMO_BYTES:
            raise ValueError("A imagem deve ter no máximo 2 MB.")

        try:
            with Image.open(BytesIO(conteudo)) as imagem:
                imagem.verify()
                tipo_mime = Image.MIME.get(
                    imagem.format,
                    arquivo.mimetype or "application/octet-stream",
                )
        except Exception as exc:
            raise ValueError("Arquivo enviado não é uma imagem válida.") from exc

        if tipo_mime not in TIPOS_MIME_PERMITIDOS:
            raise ValueError("Formato de imagem inválido. Use JPG, PNG, GIF ou WEBP.")

        nome_armazenado = f"{uuid4().hex}{extensao}"
        caminho_relativo = f"uploads/perfis/{nome_armazenado}"
        destino = UPLOAD_DIR / nome_armazenado
        destino.write_bytes(conteudo)

        return self.imagens.criar(
            nome_original=nome_seguro,
            nome_armazenado=nome_armazenado,
            caminho=caminho_relativo,
            tipo_mime=tipo_mime,
            tamanho=len(conteudo),
            data_upload=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def excluir(self, imagem_id: int | None):
        if not imagem_id:
            return

        registro = self.imagens.buscar_por_id(imagem_id)
        if not registro:
            return

        arquivo = BASE_DIR / "static" / registro["caminho"]
        if arquivo.exists() and arquivo.is_file():
            arquivo.unlink()

        self.imagens.excluir(imagem_id)
