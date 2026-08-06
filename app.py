from functools import wraps
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

from controllers.formularios_controller import FormulariosController
from controllers.html_basico_controller import HTMLBasicoController

DEFAULT_USER = "Miguel"
DEFAULT_PASSWORD = "12345"
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = "123456"


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


exercise_controllers = [
    FormulariosController(app, login_required),
    HTMLBasicoController(app, login_required),
]


if __name__ == "__main__":
    app.run(debug=True)
