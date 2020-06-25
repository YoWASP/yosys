#!/bin/sh -ex

PYTHON=${PYTHON:-python}

rm -rf pypi/yowasp_yosys/share
cp -r yosys-build/yosys.wasm yosys-build/share pypi/yowasp_yosys/

cd pypi
${PYTHON} setup.py bdist_wheel 
sha256sum dist/*.whl
