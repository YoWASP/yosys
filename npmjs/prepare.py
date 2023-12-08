import os
import re
import json
import subprocess


yosys_version_raw = subprocess.check_output([
    "make", "-s", "-C", "../yosys-src", "echo-yosys-ver"
], encoding="utf-8").strip()

git_rev_list_raw = subprocess.check_output([
    "git", "rev-list", "HEAD"
], encoding="utf-8").split()

# Yosys can't figure out if it should have a patch version or not.
# Match one, and add one below in our version just in case.
yosys_version = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?(?:\+(\d+))?$", yosys_version_raw)
yosys_major  = int(yosys_version[1])
yosys_minor  = int(yosys_version[2])
_yosys_patch = int(yosys_version[3] or "0")
yosys_node   = int(yosys_version[4] or "0")

distance = len(git_rev_list_raw) - 1

if os.environ.get("RELEASE_BRANCH", "false") in ("true", "1", "yes"):
    version = f"{yosys_major}.{yosys_minor}.{distance}"
else:
    version = f"{yosys_major}.{yosys_minor + 1}.{yosys_node}-dev.{distance}"
print(f"version {version}")

with open("package-in.json", "rt") as f:
    package_json = json.load(f)
package_json["version"] = version
with open("package.json", "wt") as f:
    json.dump(package_json, f)
