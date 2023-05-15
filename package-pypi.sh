#!/bin/sh -ex

PYTHON=${PYTHON:-python}

rm -rf pypi/yowasp_yosys/share
cp -r \
  yosys-build/yosys.wasm \
  yosys-build/share \
  yosys-src/backends/smt2/smtbmc.py \
  yosys-src/backends/smt2/ywio.py \
  yosys-src/backends/smt2/witness.py \
  SymbiYosys-src/sbysrc/sby.py \
  pypi/yowasp_yosys/
cp SymbiYosys-src/sbysrc/sby_*.py \
  pypi/yowasp_yosys/share/python3

cd pypi
rm -rf build && ${PYTHON} -m build -w
sha256sum dist/*.whl
