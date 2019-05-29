# -*- coding: utf-8 -*-

import os
from conanfile_base import ConanBase


class ConanInstaller(ConanBase):
    name = ConanBase._base_name + "_installer"
    version = ConanBase.version
    exports = ConanBase.exports + ["conanfile_base.py"]

    settings = "os_build", "arch_build", "compiler"

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)

        bison_pkgdir = os.path.join(self.package_folder, "share", "bison")
        self.output.info('Setting BISON_INSTALLER_PKGDATADIR environment variable: {}'.format(bison_pkgdir))
        self.env_info.BISON_PKGDATADIR = bison_pkgdir

        self.output.info('Setting BISON_INSTALLER_ROOT environment variable: {}'.format(self.package_folder))
        self.env_info.BISON_INSTALLER_ROOT = self.package_folder
