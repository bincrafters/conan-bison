#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile
import os
import sys


class BisonInstallerConan(ConanFile):
    name = "bison_installer"
    version = "3.3.2"
    url = "https://github.com/bincrafters/conan-bison"
    homepage = "https://www.gnu.org/software/bison/"
    description = "Bison is a general-purpose parser generator"
    license = "GPL-3.0-or-later"
    authors = "Bincrafters <bincrafters@gmail.com>"
    exports = ["../LICENSE.md", "../bison_common.py"]
    settings = "os_build", "arch_build", "compiler"
    _source_subfolder = "source_subfolder"
    no_copy_source = True

    is_installer = True

    def _add_common(self):
        sys.path.append(os.path.dirname(os.path.realpath(__file__)))
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    def build_requirements(self):
        self._add_common()
        from bison_common import bison_build_requirements
        bison_build_requirements(self)

    def source(self):
        self._add_common()
        from bison_common import bison_source
        bison_source(self)

    def configure(self):
        self._add_common()
        from bison_common import bison_configure
        bison_configure(self)

    def build(self):
        self._add_common()
        from bison_common import bison_build
        bison_build(self)

    def package(self):
        self._add_common()
        from bison_common import bison_package
        bison_package(self)

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)

        bison_pkgdir = os.path.join(self.package_folder, "share", "bison")
        self.output.info('Setting BISON_INSTALLER_PKGDATADIR environment variable: {}'.format(bison_pkgdir))
        self.env_info.BISON_INSTALLER_PKGDATADIR = bison_pkgdir

        self.output.info('Setting BISON_INSTALLER_ROOT environment variable: {}'.format(self.package_folder))
        self.env_info.BISON_INSTALLER_ROOT = self.package_folder
