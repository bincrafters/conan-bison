# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake",

    def build_requirements(self):
        version = self.requires["bison"].ref.version
        user = self.requires["bison"].ref.user
        channel = self.requires["bison"].ref.channel

        self.build_requires("bison_installer/{}@{}/{}".format(version, user, channel))
        if tools.os_info.is_windows:
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run(os.path.join(self.build_folder, "bin", "McParser"))
