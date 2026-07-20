from functools import wraps
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, send_from_directory, session, url_for
from jinja2 import ChoiceLoader, FileSystemLoader, PrefixLoader

from exercise_data import find_exercise_by_target, get_exercise, get_list, load_exercise_modules

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
    return {"exercise_lists": load_exercise_modules(BASE_DIR)}


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


@app.route("/listas/<list_slug>")
@login_required
def exercise_list(list_slug):
    selected_list = get_list(list_slug, BASE_DIR)
    if selected_list is None:
        abort(404)

    return render_template("module_overview.html", selected_list=selected_list)


@app.route("/listas/<list_slug>/<path:exercise_slug>")
@login_required
def exercise_detail(list_slug, exercise_slug):
    selected_list = get_list(list_slug, BASE_DIR)
    selected_exercise = get_exercise(list_slug, exercise_slug, BASE_DIR)
    if selected_list is None or selected_exercise is None:
        abort(404)

    exercises = selected_list["exercises"]
    selected_index = exercises.index(selected_exercise)
    next_exercise = (
        exercises[selected_index + 1]
        if selected_index + 1 < len(exercises)
        else None
    )

    return render_template(
        selected_exercise.get("template", "exercise_detail.html"),
        selected_list=selected_list,
        selected_exercise=selected_exercise,
        next_exercise=next_exercise,
    )


@app.route("/sair")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/exercicios-flask/static/<path:filename>")
@login_required
def flask_static(filename):
    return send_from_directory(BASE_DIR / "exercicios_flask" / "static", filename)


@app.route("/<path:exercise_target>")
@login_required
def legacy_exercise_link(exercise_target):
    selected_list, selected_exercise = find_exercise_by_target(exercise_target, BASE_DIR)
    if selected_list is None or selected_exercise is None:
        abort(404)

    return redirect(
        url_for(
            "exercise_detail",
            list_slug=selected_list["slug"],
            exercise_slug=selected_exercise["slug"],
        )
    )


if __name__ == "__main__":
    app.run(debug=True)