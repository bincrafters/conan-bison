#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, RunEnvironment, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def test(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("export")
            self.run("bison --version")
            self.run("bison -d %s" % os.path.join(self.source_folder, "mc_parser.yy"))
