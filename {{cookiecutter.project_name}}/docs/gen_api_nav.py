"""Plugin for generate API docs."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
from pathlib import Path
from shutil import rmtree

# Import third-party modules
import mkdocs_gen_files
import toml


DIR = Path(__file__).parent
ROOT = DIR.parent
WHITE_LIST = ("__init__", "__main__", "__version__", "test")


def get_api_root():
    """Get API Root for the project.

    Returns:
        str: project source folder path.
    """
    with open(str(ROOT / "pyproject.toml"), "r") as rf:
        pyproject = toml.load(rf)
    project_name = pyproject["tool"]["poetry"]["name"]
    return ROOT.joinpath(project_name)


def is_in_whitelist(full_doc_path):
    """Check path is contain white list.

    Args:
        full_doc_path (str): doc path.

    Returns:
        bool: is in white list.
    """
    return list(filter(lambda part: part in full_doc_path, WHITE_LIST))


def write_api_files(path, full_doc_path, nav):
    """Write Api Docs files.

    Args:
        path (Path): python script path.
        full_doc_path (Path): docs path.
        nav (mkdocs_gen_files.Nav): nav object.
    """
    nav_parts = list(path.relative_to(ROOT).with_suffix("").parts)
    if nav_parts[-1].startswith("_"):
        nav_parts[-1] = nav_parts[-1][1:]
    nav[nav_parts] = full_doc_path.as_posix().replace("\\", "/")
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        print("::: {0}".format(".".join(nav_parts)), file=fd)  # noqa: WPS421

    mkdocs_gen_files.set_edit_path(full_doc_path, path.as_posix().replace("\\", "/"))


def generate_api_docs():
    """Generate docs."""
    nav = mkdocs_gen_files.Nav()
    rmtree(DIR / "reference", ignore_errors=True)

    for path in sorted(get_api_root().glob("**/*.py")):
        doc_path = path.relative_to(ROOT).with_suffix(".md")
        full_doc_path = Path("reference", doc_path).as_posix().replace("\\", "/")
        if is_in_whitelist(full_doc_path):
            continue
        write_api_files(path, doc_path, full_doc_path, nav)

    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


if __name__ in {"<run_path>", "__main__"}:
    generate_api_docs()
