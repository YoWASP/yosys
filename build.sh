#!/bin/sh -ex

export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)

WASI_SDK=wasi-sdk-12.0
WASI_SDK_URL=https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-12/wasi-sdk-12.0-linux.tar.gz
if ! [ -d ${WASI_SDK} ]; then curl -L ${WASI_SDK_URL} | tar xzf -; fi

${WASI_SDK}/bin/clang --sysroot ${WASI_SDK}/share/wasi-sysroot -c getopt_long.c

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
LDLIBS := $(pwd)/getopt_long.o
END
make -C yosys-build -f ../yosys-src/Makefile PRETTY=0 CXX="ccache clang"
