import sys
import importlib.resources
import yowasp_runtime


def run_yosys(argv):
    return yowasp_runtime.run_wasm(__package__, "yosys.wasm", resources=["share"],
        argv=["yowasp-yosys", *argv])


def _run_yosys_argv():
    sys.exit(run_yosys(sys.argv[1:]))


def _run_yosys_smtbmc_argv():
    prefix = importlib.resources.files(__package__)
    sys.path[0:0] = [str(prefix / "share" / "python3")]
    smtbmc_py = prefix / "smtbmc.py"
    with open(smtbmc_py) as f:
        globals = {"__name__": "__main__"}
        exec(compile(f.read(), smtbmc_py, "exec"), globals, globals)


def _run_yosys_witness_argv():
    prefix = importlib.resources.files(__package__)
    sys.path[0:0] = [str(prefix / "share" / "python3")]
    witness_py = prefix / "witness.py"
    with open(witness_py) as f:
        globals = {"__name__": "__main__"}
        exec(compile(f.read(), witness_py, "exec"), globals, globals)


def _run_sby_argv():
    prefix = importlib.resources.files(__package__)
    sys.path[0:0] = [str(prefix / "share" / "python3")]
    sby_py = prefix / "sby.py"
    with open(sby_py) as f:
        globals = {}
        exec(compile(f.read(), sby_py, "exec"), globals, globals)
