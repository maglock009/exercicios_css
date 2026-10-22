from functools import wraps

from flask import abort, redirect, render_template, session, url_for


class BaseController:
    def __init__(self, app, login_required=None):
        self.app = app
        self.login_required = login_required
        if hasattr(self, "exercises"):
            self.selected_list = self._build_selected_list()
        if hasattr(self, "rotas"):
            self.registrar_rotas()

    def registrar_rotas(self):
        for rota in self.rotas:
            if len(rota) == 3:
                endereco_url, nome_rota, funcao_resposta = rota
                methods = None
                papel = None
            elif len(rota) == 5:
                endereco_url, nome_rota, funcao_resposta, methods, papel = rota
            else:
                raise ValueError(f"Rota inválida: {rota}")

            view = funcao_resposta
            if papel:
                view = self._proteger(view, papel)
            elif self.login_required:
                view = self.login_required(view)

            kwargs = {"endpoint": nome_rota, "view_func": view}
            if methods is not None:
                kwargs["methods"] = methods
            self.app.add_url_rule(endereco_url, **kwargs)

    def _proteger(self, view, papel):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("is_authenticated"):
                return redirect(url_for("login"))
            if papel == "administrador" and session.get("papel") != "administrador":
                abort(403)
            return view(*args, **kwargs)

        return wrapped

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
