#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager
from conans.util.env_reader import get_env
import os

if __name__ == "__main__":
    build_bison_installer = get_env("BUILD_BISON_INSTALLER", False)

    subdir = "bison_installer" if build_bison_installer else "bison"
    builder = ConanMultiPackager(
        cwd=os.path.join(os.path.dirname(os.path.realpath(__file__)), subdir),
        docker_entry_script="cd {}".format(subdir)
    )

    if build_bison_installer:
        arch_str = get_env("ARCH", "x86,x86_64")
        archs = arch_str.split(",")

        for arch in archs:
            builder.add(settings={"arch_build": arch,})
    else:
        builder.add_common_builds()

    builder.run()
