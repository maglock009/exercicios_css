from functools import wraps
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
from jinja2 import ChoiceLoader, FileSystemLoader, PrefixLoader

from exercicios_flask.controllers.html_basico_controller import HTMLBasicoController
from exercicios_formularios.controllers.formularios_controller import FormulariosController

DEFAULT_USER = "Miguel"
DEFAULT_PASSWORD = "12345"
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"
app.jinja_loader = ChoiceLoader(
    [
        app.jinja_loader,
        PrefixLoader(
            {
                "exercicios_flask": FileSystemLoader(
                    str(BASE_DIR / "exercicios_flask" / "templates")
                ),
                "exercicios_formularios": FileSystemLoader(
                    str(BASE_DIR / "exercicios_formularios" / "templates")
                ),
            }
        ),
    ]
)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("is_authenticated"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.context_processor
def inject_sidebar_data():
    return {
        "exercise_lists": [
            controller.selected_list for controller in exercise_controllers
        ]
    }


@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("is_authenticated"):
        return redirect(url_for("home"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == DEFAULT_USER and password == DEFAULT_PASSWORD:
            session["is_authenticated"] = True
            session["username"] = username
            return redirect(url_for("home"))

        error = "Usuario ou senha invalidos."

    return render_template("login.html", error=error)


@app.route("/inicio")
@login_required
def home():
    return render_template("home.html")


@app.route("/sair")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/exercicios-flask/static/<path:filename>")
@login_required
def flask_static(filename):
    return send_from_directory(BASE_DIR / "exercicios_flask" / "static", filename)


exercise_controllers = [
    FormulariosController(app, login_required),
    HTMLBasicoController(app, login_required),
]


if __name__ == "__main__":
    app.run(debug=True)