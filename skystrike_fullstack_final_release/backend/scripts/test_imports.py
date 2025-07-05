#!/usr/bin/env python3
# coding: utf-8

import pkgutil
import importlib
import sys

# Folders to test (inside your PYTHONPATH)
folders = ["backend.engine", "backend.ml"]
errors = []

for pkg_name in folders:
    try:
        pkg = importlib.import_module(pkg_name)
    except Exception as e:
        print(f"FAIL: could not import package {pkg_name} -> {e}")
        errors.append((pkg_name, e))
        continue

    for finder, name, is_pkg in pkgutil.iter_modules(pkg.__path__):
        if is_pkg or name.startswith("_"):
            continue
        full = f"{pkg_name}.{name}"
        try:
            importlib.import_module(full)
            print(f"OK:   {full}")
        except Exception as e:
            print(f"FAIL: {full} -> {e}")
            errors.append((full, e))

if errors:
    sys.exit(1)
