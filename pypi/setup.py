import re
from setuptools import setup, find_packages
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


def long_description():
    with open("../README.md") as f:
        return f.read()


setup(
    name="yowasp-yosys",
    version=version(),
    author="whitequark",
    author_email="whitequark@whitequark.org",
    description="Yosys Open SYnthesis Suite",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    license="ISC", # same as Yosys
    python_requires="~=3.5",
    setup_requires=["setuptools_scm", "wheel"],
    install_requires=[
        "importlib_resources; python_version<'3.9'",
        "appdirs~=1.4",
        "wasmtime>=0.30,<2.0"
    ],
    packages=["yowasp_yosys"],
    package_data={"yowasp_yosys": [
        "*.wasm",
        "share/*", "share/**/*", "share/**/**/*", "share/**/**/**/*", # why
    ]},
    entry_points={
        "console_scripts": [
            "yowasp-yosys = yowasp_yosys:_run_yosys_argv",
            "yowasp-yosys-smtbmc = yowasp_yosys:_run_yosys_smtbmc_argv",
            "yowasp-sby = yowasp_yosys:_run_sby_argv",
        ],
    },
    project_urls={
        "Homepage": "https://yowasp.github.io/",
        "Source Code": "https://github.com/YoWASP/yosys",
        "Bug Tracker": "https://github.com/YoWASP/yosys/issues",
    },
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
    ],
)
