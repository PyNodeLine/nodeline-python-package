"""dodo file."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import glob
import os
import sys
import posixpath
from shutil import rmtree
import signal
import subprocess

# Import third-party modules
from doit.action import CmdAction
import toml
from dotenv import load_dotenv

load_dotenv()
for path in os.getenv("PYTHONPATH").split(";"):
    if path not in sys.path:
        sys.path.insert(0, path)
        
# NOTES(timmyliang): for ctrl+C quit
signal.signal(signal.SIGINT, signal.SIG_DFL)

DOIT_CONFIG = {
    # NOTES(timmyliang): list task with definition order.
    "sort": "definition",
    "verbosity": 2,
}

DIR = os.path.dirname(__file__)
PY_FILES = glob.glob(posixpath.join(DIR, "**/*.py"), recursive=True)
with open(posixpath.join(DIR, "pyproject.toml"), "r") as rf:
    PYPROJECT = toml.load(rf)


def add_short_name(short_name):
    """Doit for short decorator.

    Args:
        short_name (str): short alias name.

    Returns:
        callable: decoartor function.
    """

    def decorator(func):
        globals()["task_{0}".format(short_name)] = func  # noqa: WPS421
        return func

    return decorator


@add_short_name("@f")
def task_group_format():
    """[Group] Run `black` `isort`."""
    return {"actions": None, "task_dep": ["black", "isort"]}


@add_short_name("@init")
def task_group_init():
    """[Group] Run `dot_env` `nitpick`."""
    return {"actions": None, "task_dep": ["dot_env", "nitpick"]}


@add_short_name("pf")
def task_preflight():
    """Run pre commit for all files."""
    command = ["nox", "-s", "preflight"]
    return {"actions": [command]}


@add_short_name("b")
def task_black():
    """Run black format all python files."""
    command = ["nox", "-s", "black", "--"] + PY_FILES
    return {"actions": [command]}


@add_short_name("i")
def task_isort():
    """Run isort format all python files."""
    command = ["nox", "-s", "isort", "--"] + PY_FILES
    return {"actions": [command]}


@add_short_name("l")
def task_lint():
    """Run flakehell lint for all python files."""
    env = ["nox", "-s", "flakehell", "--"]
    command = env + ["flakehell", "lint", "."]
    return {"actions": [command]}


@add_short_name("bl")
def task_baseline():
    """Run flakehell lint for all python files."""
    env = ["nox", "-s", "flakehell", "--"]
    command = env + ["flakehell", "baseline", ">", ".flakehell_baseline"]
    return {"actions": [command]}


@add_short_name("np")
def task_nitpick():
    """Update config with nitpick."""
    env = ["nox", "-s", "nitpick", "--"]
    command = env + ["nitpick", "fix"]
    return {"actions": [lambda: subprocess.call(command) or None]}


@add_short_name("d")
def task_docs():
    """Run mike serve."""

    def serve_docs(api):
        """Generate API docs."""
        # NOTES(timmyliang): remove reference api
        rmtree(posixpath.join(DIR, "docs", "reference"), ignore_errors=True)
        command = ["nox", "-s", "mkdocs", "--"]
        if api:
            script_path = posixpath.join(DIR, "docs", "gen_api_nav.py")
            command += ["python", script_path, "&"]
        return " ".join(command + ["mkdocs", "serve"])

    return {
        "actions": [CmdAction(serve_docs)],
        "params": [
            {
                "name": "api",
                "short": "a",
                "type": bool,
                "default": False,
                "inverse": "flagoff",
                "help": "generate api docs",
            },
        ],
    }


@add_short_name("m")
def task_mike():
    """Run mike serve."""
    # NOTES(timmyliang): for ctrl+C quit
    echo = ["echo", "Serve on http://localhost:8000"]
    docs_env = ["nox", "-s", "mkdocs", "--"]
    command = docs_env + ["mike", "serve"]
    return {"actions": [" ".join(echo), command]}


@add_short_name("dd")
def task_docs_deploy():
    """Run mike to deploy docs."""
    docs_env = ["nox", "-s", "mkdocs", "--"]
    command = docs_env + [
        "mike",
        "deploy",
        "--push",
        "--update-aliases",
        PYPROJECT["tool"]["poetry"]["version"],
        "latest",
    ]
    return {"actions": [command]}


@add_short_name("sub")
def task_add_submodule():
    """Run mike to deploy docs."""

    def add_submodule():
        # Import third-party modules
        import pyperclip

        git_url = pyperclip.paste()
        if not git_url.startswith("git@"):
            return "echo invalid clip text"

        base = os.path.basename(git_url)
        stem = os.path.splitext(base)[0]
        submodule = posixpath.join("_modules", stem)
        command = ["git", "submodule", "add", git_url, submodule]
        return " ".join(command)

    return {"actions": [CmdAction(add_submodule)]}


@add_short_name("env")
def task_dot_env():
    """Generate dot env file for repo."""

    def create_dot_env():
        MODULE = posixpath.join(DIR, "_modules")
        env_path = posixpath.join(DIR, ".env")
        paths = [
            os.path.relpath(os.path.dirname(path)).replace("\\", "/")
            for path in glob.iglob(posixpath.join(MODULE, "**/pyproject.toml"))
        ]

        with open(env_path, "w") as rf:
            rf.write("PYTHONPATH=.;{0}\n".format(";".join(paths)))

    return {"actions": [create_dot_env]}


@add_short_name("pyc")
def task_clear_pyc():
    """Clear pyc cache."""

    def clear_pyc():
        for pyc_path in glob.iglob(posixpath.join(DIR, "**/*.pyc"), recursive=True):
            print(pyc_path)
            os.remove(pyc_path)

    return {"actions": [clear_pyc]}


@add_short_name("pt")
def task_pytest():
    """Run pytest."""
    env = ["nox", "-s", "tests", "--"]
    project_name = PYPROJECT["tool"]["poetry"]["name"].lower().replace("-", "_")
    command = env + ["pytest", project_name]
    return {"actions": [command]}
