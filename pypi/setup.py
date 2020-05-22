from setuptools import setup, find_packages
from setuptools_scm.git import parse as parse_git


def version():
    yosys_git = parse_git("../yosys-src")
    if yosys_git.exact:
        yosys_version = yosys_git.format_with("{tag}")
    else:
        yosys_version = yosys_git.format_with("{tag}.post{distance}")

    package_git = parse_git("..")
    package_version = package_git.format_with(".dev{distance}")

    return yosys_version + package_version


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
        "wasmtime~=0.18.0"
    ],
    packages=["yowasp_yosys"],
    package_data={"yowasp_yosys": [
        "yosys.wasm",
        # why
        "share/*", "share/**/*", "share/**/**/*", "share/**/**/**/*"
    ]},
    entry_points={
        "console_scripts": [
            "yowasp-yosys = yowasp_yosys:_run_yosys_argv",
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
