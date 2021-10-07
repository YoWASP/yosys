import os
import sys
import tempfile
import wasmtime
import pathlib
import hashlib
import appdirs
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
    module_binary = importlib_resources.read_binary(__package__, wasm_filename)
    module_digest = hashlib.sha1(module_binary).digest()

    wasi_cfg = wasmtime.WasiConfig()
    wasi_cfg.argv = argv
    wasi_cfg.preopen_dir(str(importlib_resources.files(__package__) / "share"), "/share")
    wasi_cfg.preopen_dir(_tempdir.name, "/tmp")
    if os.name == "nt":
        for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            wasi_cfg.preopen_dir(letter + ":\\", letter + ":")
    else:
        wasi_cfg.preopen_dir("/", "/")
    wasi_cfg.preopen_dir(".", ".")
    for level in range(len(pathlib.Path().cwd().parts)):
        wasi_cfg.preopen_dir(str(pathlib.Path("").joinpath(*[".."] * level)),
                             "/".join([".."] * level))
    wasi_cfg.inherit_stdin()
    wasi_cfg.inherit_stdout()
    wasi_cfg.inherit_stderr()
    
    engine = wasmtime.Engine()
    cache_path = pathlib.Path(os.getenv("YOWASP_CACHE_DIR", appdirs.user_cache_dir("yowasp")))
    cache_path.mkdir(parents=True, exist_ok=True)
    cache_filename = (cache_path / "{}-cache".format(wasm_filename))
    digest_filename = (cache_path / "{}-digest".format(wasm_filename))
    try:
        with digest_filename.open("rb") as digest_file:
            if digest_file.read() != module_digest:
                raise Exception("cache miss")
        module = wasmtime.Module.deserialize_file(engine, str(cache_filename))
    except:
        print("Preparing to run {}. This might take a while...".format(argv[0]), file=sys.stderr)
        module = wasmtime.Module(engine, module_binary)
        with cache_filename.open("wb") as cache_file:
            cache_file.write(module.serialize())
        with digest_filename.open("wb") as digest_file:
            digest_file.write(module_digest)

    linker = wasmtime.Linker(engine)
    linker.define_wasi()
    store = wasmtime.Store(engine)
    store.set_wasi(wasi_cfg)
    app = linker.instantiate(store, module)
    linker.define_instance(store, "app", app)
    try:
        app.exports(store)["_start"](store)
        return 0
    except wasmtime.ExitTrap as trap:
        return trap.code


def run_yosys(argv):
    return _run_wasm_app("yosys.wasm", ["yowasp-yosys", *argv])


def _run_yosys_argv():
    sys.exit(run_yosys(sys.argv[1:]))


def _run_yosys_smtbmc_argv():
    prefix = importlib_resources.files(__package__)
    sys.path[0:0] = [str(prefix / "share" / "python3")]
    smtbmc_py = prefix / "smtbmc.py"
    with open(smtbmc_py) as f:
        globals = {}
        exec(compile(f.read(), smtbmc_py, "exec"), globals, globals)


def _run_sby_argv():
    prefix = importlib_resources.files(__package__)
    sys.path[0:0] = [str(prefix / "share" / "python3")]
    sby_py = prefix / "sby.py"
    with open(sby_py) as f:
        globals = {}
        exec(compile(f.read(), sby_py, "exec"), globals, globals)
