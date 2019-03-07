# -*- coding: utf-8 -*-

from conans import ConanFile, CMake
from conans.client.tools.oss import detected_os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake",

    def build_requirements(self):
        if detected_os() == "Windows":
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run("bison --version")
        self.run("yacc --version")
