#!/tmp/pi-swebench-venv/bin/python

import os
import platform
import runpy
import sys


REAL_PYTHON = "/tmp/pi-swebench-venv/bin/python"
X86_INSTANCE_IDS = {
    "astropy__astropy-7166",
    "astropy__astropy-7336",
    "astropy__astropy-7606",
    "astropy__astropy-7671",
}


def requested_instance_ids(arguments: list[str]) -> set[str]:
    try:
        start = arguments.index("--instance_ids") + 1
    except ValueError:
        return set()
    end = start
    while end < len(arguments) and not arguments[end].startswith("--"):
        end += 1
    return set(arguments[start:end])


if sys.argv[1:3] == ["-m", "swebench.harness.run_evaluation"]:
    module_arguments = sys.argv[3:]
    if requested_instance_ids(module_arguments) & X86_INSTANCE_IDS:
        platform.machine = lambda: "x86_64"
    sys.argv = ["swebench.harness.run_evaluation", *module_arguments]
    runpy.run_module("swebench.harness.run_evaluation", run_name="__main__")
else:
    os.execv(REAL_PYTHON, [REAL_PYTHON, *sys.argv[1:]])
