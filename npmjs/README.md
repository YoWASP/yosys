YoWASP Yosys package
====================

This package provides [Yosys][] binaries built for [WebAssembly][]. See the [overview of the YoWASP project][yowasp] for details.

At the moment, this package only provides an API allowing to run Yosys in a virtual filesystem; no binaries are provided.

This package does not provide access to `sby`, `yowasp-yosys-smtbmc`, and `yowasp-yosys-witness`; only the main `yosys` application is available.

[yosys]: https://github.com/YosysHQ/yosys/
[webassembly]: https://webassembly.org/
[yowasp]: https://yowasp.github.io/


API reference
-------------

This package provides one function:

- `runYosys` (alias `cmd:yosys`)

For more detail, see the documentation for [the JavaScript YoWASP runtime](https://github.com/YoWASP/runtime-js#api-reference).


Versioning
----------

The version of this package is derived from the upstream Yosys package version in the `X.Y[.Z][+N]` format, and can be in one of the two formats, `X.Y.M` (for builds from release branches) or `X.(Y+1).N-dev.M` (for development builds), where the symbols are:

1. `X`: Yosys major version
2. `Y`: Yosys minor version
3. `Z`: Yosys patch version; ignored if present
4. `N`: matches the `N` in the `X.Y+N` upstream version, if present
5. `M`: package build version; disambiguates different builds produced from the same Yosys source tree
6. `-dev`: present only for packages built from unreleased Yosys snapshots; marks these packages as pre-releases

With this scheme, there is a direct correspondence between upstream versions and [SemVer][semver] NPM package versions.

Note that for development builds, the minor version is incremented as required by the SemVer comparison order. This means that an NPM package built from the upstream version `0.45+12` and the 120th commit in this repository will have the version `0.46.12-dev.120`. Because this is a pre-release package, it will not be matched by version specifiers such as `^0.46` or `>=0.46`.

[semver]: https://semver.org/


License
-------

This package is covered by the [ISC license](LICENSE.txt), which is the same as the [Yosys license](https://github.com/YosysHQ/yosys/blob/master/COPYING).
