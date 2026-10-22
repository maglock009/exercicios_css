from flask import redirect, render_template, request, send_file, session, url_for

from controllers.base_controller import BaseController
from database.connection import BancoMySQL
from repositories.auditoria_repository import AuditoriaRepository
from repositories.imagem_repository import ImagemRepository
from repositories.usuario_repository import UsuarioRepository
from services.auditoria_service import AuditoriaService
from services.imagem_service import ImagemService
from services.usuario_service import UsuarioService


class UsuarioController(BaseController):
    def __init__(self, app, login_required=None):
        self.banco = BancoMySQL()
        self.usuario_repository = UsuarioRepository(self.banco)
        self.auditoria_repository = AuditoriaRepository(self.banco)
        self.imagem_repository = ImagemRepository(self.banco)
        self.imagem_service = ImagemService(self.imagem_repository)
        self.usuario_service = UsuarioService(
            self.usuario_repository,
            self.auditoria_repository,
            self.imagem_service,
        )
        self.auditoria_service = AuditoriaService(self.auditoria_repository)

        self.rotas = [
            ("/usuarios", "usuarios", self.listar, ["GET"], "administrador"),
            (
                "/usuarios/cadastrar",
                "cadastrar_usuario",
                self.cadastrar,
                ["GET", "POST"],
                "administrador",
            ),
            (
                "/usuarios/editar/<int:usuario_id>",
                "editar_usuario",
                self.editar,
                ["GET", "POST"],
                "administrador",
            ),
            (
                "/usuarios/excluir/<int:usuario_id>",
                "excluir_usuario",
                self.excluir,
                ["POST"],
                "administrador",
            ),
            (
                "/usuarios/excluir/<int:usuario_id>",
                "confirmar_exclusao_usuario",
                self.confirmar_exclusao,
                ["GET"],
                "administrador",
            ),
            (
                "/usuarios/relatorio",
                "relatorio_usuarios",
                self.relatorio,
                ["GET"],
                "administrador",
            ),
            ("/perfil", "perfil", self.editar_perfil, ["GET", "POST"], "autenticado"),
        ]
        super().__init__(app, login_required)

    def listar(self):
        usuarios = self.usuario_service.listar()
        return render_template(
            "html_usuarios/usuarios.html",
            usuarios=usuarios,
            formatar_data=self.usuario_service.formatar_data_br,
        )

    def cadastrar(self):
        erro = None
        if request.method == "POST":
            try:
                self.usuario_service.cadastrar(
                    email=request.form.get("email", "").strip(),
                    senha=request.form.get("senha", ""),
                    data_nascimento=request.form.get("data_nascimento", ""),
                    papel=request.form.get("papel", "usuario"),
                    autor_id=session.get("usuario_id"),
                )
                return redirect(url_for("usuarios"))
            except ValueError as exc:
                erro = str(exc)

        return render_template("html_usuarios/cadastrar_usuario.html", erro=erro)

    def editar(self, usuario_id):
        usuario = self.usuario_service.buscar_por_id(usuario_id)
        if not usuario:
            return redirect(url_for("usuarios"))

        erro = None
        if request.method == "POST":
            try:
                self.usuario_service.atualizar(
                    usuario_id=usuario_id,
                    email=request.form.get("email", "").strip(),
                    data_nascimento=request.form.get("data_nascimento", ""),
                    papel=request.form.get("papel", "usuario"),
                    autor_id=session.get("usuario_id"),
                )
                return redirect(url_for("usuarios"))
            except ValueError as exc:
                erro = str(exc)
                usuario = self.usuario_service.buscar_por_id(usuario_id)

        return render_template(
            "html_usuarios/editar.html",
            usuario=usuario,
            erro=erro,
        )

    def confirmar_exclusao(self, usuario_id):
        usuario = self.usuario_service.buscar_por_id(usuario_id)
        if not usuario:
            return redirect(url_for("usuarios"))
        return render_template(
            "html_usuarios/confirmar_exclusao.html",
            usuario=usuario,
        )

    def excluir(self, usuario_id):
        try:
            self.usuario_service.excluir(
                usuario_id=usuario_id,
                autor_id=session.get("usuario_id"),
            )
        except ValueError:
            pass
        return redirect(url_for("usuarios"))

    def editar_perfil(self):
        usuario_id = session.get("usuario_id")
        usuario = self.usuario_service.buscar_por_id(usuario_id)
        if not usuario:
            return redirect(url_for("login"))

        erro = None
        sucesso = None
        if request.method == "POST":
            try:
                nova_senha = request.form.get("senha", "").strip() or None
                remover_imagem = request.form.get("remover_imagem") == "1"
                self.usuario_service.atualizar_perfil(
                    usuario_id=usuario_id,
                    email=request.form.get("email", "").strip(),
                    data_nascimento=request.form.get("data_nascimento", ""),
                    nova_senha=nova_senha,
                    arquivo_imagem=request.files.get("imagem_perfil"),
                    remover_imagem=remover_imagem,
                )
                session["username"] = request.form.get("email", "").strip()
                usuario = self.usuario_service.buscar_por_id(usuario_id)
                session["imagem_perfil"] = ImagemService.url_publica(
                    usuario.get("imagem_caminho")
                )
                sucesso = "Perfil atualizado com sucesso."
            except ValueError as exc:
                erro = str(exc)
                usuario = self.usuario_service.buscar_por_id(usuario_id)

        return render_template(
            "html_usuarios/editar_perfil.html",
            usuario=usuario,
            imagem_url=ImagemService.url_publica(usuario.get("imagem_caminho")),
            erro=erro,
            sucesso=sucesso,
        )

    def relatorio(self):
        buffer = self.usuario_service.gerar_relatorio_excel()
        return send_file(
            buffer,
            as_attachment=True,
            download_name="relatorio_usuarios.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
