#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, CMake
from six import StringIO


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake",

    def build_requirements(self):
        if not tools.cross_building(self.settings):
            if tools.os_info.is_windows:
                if "CONAN_BASH_PATH" not in os.environ:
                    self.build_requires("msys2_installer/latest@bincrafters/stable")

    def build(self):
        # verify CMake integration
        if not tools.cross_building(self.settings):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            # verify bison may run
            self.run("bison --version", run_environment=True)
            # verify yacc may run
            self.run("yacc --version", run_environment=True, win_bash=tools.os_info.is_windows)
            # verify bison may preprocess something
            mc_parser = os.path.join(self.source_folder, "mc_parser.yy")
            self.run("bison -d %s" % mc_parser, run_environment=True)
            # verify bison doesn't have hard-coded paths
            bison = tools.which("bison")
            if tools.which("strings") and tools.which("grep"):
                output = StringIO()
                self.run('strings %s | grep "\.bison" | true' % bison, output=output)
                output = output.getvalue().strip()
                if output:
                    raise Exception("bison has hard-coded paths to conan: %s" % output)
            # verify bison works without BISON_PKGDATADIR and M4 environment variables
            with tools.environment_append({"BISON_PKGDATADIR": None, "M4": None}):
                self.run("bison -d %s" % mc_parser, run_environment=True)
