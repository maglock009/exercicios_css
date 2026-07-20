import unicodedata
from pathlib import Path


MODULE_DIRECTORIES = [
    {
        "slug": "exercicios-formularios",
        "title": "Exercicios Formularios",
        "folder": "exercicios_formularios",
        "template_prefix": "exercicios_formularios",
        "excluded_targets": set(),
    },
    {
        "slug": "exercicios-flask",
        "title": "Exercicios Flask",
        "folder": "exercicios_flask",
        "template_prefix": "exercicios_flask",
        "excluded_targets": {"index", "inicio", "pagina-inicial", "paginainicial"},
    },
]


def _humanize_name(file_stem):
    return file_stem.replace("_", " ").replace("-", " ").title()


def _slugify(file_stem):
    return file_stem.replace("_", "-")


def _strip_accents(value):
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(character for character in normalized if not unicodedata.combining(character))


def _normalize_target(target):
    path = Path(target)
    target_name = path.name
    if target_name.endswith(".html"):
        target_name = target_name[:-5]

    return _slugify(_strip_accents(target_name)).lower()


def _target_keys(target):
    normalized = _normalize_target(target)
    compact = normalized.replace("-", "")
    return {normalized, compact}


def _target_matches(requested_keys, exercise):
    exercise_keys = _target_keys(exercise["slug"]) | _target_keys(exercise["filename"])
    if requested_keys & exercise_keys:
        return True

    for requested_key in requested_keys:
        for exercise_key in exercise_keys:
            if exercise_key.startswith(f"{requested_key}-"):
                return True

    return False


def load_exercise_modules(base_dir):
    modules = []

    for module in MODULE_DIRECTORIES:
        templates_dir = Path(base_dir) / module["folder"] / "templates"
        html_files = sorted(
            path
            for path in templates_dir.glob("*.html")
            if not path.name.startswith("_")
            and not (_target_keys(path.name) & module["excluded_targets"])
        )

        exercises = [
            {
                "slug": _slugify(path.stem),
                "title": _humanize_name(path.stem),
                "template": f"{module['template_prefix']}/{path.name}",
                "filename": path.name,
            }
            for path in html_files
        ]

        modules.append(
            {
                "slug": module["slug"],
                "title": module["title"],
                "folder": module["folder"],
                "exercises": exercises,
            }
        )

    return modules


def get_list(list_slug, base_dir=None):
    exercise_lists = load_exercise_modules(base_dir or Path(__file__).resolve().parent)
    return next(
        (exercise_list for exercise_list in exercise_lists if exercise_list["slug"] == list_slug),
        None,
    )


def get_exercise(list_slug, exercise_slug, base_dir=None):
    exercise_list = get_list(list_slug, base_dir)
    if exercise_list is None:
        return None

    requested_keys = _target_keys(exercise_slug)

    return next(
        (
            exercise
            for exercise in exercise_list["exercises"]
            if _target_matches(requested_keys, exercise)
        ),
        None,
    )


def find_exercise_by_target(target, base_dir=None):
    exercise_lists = load_exercise_modules(base_dir or Path(__file__).resolve().parent)
    requested_keys = _target_keys(target)

    for exercise_list in exercise_lists:
        for exercise in exercise_list["exercises"]:
            if _target_matches(requested_keys, exercise):
                return exercise_list, exercise

    return None, None
