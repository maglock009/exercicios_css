from flask import abort, redirect, render_template


class BaseController:
    def __init__(self, app, login_required):
        self.app = app
        self.login_required = login_required
        self.selected_list = self._build_selected_list()
        self.registrar_rotas()

    def registrar_rotas(self):
        for endereco_url, nome_rota, funcao_resposta in self.rotas:
            self.app.add_url_rule(
                endereco_url,
                nome_rota,
                self.login_required(funcao_resposta),
            )

    def _build_selected_list(self):
        return {
            "title": self.list_title,
            "folder": self.folder,
            "url": self.list_url,
            "exercises": self.exercises,
        }

    def renderizar_lista(self):
        return render_template("module_overview.html", selected_list=self.selected_list)

    def renderizar_exercicio(self, selected_exercise):
        if selected_exercise not in self.exercises:
            abort(404)

        exercises = self.selected_list["exercises"]
        selected_index = exercises.index(selected_exercise)
        next_exercise = (
            exercises[selected_index + 1]
            if selected_index + 1 < len(exercises)
            else None
        )

        return render_template(
            selected_exercise["template"],
            selected_list=self.selected_list,
            selected_exercise=selected_exercise,
            next_exercise=next_exercise,
        )

    def redirecionar_para_exercicio(self, selected_exercise):
        if selected_exercise not in self.exercises:
            abort(404)

        return redirect(selected_exercise["url"])
