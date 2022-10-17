YoWASP Yosys packages
=====================

This package provides [Yosys][] binaries built for [WebAssembly][]. See the [overview of the YoWASP project][yowasp] for details.

[yosys]: https://github.com/YosysHQ/yosys/
[webassembly]: https://webassembly.org/
[yowasp]: https://yowasp.github.io/

Building
--------

The primary build environment for this repository is the `ubuntu-latest` GitHub CI runner; packages are built on every push and automatically published from the `release` branch to PyPI.

To reduce maintenance overhead, the only development environment we will support for this repository is x86_64 Linux.

License
-------

This package is covered by the [ISC license](LICENSE.txt), which is the same as the [Yosys license](https://github.com/YosysHQ/yosys/blob/master/COPYING).
