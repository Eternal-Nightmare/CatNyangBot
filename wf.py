"""This is invoked in a subprocess to call the build backend hooks.

It expects:
- Command line args: hook_name, control_dir
- Environment variables:
      PEP517_BUILD_BACKEND=entry.point:spec
      PEP517_BACKEND_PATH=paths (separated with os.pathsep)
- control_dir/input.json:
  - {"kwargs": {...}}

Results:
- control_dir/output.json
  - {"return_val": ...}
"""
from glob import glob
from importlib import import_module
import json
import os
import os.path
from os.path import join as pjoin
import re
import shutil
import sys
import traceback

# This file is run as a script, and `import compat` is not zip-safe, so we
# include write_json() and read_json() from compat.py.
#
# Handle reading and writing JSON in UTF-8, on Python 3 and 2.

if sys.version_info[0] >= 3:
    # Python 3
    def write_json(obj, path, **kwargs):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, **kwargs)

    def read_json(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

else:
    # Python 2
    def write_json(obj, path, **kwargs):
        with open(path, 'wb') as f:
            json.dump(obj, f, encoding='utf-8', **kwargs)

    def read_json(path):
        with open(path, 'rb') as f:
            return json.load(f)


class BackendUnavailable(Exception):
    """Raised if we cannot import the backend"""
    def __init__(self, traceback):
        self.traceback = traceback


class BackendInvalid(Exception):
    """Raised if the backend is invalid"""
    def __init__(self, message):
        self.message = message

