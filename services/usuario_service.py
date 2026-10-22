import re
from datetime import date, datetime
from io import BytesIO

import bcrypt
from email_validator import EmailNotValidError, validate_email
from openpyxl import Workbook

from repositories.auditoria_repository import AuditoriaRepository
from repositories.usuario_repository import UsuarioRepository
from services.imagem_service import ImagemService

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SENHA_MAIUSCULA = re.compile(r"[A-Z]")
SENHA_NUMERO = re.compile(r"\d")


class UsuarioService:
    def __init__(
        self,
        usuario_repository: UsuarioRepository | None = None,
        auditoria_repository: AuditoriaRepository | None = None,
        imagem_service: ImagemService | None = None,
    ):
        self.usuarios = usuario_repository or UsuarioRepository()
        self.auditoria = auditoria_repository or AuditoriaRepository()
        self.imagens = imagem_service or ImagemService()

    @staticmethod
    def _hash_senha(senha: str) -> str:
        return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verificar_senha(senha: str, senha_hash: str) -> bool:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))

    @staticmethod
    def validar_email(email: str) -> str:
        email_limpo = (email or "").strip()
        if not email_limpo:
            raise ValueError("O e-mail é obrigatório.")
        if not EMAIL_REGEX.match(email_limpo):
            raise ValueError("Informe um e-mail em formato válido.")
        try:
            resultado = validate_email(email_limpo, check_deliverability=False)
        except EmailNotValidError as exc:
            raise ValueError("Informe um e-mail em formato válido.") from exc
        return resultado.normalized

    @staticmethod
    def validar_data_nascimento(data_nascimento: str) -> str:
        texto = (data_nascimento or "").strip()
        if not texto:
            raise ValueError("A data de nascimento é obrigatória.")
        try:
            nascimento = datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError("Informe uma data de nascimento válida.") from exc

        hoje = date.today()
        if nascimento > hoje:
            raise ValueError("A data de nascimento não pode ser futura.")

        idade = (
            hoje.year
            - nascimento.year
            - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        )
        if idade < 18:
            raise ValueError("O usuário deve ter 18 anos ou mais.")
        return texto

    @staticmethod
    def validar_senha(senha: str) -> str:
        if not senha:
            raise ValueError("A senha é obrigatória.")
        if not SENHA_MAIUSCULA.search(senha) or not SENHA_NUMERO.search(senha):
            raise ValueError(
                "A senha deve conter ao menos uma letra maiúscula e um número."
            )
        return senha

    @staticmethod
    def formatar_data_br(valor) -> str:
        if valor is None or valor == "":
            return ""
        if isinstance(valor, str):
            texto = valor.strip()
            for formato in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    return datetime.strptime(texto[:19], formato).strftime("%d/%m/%Y")
                except ValueError:
                    continue
            if len(texto) == 10 and texto[2] == "/" and texto[5] == "/":
                return texto
            return texto
        if hasattr(valor, "strftime"):
            return valor.strftime("%d/%m/%Y")
        return str(valor)

    def autenticar(self, email: str, senha: str):
        usuario = self.usuarios.buscar_por_email(email)
        if not usuario:
            return None
        if not self.verificar_senha(senha, usuario["senha_hash"]):
            return None
        self.auditoria.registrar(
            usuario["id"],
            "LOGIN",
            "Acesso ao sistema",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return usuario

    def listar(self):
        return self.usuarios.listar()

    def buscar_por_id(self, usuario_id: int):
        return self.usuarios.buscar_por_id(usuario_id)

    def cadastrar(self, email: str, senha: str, data_nascimento: str, papel: str, autor_id: int | None = None):
        email = self.validar_email(email)
        senha = self.validar_senha(senha)
        data_nascimento = self.validar_data_nascimento(data_nascimento)

        existente = self.usuarios.buscar_por_email(email)
        if existente:
            raise ValueError("Já existe um usuário com este e-mail.")

        usuario_id = self.usuarios.criar(
            email=email,
            senha_hash=self._hash_senha(senha),
            data_nascimento=data_nascimento,
            papel=papel,
        )
        if autor_id:
            self.auditoria.registrar(
                autor_id,
                "CADASTRO",
                f"Usuário {email} criado",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        return usuario_id

    def _atualizar_imagem_perfil(
        self,
        usuario_id: int,
        imagem_anterior_id: int | None,
        arquivo_imagem=None,
        remover_imagem: bool = False,
    ):
        if arquivo_imagem is not None and getattr(arquivo_imagem, "filename", None):
            nova_imagem_id = self.imagens.salvar_upload(arquivo_imagem)
            self.usuarios.atualizar_imagem_perfil(usuario_id, nova_imagem_id)
            if imagem_anterior_id and imagem_anterior_id != nova_imagem_id:
                self.imagens.excluir(imagem_anterior_id)
        elif remover_imagem and imagem_anterior_id:
            self.usuarios.atualizar_imagem_perfil(usuario_id, None)
            self.imagens.excluir(imagem_anterior_id)

    def atualizar(
        self,
        usuario_id: int,
        email: str,
        data_nascimento: str,
        papel: str,
        autor_id: int | None = None,
        arquivo_imagem=None,
        remover_imagem: bool = False,
    ):
        email = self.validar_email(email)
        data_nascimento = self.validar_data_nascimento(data_nascimento)

        atual = self.usuarios.buscar_por_id(usuario_id)
        if not atual:
            raise ValueError("Usuário não encontrado.")

        outro = self.usuarios.buscar_por_email(email)
        if outro and outro["id"] != usuario_id:
            raise ValueError("Já existe um usuário com este e-mail.")

        self.usuarios.atualizar(usuario_id, email, data_nascimento, papel)
        self._atualizar_imagem_perfil(
            usuario_id=usuario_id,
            imagem_anterior_id=atual.get("imagem_perfil_id"),
            arquivo_imagem=arquivo_imagem,
            remover_imagem=remover_imagem,
        )
        if autor_id:
            self.auditoria.registrar(
                autor_id,
                "EDICAO",
                f"Usuário {email} atualizado",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

    def atualizar_perfil(
        self,
        usuario_id: int,
        email: str,
        data_nascimento: str,
        nova_senha: str | None = None,
        arquivo_imagem=None,
        remover_imagem: bool = False,
    ):
        email = self.validar_email(email)
        data_nascimento = self.validar_data_nascimento(data_nascimento)
        if nova_senha:
            nova_senha = self.validar_senha(nova_senha)

        atual = self.usuarios.buscar_por_id(usuario_id)
        if not atual:
            raise ValueError("Usuário não encontrado.")

        outro = self.usuarios.buscar_por_email(email)
        if outro and outro["id"] != usuario_id:
            raise ValueError("Já existe um usuário com este e-mail.")

        self.usuarios.atualizar_perfil(usuario_id, email, data_nascimento)
        if nova_senha:
            self.usuarios.atualizar_senha(usuario_id, self._hash_senha(nova_senha))

        self._atualizar_imagem_perfil(
            usuario_id=usuario_id,
            imagem_anterior_id=atual.get("imagem_perfil_id"),
            arquivo_imagem=arquivo_imagem,
            remover_imagem=remover_imagem,
        )

        self.auditoria.registrar(
            usuario_id,
            "EDICAO",
            "Perfil atualizado",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def excluir(self, usuario_id: int, autor_id: int | None = None):
        atual = self.usuarios.buscar_por_id(usuario_id)
        if not atual:
            raise ValueError("Usuário não encontrado.")
        if autor_id and autor_id == usuario_id:
            raise ValueError("Não é possível excluir o próprio usuário.")

        email = atual["email"]
        imagem_perfil_id = atual.get("imagem_perfil_id")
        self.usuarios.atualizar_imagem_perfil(usuario_id, None)
        self.usuarios.excluir(usuario_id)
        if imagem_perfil_id:
            self.imagens.excluir(imagem_perfil_id)
        if autor_id:
            self.auditoria.registrar(
                autor_id,
                "EXCLUSAO",
                f"Usuário {email} excluído",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

    def gerar_relatorio_excel(self) -> BytesIO:
        workbook = Workbook()
        planilha = workbook.active
        planilha.title = "Usuarios"

        planilha["A1"] = "Relatórios de usuários"
        planilha["A3"] = "e-mail"
        planilha["B3"] = "data de nascimento"

        for indice, usuario in enumerate(self.usuarios.listar(), start=4):
            planilha.cell(row=indice, column=1, value=usuario["email"])
            planilha.cell(
                row=indice,
                column=2,
                value=self.formatar_data_br(usuario["data_nascimento"]),
            )

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)
        return buffer
