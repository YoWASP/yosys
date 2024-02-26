#!/bin/sh -ex

export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)

WASI_SDK=wasi-sdk-19.0
WASI_SDK_URL=https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-19/wasi-sdk-19.0-linux.tar.gz
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
LINKFLAGS += -Wl,--strip-all
END
make -C yosys-build -f ../yosys-src/Makefile PRETTY=0 CXX="ccache clang"
