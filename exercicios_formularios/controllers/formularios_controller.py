from controllers.base_controller import BaseController


class FormulariosController(BaseController):

    list_title = "Exercicios Formularios"
    folder = "exercicios_formularios"
    list_url = "/listas/exercicios-formularios"

    pagina_cadastro_simples = {
        "title": "Cadastro Simples",
        "template": "exercicios_formularios/cadastro_simples.html",
        "filename": "cadastro_simples.html",
        "url": "/listas/exercicios-formularios/cadastro-simples",
    }
    pagina_preferencias = {
        "title": "Preferencias",
        "template": "exercicios_formularios/preferencias.html",
        "filename": "preferencias.html",
        "url": "/listas/exercicios-formularios/preferencias",
    }

    exercises = [
        pagina_cadastro_simples,
        pagina_preferencias,
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
                "redirecionar_cadastro_simples",
                self.redirecionar_cadastro_simples,
            ),
            (
                "/cadastro-simples",
                "redirecionar_cadastro_simples_hifen",
                self.redirecionar_cadastro_simples,
            ),
            (
                "/preferencias",
                "redirecionar_preferencias",
                self.redirecionar_preferencias,
            ),
        ]

        super().__init__(app, login_required)

    def lista(self):
        return self.renderizar_lista()

    def cadastro_simples(self):
        return self.renderizar_exercicio(self.pagina_cadastro_simples)

    def preferencias(self):
        return self.renderizar_exercicio(self.pagina_preferencias)

    def redirecionar_cadastro_simples(self):
        return self.redirecionar_para_exercicio(self.pagina_cadastro_simples)

    def redirecionar_preferencias(self):
        return self.redirecionar_para_exercicio(self.pagina_preferencias)
