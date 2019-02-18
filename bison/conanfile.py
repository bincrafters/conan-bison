#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os
import sys


class BisonConan(ConanFile):
    name = "bison"
    version = "3.0.5"
    url = "https://github.com/bincrafters/conan-bison"
    homepage = "https://www.gnu.org/software/bison/"
    description = "Bison is a general-purpose parser generator"
    license = "GPL-3.0-or-later"
    authors = "Bincrafters <bincrafters@gmail.com>"
    exports = ["../LICENSE.md", "../bison_common.py"]
    settings = "os", "arch", "compiler"
    _source_subfolder = "source_subfolder"

    is_installer = False

    @property
    def _conanfile_dir(self):
        return os.path.dirname(os.path.realpath(__file__))

    def source(self):
        sys.path.append(self._conanfile_dir)
        from bison_common import bison_source
        bison_source(self)

    def configure(self):
        sys.path.append(self._conanfile_dir)
        from bison_common import bison_configure
        bison_configure(self)

    def build(self):
        sys.path.append(self._conanfile_dir)
        from bison_common import bison_build
        bison_build(self)

    def package(self):
        sys.path.append(self._conanfile_dir)
        from bison_common import bison_package
        bison_package(self)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        self.output.info('Setting BISON_ROOT environment variable: {}'.format(self.package_folder))
        self.env_info.BISON_ROOT = self.package_folder
