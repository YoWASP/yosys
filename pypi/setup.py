import re
from setuptools import setup
from setuptools_scm.git import parse as parse_git


def version():
    with open("../yosys-src/Makefile", "r") as f:
        yosys_version = re.search(r"^YOSYS_VER := ([\d.]+)(?:\+(\d+))?$", f.read(), re.M)
    if yosys_version[2] is None or yosys_version[2] == "0":
        upstream_version = yosys_version[1]
    else:
        upstream_version = yosys_version[1] + ".post" + yosys_version[2]

    package_git = parse_git("..")
    if not package_git.dirty:
        package_version = package_git.format_with(".dev{distance}")
    else:
        package_version = package_git.format_with(".dev{distance}+dirty")

    return upstream_version + package_version


setup(
    version=version(),
)
