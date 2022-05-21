# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import contextlib
import glob
import os
import posixpath
import winreg
import warnings

# Import third-party modules
import nox
import toml


DIR = os.path.dirname(os.path.abspath(__file__))
with open(posixpath.join(DIR, "pyproject.toml"), "r") as rf:
    PYPROJECT = toml.load(rf)


@nox.session
def preflight(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@nox.session
def black(session: nox.Session) -> None:
    session.install("black")
    session.run("black", *session.posargs)


@nox.session
def isort(session: nox.Session) -> None:
    session.install("isort")
    session.run("isort", *session.posargs)


@nox.session
def nitpick(session: nox.Session) -> None:
    session.install("nitpick")
    session.run(*session.posargs)


@nox.session
def flakehell(session: nox.Session) -> None:
    session.install(
        "flakehell==0.9.0",
        "flake8==3.9.0",
        "wemake-python-styleguide",
    )
    session.run(*session.posargs)


@nox.session
def commitizen(session: nox.Session) -> None:
    session.install("commitizen")
    session.run(*session.posargs)


@nox.session
def mkdocs(session: nox.Session) -> None:
    session.install(
        "mkdocs",
        "mike",
        "pymdown-extensions",
        "mkdocs-click",
        "mkdocs-material",
        "mkdocs-gen-files",
        "mkdocs-include-markdown-plugin",
        "mkdocs-literate-nav",
        "mkdocstrings",
        "mkdocstrings-python",
        "markdown-callouts",
        "mkdocs-pymdownx-material-extras",
        "mkdocs-same-dir",
        "mkdocs-section-index",
        "mkdocs-autolinks-plugin",
        "mkdocs-awesome-pages-plugin",
        "mkdocs-minify-plugin",
        "mkdocs-git-revision-date-localized-plugin",
        "mkdocs-static-i18n",
    )
    session.run(*session.posargs)


@nox.session()
def tests(session: nox.Session) -> None:
    session.install(
        "pytest",
        "tomlkit",
        "cookiecutter",
        "pytest-randomly",
        "pytest-cookies",
        "jinja2-git",
        "lice",
        "safety",
        "MarkupSafe==2.0",
    )
    session.run(*session.posargs)
