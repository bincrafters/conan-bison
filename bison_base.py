# -*- coding: utf-8 -*-

from conans.errors import ConanInvalidConfiguration
import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class BisonBase(ConanFile):
    version = "3.3.2"
    url = "https://github.com/bincrafters/conan-bison"
    homepage = "https://www.gnu.org/software/bison/"
    description = "Bison is a general-purpose parser generator"
    license = "GPL-3.0-or-later"
    authors = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    _source_subfolder = "source_subfolder"
    requires = ("m4_installer/1.4.18@bincrafters/stable",)

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/bison/"
        tools.get("{0}/{1}-{2}.tar.gz".format(source_url, "bison", self.version),
                  sha256="0fda1d034185397430eb7b0c9e140fb37e02fbfc53b90252fa5575e382b6dbd1")
        extracted_dir = "bison-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            raise ConanInvalidConfiguration("Bison is not supported on Visual Studio.")
        del self.settings.compiler.libcxx

    def build(self):
        env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        with tools.chdir(self._source_subfolder):
            env_build.configure()
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
