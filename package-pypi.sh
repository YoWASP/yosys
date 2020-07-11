#!/bin/sh -ex

PYTHON=${PYTHON:-python}

rm -rf pypi/yowasp_yosys/share
cp -r \
  yosys-build/yosys.wasm \
  yosys-build/share \
  yosys-src/backends/smt2/smtbmc.py \
  SymbiYosys-src/sbysrc/sby.py \
  pypi/yowasp_yosys/
cp SymbiYosys-src/sbysrc/sby_*.py \
  pypi/yowasp_yosys/share/python3

cd pypi
${PYTHON} setup.py bdist_wheel
sha256sum dist/*.whl
