#!/bin/sh -ex

PYTHON=${PYTHON:-python}

cd $(dirname $0)/npmjs

${PYTHON} prepare.py
npm install
npm run transpile
npm run pack
npm run build:node
npm run build:browser

mkdir -p dist
npm pack --pack-destination dist