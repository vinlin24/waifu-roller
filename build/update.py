#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update.py
22 August 2022 16:42:28

Script to use the JSON metadata file to update appropriate files
as part of a pre-push checklist.

To be called from build/build.ps1, where the current working directory
is asserted to be build/.

Return an exit code of 0 on success, 1 otherwise (Exception).
"""

import configparser
import json
import re
import sys
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

# Relative paths from build/ to files
METADATA_JSON_PATH = Path("./meta.json")
WORKFLOW_YAML_PATH = Path("../.github/workflows/main.yml")
SETUP_CFG_PATH = Path("../src/setup.cfg")
PACKAGE_INIT_PATH = Path("../src/waifu/__init__.py")

# From main.yml schema
WORKFLOW_JOB_NAME = "update-badges"
WORKFLOW_STEP_NAME = "Dynamic Badges"

JSONData = dict[str, Any]


def update_badge(meta: JSONData) -> None:
    """Update the 'message' field in the GitHub workflow file."""
    # Load YAML
    yaml = YAML()  # round-trip handler
    loaded = yaml.load(WORKFLOW_YAML_PATH)

    # Find version field to update
    steps = loaded["jobs"][WORKFLOW_JOB_NAME]["steps"]
    for step in steps:
        if step["name"] == WORKFLOW_STEP_NAME:
            break
    else:
        raise ValueError(
            "Could not find workflow job step name with "
            f"{WORKFLOW_STEP_NAME=}"
        )

    # Update version field with new version string
    new_version = meta["version"]
    step["with"]["message"] = new_version

    # Dump updated YAML
    yaml.dump(loaded, WORKFLOW_YAML_PATH)

    print(f"\tINFO: Successfully updated {WORKFLOW_YAML_PATH}")


def update_setup(meta: JSONData) -> None:
    """Update the value of metadata.version in the setup.cfg file."""
    # Load cfg
    config = configparser.ConfigParser()
    config.read(SETUP_CFG_PATH)

    # Update version field
    new_version = meta["version"]
    config["metadata"]["version"] = new_version

    # Dump updated cfg (loses comments)
    with open(SETUP_CFG_PATH, "wt") as fp:
        config.write(fp, space_around_delimiters=True)

    print(f"\tINFO: Successfully updated {SETUP_CFG_PATH}")


def update_init(meta: JSONData) -> None:
    """Update the value of __version__ in the source __init__.py."""
    updated_line = f"__version__ = \"{meta['version']}\""

    # Match the line that __version__ is assigned on
    version_finder = re.compile(r"^__version__ ?= ?.*$", re.MULTILINE)
    with open(PACKAGE_INIT_PATH, "rt+") as fp:
        content = fp.read()
        match = version_finder.search(content)
        # __version__ isn't assigned yet, append the line
        if match is None:
            fp.write(updated_line)
            return
        # Otherwise replace that line
        start, end = match.start(), match.end()
        updated_content = content[:start] + updated_line + content[end:]
        fp.truncate(0)
        fp.seek(0)
        fp.write(updated_content)

    print(f"\tINFO: Successfully updated {PACKAGE_INIT_PATH}")


def main() -> None:
    """Main driver function."""
    # Load JSON metadata
    json_path = Path(METADATA_JSON_PATH)
    with open(json_path, "rt") as fp:
        meta = json.load(fp)

    # Run updaters
    print("[update.py] INFO: Running updaters...")
    update_badge(meta)
    update_setup(meta)
    update_init(meta)

    # Let PS know everything went well
    sys.exit(0)


if __name__ == "__main__":
    main()
