from controllers.base_controller import BaseController


class HTMLBasicoController(BaseController):

    list_title = "Exercicios Flask"
    folder = "exercicios_flask"
    list_url = "/listas/exercicios-flask"

    exercicio_1_html = {
        "title": "Exercicio 1 Html",
        "template": "exercicios_flask/exercicio_1_html.html",
        "filename": "exercicio_1_html.html",
        "url": "/listas/exercicios-flask/exercicio-1-html",
    }
    exercicio_2_html = {
        "title": "Exercicio 2 Html",
        "template": "exercicios_flask/exercicio_2_html.html",
        "filename": "exercicio_2_html.html",
        "url": "/listas/exercicios-flask/exercicio-2-html",
    }
    exercicio_3_html = {
        "title": "Exercicio 3 Html",
        "template": "exercicios_flask/exercicio_3_html.html",
        "filename": "exercicio_3_html.html",
        "url": "/listas/exercicios-flask/exercicio-3-html",
    }
    exercicio_4_html = {
        "title": "Exercicio 4 Html",
        "template": "exercicios_flask/exercicio_4_html.html",
        "filename": "exercicio_4_html.html",
        "url": "/listas/exercicios-flask/exercicio-4-html",
    }

    exercises = [
        exercicio_1_html,
        exercicio_2_html,
        exercicio_3_html,
        exercicio_4_html,
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

    def redirecionar_exercicio_1(self):
        return self.redirecionar_para_exercicio(self.exercicio_1_html)

    def redirecionar_exercicio_2(self):
        return self.redirecionar_para_exercicio(self.exercicio_2_html)

    def redirecionar_exercicio_3(self):
        return self.redirecionar_para_exercicio(self.exercicio_3_html)

    def redirecionar_exercicio_4(self):
        return self.redirecionar_para_exercicio(self.exercicio_4_html)
