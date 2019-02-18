#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans.util.env_reader import get_env
import os
import subprocess
import sys


if __name__ == "__main__":
    is_installer = get_env("BUILD_BISON_INSTALLER", False)
    subdir = "bison_installer" if is_installer else "bison"

    curdir = os.path.dirname(os.path.realpath(__file__))
    subdir = os.path.join(curdir, subdir)
    subprocess.run([str(sys.executable), os.path.join(subdir, "build.py")], check=True, cwd=subdir)
