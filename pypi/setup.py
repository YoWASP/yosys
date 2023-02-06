import re
import subprocess
from setuptools import setup
from setuptools_scm.git import parse as parse_git


def version():
    upstream_git = parse_git("../yosys-src")
    package_git  = parse_git("..")

    yosys_version_raw = subprocess.check_output([
        "make", "-s", "-C", "../yosys-src", "echo-yosys-ver"
    ], encoding="utf-8").strip()

    # Yosys can't figure out if it should have a patch version or not.
    # Match one, and add one below in our version just in case.
    yosys_version = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?(?:\+(\d+))?$", yosys_version_raw)
    yosys_major  = int(yosys_version[1])
    yosys_minor  = int(yosys_version[2])
    yosys_patch  = int(yosys_version[3] or "0")
    yosys_node   = int(yosys_version[4]) if yosys_version[4] else None
    
    version = f"{yosys_major}.{yosys_minor}.{yosys_patch}"
    if yosys_node is None: # release
        version += f".0"
    else: # snapshot
        version += f".{yosys_node}"
    version += f".post{package_git.distance}"
    if yosys_node is not None: # snapshot
        version += f".dev"
    if upstream_git.dirty or package_git.dirty:
        version += f"+dirty"
    return version


setup(
    version=version(),
)
