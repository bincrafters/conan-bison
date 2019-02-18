#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_installer
from conans.client.tools.oss import detected_os
import os


if __name__ == "__main__":
    arch_str = os.environ.get("ARCH", "x86,x86_64")
    archs = arch_str.split(",")

    builder = build_template_installer.get_builder()
    for arch in archs:
        builder.add(settings={"os_build": detected_os(), "arch_build": arch, })
    builder.run()
