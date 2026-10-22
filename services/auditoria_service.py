from datetime import datetime
from io import BytesIO

from openpyxl import Workbook

from repositories.auditoria_repository import AuditoriaRepository
from services.usuario_service import UsuarioService


class AuditoriaService:
    def __init__(self, auditoria_repository: AuditoriaRepository | None = None):
        self.auditoria = auditoria_repository or AuditoriaRepository()

    def listar(self):
        return self.auditoria.listar_com_email()

    def gerar_relatorio_excel(self) -> BytesIO:
        workbook = Workbook()
        planilha = workbook.active
        planilha.title = "Auditoria"

        cabecalhos = ["entidade_ID", "acao", "detalhes", "data_evento"]
        for coluna, titulo in enumerate(cabecalhos, start=1):
            planilha.cell(row=1, column=coluna, value=titulo)

        for linha, registro in enumerate(self.listar(), start=2):
            planilha.cell(row=linha, column=1, value=registro["entidade_email"])
            planilha.cell(row=linha, column=2, value=registro["acao"])
            planilha.cell(row=linha, column=3, value=registro["detalhes"] or "")
            planilha.cell(
                row=linha,
                column=4,
                value=UsuarioService.formatar_data_br(registro["data_evento"]),
            )

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)
        return buffer

    def registrar(self, entidade_id: int, acao: str, detalhes: str = ""):
        return self.auditoria.registrar(
            entidade_id,
            acao,
            detalhes,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
