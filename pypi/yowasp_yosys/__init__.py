import os
import sys
import tempfile
import wasmtime
try:
    from importlib import resources as importlib_resources
    try:
        importlib_resources.files # py3.9+ stdlib
    except AttributeError:
        import importlib_resources # py3.8- shim
except ImportError:
    import importlib_resources # py3.6- shim


# This isn't used yet but if yosys-abc becomes a separate binary then it will be.
_tempdir = tempfile.TemporaryDirectory("yosys")


def _run_wasm_app(wasm_filename, argv):
    wasm_cfg = wasmtime.Config()
    wasm_cfg.cache = True

    wasi_cfg = wasmtime.WasiConfig()
    wasi_cfg.argv = argv
    wasi_cfg.preopen_dir(str(importlib_resources.files(__package__) / "share"), "/share")
    wasi_cfg.preopen_dir(_tempdir.name, "/tmp")
    wasi_cfg.preopen_dir("/", "/")
    wasi_cfg.preopen_dir(".", ".")
    # sby needs to run `yowasp-yosys -ql ../model/design.log ../model/design.ys`
    wasi_cfg.preopen_dir("..", "..")
    wasi_cfg.inherit_stdin()
    wasi_cfg.inherit_stdout()
    wasi_cfg.inherit_stderr()

    store = wasmtime.Store(wasmtime.Engine(wasm_cfg))
    linker = wasmtime.Linker(store)
    wasi = linker.define_wasi(wasmtime.WasiInstance(store,
        "wasi_snapshot_preview1", wasi_cfg))
    app = linker.instantiate(wasmtime.Module(store.engine,
        importlib_resources.read_binary(__package__, wasm_filename)))
    try:
        app.exports["_start"]()
        return 0
    except wasmtime.ExitTrap as trap:
        return trap.code


def run_yosys(argv):
    return _run_wasm_app("yosys.wasm", ["yowasp-yosys", *argv])


def _run_yosys_argv():
    sys.exit(run_yosys(sys.argv[1:]))


def _run_yosys_smtbmc_argv():
    prefix = importlib_resources.files(__package__)
    sys.path.append(str(prefix / "share" / "python3"))
    smtbmc_py = prefix / "smtbmc.py"
    with open(smtbmc_py) as f:
        globals = {}
        exec(compile(f.read(), smtbmc_py, "exec"), globals, globals)


def _run_sby_argv():
    prefix = importlib_resources.files(__package__)
    sys.path.append(str(prefix / "share" / "python3"))
    sby_py = prefix / "sby.py"
    with open(sby_py) as f:
        globals = {}
        exec(compile(f.read(), sby_py, "exec"), globals, globals)
