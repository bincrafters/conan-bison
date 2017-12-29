#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class BisonConan(ConanFile):
    name = "bison"
    version = "3.0.4"
    url = "https://github.com/bincrafters/conan-bison"
    homepage = "https://www.gnu.org/software/bison/"
    description = "Bison is a general-purpose parser generator"
    license = "https://git.savannah.gnu.org/cgit/bison.git/tree/COPYING"
    authors = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/bison/"
        tools.get("{0}/{1}-{2}.tar.gz".format(source_url, self.name,self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def configure(self):
        if self.settings.os == "Windows":
            raise Exception("Bison is not supported on Windows.")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        configure_args = ['--prefix=%s' % self.package_folder]
        with tools.chdir("sources"):
            env_build.configure(args=configure_args)
            env_build.make(args=["all"])
            env_build.make(args=["install"])

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="COPYING", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.BISON_PKGDATADIR = os.path.join(self.package_folder, "share", "bison")
