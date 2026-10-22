from flask import render_template, send_file

from controllers.base_controller import BaseController
from database.connection import BancoMySQL
from repositories.auditoria_repository import AuditoriaRepository
from services.auditoria_service import AuditoriaService
from services.usuario_service import UsuarioService


class AuditoriaController(BaseController):
    def __init__(self, app, login_required=None):
        self.banco = BancoMySQL()
        self.auditoria_service = AuditoriaService(AuditoriaRepository(self.banco))

        self.rotas = [
            ("/auditoria", "auditoria", self.listar, ["GET"], "administrador"),
            (
                "/auditoria/relatorio",
                "relatorio_auditoria",
                self.relatorio,
                ["GET"],
                "administrador",
            ),
        ]
        super().__init__(app, login_required)

    def listar(self):
        registros = self.auditoria_service.listar()
        return render_template(
            "html_auditoria/auditoria.html",
            registros=registros,
            formatar_data=UsuarioService.formatar_data_br,
        )

    def relatorio(self):
        buffer = self.auditoria_service.gerar_relatorio_excel()
        return send_file(
            buffer,
            as_attachment=True,
            download_name="relatorio_auditoria.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
