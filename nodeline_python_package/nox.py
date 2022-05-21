# -*- coding: utf-8 -*-
"""Nox Template Script."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import contextlib
import glob
import os
import winreg

# Import third-party modules
import nox


@contextlib.contextmanager
def patch_entry(session, new_python_path):
    virtual_env = session.env["VIRTUAL_ENV"]
    Scripts = os.path.join(virtual_env, "Scripts")
    exe_pattern = os.path.join(Scripts, "*.exe")
    program_set = set(glob.iglob(exe_pattern))
    python_path = os.path.join(Scripts, "python.EXE").encode("utf-8")

    yield

    # NOTES(timmyliang): replace running python.exe
    program_set = set(glob.iglob(exe_pattern)) - program_set
    for program_path in program_set:
        with open(program_path, "rb") as rf:
            exe_content = rf.read()
        with open(program_path, "wb") as wf:
            wf.write(exe_content.replace(python_path, new_python_path.encode("utf-8")))


def get_maya_location(version):
    path = r"SOFTWARE\Autodesk\Maya\{0}\Setup\InstallPath".format(version)
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    maya_location, _ = winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")
    return maya_location


def get_maya_locations():
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Autodesk\Maya")
    maya_locations = {}
    for index in range(winreg.QueryInfoKey(key)[0]):
        version = winreg.EnumKey(key, index)
        if version.isnumeric():
            maya_location = get_maya_location(version)
            if os.path.isdir(maya_location):
                maya_locations[version] = maya_location
    return maya_locations


@nox.session
@nox.parametrize(
    "maya_location",
    [nox.param(path, id=version) for version, path in get_maya_locations().items()],
)
def maya(session: nox.Session, maya_location: str) -> None:
    virtual_env = session.env["VIRTUAL_ENV"]
    mayapy_location = os.path.join(maya_location, "bin", "mayapy.exe")

    with patch_entry(session, mayapy_location):
        # NOTES(timmyliang): py2 py3 compat
        session.install(
            "scandir",
            "funcsigs",
            "atomicwrites==1.1.0",
            "more_itertools==5.0.0",
            "packaging==20.9",
            "pathlib2==2.3",
            "configparser==4.0.2",
            "contextlib2==0.6.0.post1",
            "zipp==1.2.0",
            "importlib-metadata==2.1.3",
            "pytest==4.6",
        )

    session.env["PYTHONPATH"] = ";".join(
        [os.path.join(virtual_env, "Lib", "site-packages")]
    )
    PATH_ENV = session.env.get("PATH", "").split(";")
    Scripts = os.path.join(virtual_env, "Scripts")
    # bin_folder = os.path.dirname(mayapy_location)
    session.env["PATH"] = ";".join([Scripts] + PATH_ENV)

    session.run("pytest")
