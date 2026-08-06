from controllers.base_controller import BaseController


class HTMLBasicoController(BaseController):

    list_title = "Exercicios Flask"
    folder = "templates"
    list_url = "/listas/exercicios-flask"

    exercicio_1_html = {
        "title": "Exercicio 1 Html",
        "template": "exercicio_1_html.html",
        "filename": "exercicio_1_html.html",
        "url": "/listas/exercicios-flask/exercicio-1-html",
    }
    exercicio_2_html = {
        "title": "Exercicio 2 Html",
        "template": "exercicio_2_html.html",
        "filename": "exercicio_2_html.html",
        "url": "/listas/exercicios-flask/exercicio-2-html",
    }
    exercicio_3_html = {
        "title": "Exercicio 3 Html",
        "template": "exercicio_3_html.html",
        "filename": "exercicio_3_html.html",
        "url": "/listas/exercicios-flask/exercicio-3-html",
    }
    exercicio_4_html = {
        "title": "Exercicio 4 Html",
        "template": "exercicio_4_html.html",
        "filename": "exercicio_4_html.html",
        "url": "/listas/exercicios-flask/exercicio-4-html",
    }
    pagina_divs_spans = {
        "title": "Divs e Spans",
        "template": "divs_spans.html",
        "filename": "divs_spans.html",
        "url": "/listas/exercicios-flask/divs-spans",
    }
    pagina_listas = {
        "title": "Listas",
        "template": "listas.html",
        "filename": "listas.html",
        "url": "/listas/exercicios-flask/listas",
    }
    pagina_tabelas = {
        "title": "Tabelas",
        "template": "tabelas.html",
        "filename": "tabelas.html",
        "url": "/listas/exercicios-flask/tabelas",
    }

    exercises = [
        exercicio_1_html,
        exercicio_2_html,
        exercicio_3_html,
        exercicio_4_html,
        pagina_divs_spans,
        pagina_listas,
        pagina_tabelas,
    ]

    def __init__(self, app, login_required):
        self.rotas = [
            ("/listas/exercicios-flask", "exercicios_flask_lista", self.lista),
            (
                "/listas/exercicios-flask/exercicio-1-html",
                "exercicios_flask_exercicio_1",
                self.exercicio_1,
            ),
            (
                "/listas/exercicios-flask/exercicio-2-html",
                "exercicios_flask_exercicio_2",
                self.exercicio_2,
            ),
            (
                "/listas/exercicios-flask/exercicio-3-html",
                "exercicios_flask_exercicio_3",
                self.exercicio_3,
            ),
            (
                "/listas/exercicios-flask/exercicio-4-html",
                "exercicios_flask_exercicio_4",
                self.exercicio_4,
            ),
            (
                "/listas/exercicios-flask/divs-spans",
                "exercicios_flask_divs_spans",
                self.divs_spans,
            ),
            (
                "/listas/exercicios-flask/listas",
                "exercicios_flask_listas",
                self.listas,
            ),
            (
                "/listas/exercicios-flask/tabelas",
                "exercicios_flask_tabelas",
                self.tabelas,
            ),
            (
                "/exercicio_1",
                "redirecionar_exercicio_1",
                self.redirecionar_exercicio_1,
            ),
            (
                "/exercicio_1_html",
                "redirecionar_exercicio_1_html",
                self.redirecionar_exercicio_1,
            ),
            (
                "/exercicio_2",
                "redirecionar_exercicio_2",
                self.redirecionar_exercicio_2,
            ),
            (
                "/exercicio_2_html",
                "redirecionar_exercicio_2_html",
                self.redirecionar_exercicio_2,
            ),
            (
                "/exercicio_3",
                "redirecionar_exercicio_3",
                self.redirecionar_exercicio_3,
            ),
            (
                "/exercicio_3_html",
                "redirecionar_exercicio_3_html",
                self.redirecionar_exercicio_3,
            ),
            (
                "/exercicio_4",
                "redirecionar_exercicio_4",
                self.redirecionar_exercicio_4,
            ),
            (
                "/exercicio_4_html",
                "redirecionar_exercicio_4_html",
                self.redirecionar_exercicio_4,
            ),
            (
                "/divs-spans",
                "redirecionar_divs_spans",
                self.redirecionar_divs_spans,
            ),
            (
                "/listas-html",
                "redirecionar_listas",
                self.redirecionar_listas,
            ),
            (
                "/tabelas",
                "redirecionar_tabelas",
                self.redirecionar_tabelas,
            ),
        ]

        super().__init__(app, login_required)

    def lista(self):
        return self.renderizar_lista()

    def exercicio_1(self):
        return self.renderizar_exercicio(self.exercicio_1_html)

    def exercicio_2(self):
        return self.renderizar_exercicio(self.exercicio_2_html)

    def exercicio_3(self):
        return self.renderizar_exercicio(self.exercicio_3_html)

    def exercicio_4(self):
        return self.renderizar_exercicio(self.exercicio_4_html)

    def divs_spans(self):
        return self.renderizar_exercicio(self.pagina_divs_spans)

    def listas(self):
        return self.renderizar_exercicio(self.pagina_listas)

    def tabelas(self):
        return self.renderizar_exercicio(self.pagina_tabelas)

    def redirecionar_exercicio_1(self):
        return self.redirecionar_para_exercicio(self.exercicio_1_html)

    def redirecionar_exercicio_2(self):
        return self.redirecionar_para_exercicio(self.exercicio_2_html)

    def redirecionar_exercicio_3(self):
        return self.redirecionar_para_exercicio(self.exercicio_3_html)

    def redirecionar_exercicio_4(self):
        return self.redirecionar_para_exercicio(self.exercicio_4_html)

    def redirecionar_divs_spans(self):
        return self.redirecionar_para_exercicio(self.pagina_divs_spans)

    def redirecionar_listas(self):
        return self.redirecionar_para_exercicio(self.pagina_listas)

    def redirecionar_tabelas(self):
        return self.redirecionar_para_exercicio(self.pagina_tabelas)
