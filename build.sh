#!/bin/sh -ex

WASI_SDK=wasi-sdk-11.0
WASI_SDK_URL=https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-11/wasi-sdk-11.0-linux.tar.gz
if ! [ -d ${WASI_SDK} ]; then curl -L ${WASI_SDK_URL} | tar xzf -; fi

mkdir -p yosys-build
cat >yosys-build/Makefile.conf <<END
export PATH := $(pwd)/${WASI_SDK}/bin:${PATH}
WASI_SYSROOT := $(pwd)/${WASI_SDK}/share/wasi-sysroot

CONFIG := wasi
PREFIX := /

ENABLE_TCL := 0
ENABLE_READLINE := 0
ENABLE_PLUGINS := 0
ENABLE_ZLIB := 0

CXXFLAGS += -flto
LDFLAGS += -flto -Wl,--strip-all
END
make -C yosys-build -f ../yosys-src/Makefile PRETTY=0 CXX="ccache clang"

rm -rf pypi/yowasp_yosys/share
cp -r yosys-build/yosys.wasm yosys-build/share pypi/yowasp_yosys/
