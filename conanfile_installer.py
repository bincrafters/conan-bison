import os
from conanfile_base import ConanFileBase


class ConanInstaller(ConanFileBase):
    name = ConanFileBase._base_name + "_installer"
    version = ConanFileBase.version
    exports = ConanFileBase.exports + ["conanfile_base.py"]

    settings = "os_build", "arch_build", "compiler", "arch"

    def package_id(self):
        self.info.include_build_settings()
        del self.info.settings.compiler
        del self.info.settings.arch

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)

        bison_pkgdir = os.path.join(self.package_folder, "share", "bison")
        self.output.info('Setting BISON_PKGDATADIR environment variable: {}'.format(bison_pkgdir))
        self.env_info.BISON_PKGDATADIR = bison_pkgdir

        self.output.info('Setting BISON_INSTALLER_ROOT environment variable: {}'.format(self.package_folder))
        self.env_info.BISON_INSTALLER_ROOT = self.package_folder
