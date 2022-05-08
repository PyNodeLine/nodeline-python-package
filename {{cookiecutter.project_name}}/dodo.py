"""PyDoit script.

configure from pyproject.toml.
[tool.doit]
dodoFile = "scripts/dodo.py"
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import glob
import os
from shutil import rmtree
import signal

# Import third-party modules
from doit.action import CmdAction
import toml


DIR = os.path.dirname(__file__)

# NOTES(timmyliang): for ctrl+C quit
signal.signal(signal.SIGINT, signal.SIG_DFL)


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


@add_short_name("f")
def task_format():
    """Run `black` `isort`.

    Returns:
        dict: doit config.
    """
    return {"actions": None, "task_dep": ["black", "isort"]}


@add_short_name("pf")
def task_preflight():
    """Run pre commit for all files.

    Returns:
        dict: doit config.
    """
    command = ["poetry", "run", "pre-commit", "run", "-a"]
    return {"actions": [command], "verbosity": 2}


@add_short_name("b")
def task_black():
    """Run black format all python files.

    Returns:
        dict: doit config.
    """
    PY_FILES = glob.glob(os.path.join(DIR, "**/*.py"), recursive=True)
    command = ["poetry", "run", "black"] + PY_FILES
    return {"actions": [command], "verbosity": 2}


@add_short_name("i")
def task_isort():
    """Run isort format all python files.

    Returns:
        dict: doit config.
    """
    PY_FILES = glob.glob(os.path.join(DIR, "**/*.py"), recursive=True)
    command = ["poetry", "run", "isort"] + PY_FILES
    return {"actions": [command], "verbosity": 2}


@add_short_name("l")
def task_lint():
    """Run flakehell lint for all python files.

    Returns:
        dict: doit config.
    """
    command = ["poetry", "run", "flakehell", "lint", "."]
    return {"actions": [command], "verbosity": 2}


@add_short_name("test")
def task_pytest():
    """Run pytest.

    Returns:
        dict: doit config.
    """
    command = ["poetry", "run", "pytest"]
    return {"actions": [command], "verbosity": 2}


def gen_api(api):
    """Generate API docs.

    Args:
        api (bool): flag to generate docs

    Returns:
        str: running command
    """
    # NOTES(timmyliang): remove reference api
    rmtree(os.path.join(DIR, "docs", "reference"), ignore_errors=True)
    script_path = os.path.join(DIR, "docs", "gen_api_nav.py")
    api_command = " ".join(["poetry", "run", "python", script_path])
    serve_command = " ".join(["poetry", "run", "mkdocs", "serve"])
    return "{0} & {1}".format(api_command, serve_command) if api else serve_command


@add_short_name("d")
def task_docs():
    """Run mike serve.

    Returns:
        dict: doit config.
    """
    return {
        "actions": [CmdAction(gen_api)],
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
        "verbosity": 2,
    }


@add_short_name("m")
def task_mike():
    """Run mike serve.

    Returns:
        dict: doit config.
    """
    # NOTES(timmyliang): for ctrl+C quit
    echo = ["echo", "Serve on http://localhost:8000"]
    command = ["poetry", "run", "mike", "serve"]
    return {"actions": [" ".join(echo), command], "verbosity": 2}


@add_short_name("dd")
def task_docs_deploy():
    """Run mike to deploy docs.

    Returns:
        dict: doit config.
    """
    with open(os.path.join(DIR, "pyproject.toml"), "r") as rf:
        pyproject = toml.load(rf)
    command = [
        "poetry",
        "run",
        "mike",
        "deploy",
        "--push",
        "--update-aliases",
        pyproject["tool"]["poetry"]["version"],
        "latest",
    ]
    return {"actions": [command], "verbosity": 2}
