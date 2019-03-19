# -*- coding: utf-8 -*-

import os
from bison_base import BisonBase

class BisonInstaller(BisonBase):
    settings = "os_build", "arch_build", "compiler"
    exports = ["bison_base.py", "bison_installer.py"]
    
    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bison_pkgdir = os.path.join(self.package_folder, "share", "bison")
        self.output.info('Setting BISON_INSTALLER_PKGDATADIR environment variable: {}'.format(bison_pkgdir))
        self.env_info.BISON_PKGDATADIR = bison_pkgdir
        
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)
