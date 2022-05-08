# nodeline-python-package

[cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) template to create new nodeline python packages


## Purpose

This project is used to scaffold a `python` project structure.
Just like `poetry new` but better.

reference from https://github.com/wemake-services/wemake-python-package

## Features

- Always [`up-to-date`](https://github.com/wemake-services/wemake-python-package/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot) dependencies with the help of [`@dependabot`](https://dependabot.com/)
- Supports latest `python3.7+`
- [`poetry`](https://github.com/python-poetry/poetry) for managing dependencies
- [`mypy`](https://mypy.readthedocs.io) for optional static typing
- [`pytest`](https://github.com/pytest-dev/pytest) for testing
- `flake8` and [`wemake-python-styleguide`](https://github.com/wemake-services/wemake-python-styleguide) for linting
- `Github Actions` as the default CI
- [`mkdocs`](https://www.mkdocs.org/)
- Easy update process, so your template will always be up-to-date


## Installation

Firstly, you will need to install dependencies:

```bash
pip install cookiecutter jinja2-git lice
```

Then, create a project itself:

```bash
cookiecutter gh:PyNodeLine/nodeline-python-package
```

In order for the github actions to work smoothly (ie badge), you must, during the setup, use your github username in the `organization` field.
```bash
project_name [my-awesome-project]: foo-project
organization [wemake.services]: <github_username>
```
