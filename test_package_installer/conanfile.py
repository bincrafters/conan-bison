#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, CMake


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake",

    def build_requirements(self):
        if tools.os_info.is_windows:
            if "CONAN_BASH_PATH" not in os.environ:
                self.build_requires("msys2_installer/latest@bincrafters/stable")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run("bison --version", run_environment=True)
        self.run("yacc --version", run_environment=True, win_bash=tools.os_info.is_windows)
        mc_parser = os.path.join(self.source_folder, "mc_parser.yy")
        self.run("bison -d %s" % mc_parser, run_environment=True)
