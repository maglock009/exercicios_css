from controllers.base_controller import BaseController


class FormulariosController(BaseController):

    list_slug = "exercicios-formularios"
    list_title = "Exercicios Formularios"
    folder = "exercicios_formularios"
    exercises = [
        {
            "slug": "cadastro-simples",
            "title": "Cadastro Simples",
            "template": "exercicios_formularios/cadastro_simples.html",
            "filename": "cadastro_simples.html",
        },
        {
            "slug": "preferencias",
            "title": "Preferencias",
            "template": "exercicios_formularios/preferencias.html",
            "filename": "preferencias.html",
        },
    ]

    def __init__(self, app, login_required):
        self.rotas = [
            (
                "/listas/exercicios-formularios",
                "exercicios_formularios_lista",
                self.lista,
            ),
            (
                "/listas/exercicios-formularios/cadastro-simples",
                "exercicios_formularios_cadastro_simples",
                self.cadastro_simples,
            ),
            (
                "/listas/exercicios-formularios/preferencias",
                "exercicios_formularios_preferencias",
                self.preferencias,
            ),
            (
                "/cadastro_simples",
                "legacy_cadastro_simples",
                self.legacy_cadastro_simples,
            ),
            (
                "/cadastro-simples",
                "legacy_cadastro_simples_hifen",
                self.legacy_cadastro_simples,
            ),
            ("/preferencias", "legacy_preferencias", self.legacy_preferencias),
        ]

        super().__init__(app, login_required)

    def lista(self):
        return self.renderizar_lista()

    def cadastro_simples(self):
        return self.renderizar_exercicio("cadastro-simples")

    def preferencias(self):
        return self.renderizar_exercicio("preferencias")

    def legacy_cadastro_simples(self):
        return self.redirecionar_para_exercicio("cadastro-simples")

    def legacy_preferencias(self):
        return self.redirecionar_para_exercicio("preferencias")
