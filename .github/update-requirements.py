# This script updates the requirements file to match with version constraints in pyproject.yml
# and also removes subdependencies keeping only the main dependencies

import toml
import re

# Load pyproject.toml
with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f)

# Extract dependencies with their correct version constraints
main_deps = pyproject["tool"]["poetry"]["dependencies"]
main_deps.pop("python", None)  # Remove Python entry

# Read exported requirements.txt
with open("requirements.txt", "r") as f:
    exported_reqs = f.readlines()

main_reqs = [
    line
    for line in exported_reqs
    if any(line.split("=")[0] == dep for dep in main_deps.keys())
]


# Function to replace package version while keeping extras/markers
def replace_version(line):
    match = re.match(r"^([a-zA-Z0-9\-_]+)(\[.*\])?([=><~!]+[^\s;]+)(.*)", line)
    if match:
        pkg_name, extras, constraint, rest = match.groups()
        pkg_name_lower = pkg_name.lower()

        if pkg_name_lower in main_deps:
            return f"{pkg_name}{extras or ''}{main_deps[pkg_name_lower]}{rest}\n"

    return line


# Process and replace package versions
updated_reqs = [replace_version(line) for line in main_reqs]

# Write cleaned requirements.txt
with open("requirements.txt", "w") as f:
    f.writelines(updated_reqs)
