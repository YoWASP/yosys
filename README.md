YoWASP Yosys packages
=====================

This package provides [Yosys][] binaries built for [WebAssembly][]. See the [overview of the YoWASP project][yowasp] for details.

[yosys]: https://github.com/YosysHQ/yosys/
[webassembly]: https://webassembly.org/
[yowasp]: https://yowasp.github.io/


Versioning
----------

The version of this package is derived from the upstream Yosys package version in the ``X.Y[.Z][+N]`` format, and is comprised of five or six parts in a ``X.Y.Z.N.postM[.dev]`` format:

1. ``X``: Yosys major version
2. ``Y``: Yosys minor version
3. ``Z``: Yosys patch version; only present for some Yosys releases, zero if not present
4. ``N``: zero for packages built from Yosys releases, ``N`` for packages built from unreleased Yosys snapshots; matches the ``N`` in the ``X.Y+N`` upstream version
5. ``postM``: package build version; disambiguates different builds produced from the same Yosys source tree
6. ``dev``: present only for packages built from unreleased Yosys snapshots; marks these packages as pre-releases

With this scheme, there is a direct correspondence between upstream versions and [PEP 440][pep440] Python package versions. Packages built from unreleased snapshots are ignored by pip by default, but can be still installed explicitly. (These packages are uploaded daily to [TestPyPI][], but only occasionally to [PyPI][].)

A different versioning scheme was used earlier, where the package build version was denoted by a ``.devM`` suffix. This scheme did not work well with [PEP 440 version specifiers][pep440-vs] and was retired.

[testpypi]: https://test.pypi.org/
[pypi]: https://pypi.org/
[pep440]: https://peps.python.org/pep-0440/
[pep440-vs]: https://peps.python.org/pep-0440/#version-specifiers


Configuration
-------------

See the documentation for [yowasp-runtime](https://github.com/YoWASP/runtime#configuration).


License
-------

This package is covered by the [ISC license](LICENSE.txt), which is the same as the [Yosys license](https://github.com/YosysHQ/yosys/blob/master/COPYING).
