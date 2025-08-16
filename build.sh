#!/bin/sh -ex

export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)

WASI_VER=27
WASI_SDK=wasi-sdk-${WASI_VER}.0-x86_64-linux
WASI_SDK_URL=https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_VER}/${WASI_SDK}.tar.gz
if ! [ -d ${WASI_SDK} ]; then curl -L ${WASI_SDK_URL} | tar xzf -; fi
WASI_SDK_PATH=$(pwd)/${WASI_SDK}

FLEX_VER=2.6.4
FLEX=flex-${FLEX_VER}
FLEX_URL=https://github.com/westes/flex/releases/download/v${FLEX_VER}/${FLEX}.tar.gz
if ! [ -d ${FLEX} ]; then curl -L ${FLEX_URL} | tar xzf -; fi

mkdir -p flex-build
(cd flex-build &&
  ../${FLEX}/configure --prefix=$(pwd)/../flex-prefix &&
  make &&
  make install)

mkdir -p yosys-build
cat >yosys-build/Makefile.conf <<END
export PATH := ${WASI_SDK_PATH}/bin:$(pwd)/flex-prefix/bin:${PATH}
WASI_SYSROOT := ${WASI_SDK_PATH}/share/wasi-sysroot

PRETTY := 0
CONFIG := wasi

ENABLE_CCACHE := 1
ENABLE_TCL := 0
ENABLE_READLINE := 0
ENABLE_PLUGINS := 0
ENABLE_ZLIB := 0

CXXFLAGS += -I$(pwd)/flex-prefix/include -flto
LINKFLAGS += -Wl,-z,stack-size=8388608 -Wl,--stack-first -Wl,--strip-all
LIBS := -Wl,--whole-archive,$(pwd)/yosys-slang-build/libyosys-slang.a,--no-whole-archive
END

# First, install yosys developer files.
make -C yosys-build -f ../yosys-src/Makefile install-dev PREFIX=$(pwd)/yosys-prefix

# Second, build yosys-slang.
cmake -B yosys-slang-build -S yosys-slang-src \
  -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
  -DCMAKE_TOOLCHAIN_FILE=${WASI_SDK_PATH}/share/cmake/wasi-sdk.cmake \
  -DCMAKE_INSTALL_PREFIX=$(pwd)/yosys-slang-prefix \
  -DCMAKE_BUILD_TYPE=Release \
  -DYOSYS_CONFIG=$(pwd)/yosys-build/yosys-config \
  -DBUILD_AS_PLUGIN=OFF
cmake --build yosys-slang-build

# At last, build yosys including yosys-slang as a static library.
make -C yosys-build -f ../yosys-src/Makefile PREFIX=/
