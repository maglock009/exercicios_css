from flask import render_template, request, redirect, url_for

from controllers.base_controller import BaseController

from database.connection import BancoMySQL

from repositories.usuario_repository import UsuarioRepository

from services.usuario_service import UsuarioService

from repositories.auditoria_repository import AuditoriaRepository

from services.auditoria_service import AuditoriaService

class UsuarioController (BaseController):

    def __init__ (self, app):

        self.rotas = [
            ('/usuarios', 'usuarios', self.listar, ['GET'],'administrador'),

            ('/usuarios/cadastrar', 'cadatrar_usuario', self.cadastrar, ['GET','POST'], 'administrador'),

            ('/usuarios/editar/<int:usuario_id>', 'editar_usuario', self.editar, ['GET', 'POST'], 'administrador'),

            ('/usuarios/excluir/<int:usuario_id>', 'excluir_usuario', self.excluir, ['POST'], 'administrador'),

            ('/usuarios/excluir/<int:usuario_id>', 'confirmar_exclusao_usuario', self.confirmar_exclusao, ['GET'], 'administrador'),

            ('/perfil', 'perfil', self.editar_perfil, ['GET', 'POST'], 'autenticado'),

        ]

        