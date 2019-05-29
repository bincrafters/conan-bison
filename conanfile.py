# -*- coding: utf-8 -*-

from conanfile_base import ConanFileBase


class ConanFileDefault(ConanFileBase):
    name = ConanFileBase._base_name
    version = ConanFileBase.version
    exports = ConanFileBase.exports + ["conanfile_base.py"]

    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def package_info(self):
        self.cpp_info.libs = ["y"]

        self.output.info('Setting BISON_ROOT environment variable: {}'.format(self.package_folder))
        self.env_info.BISON_ROOT = self.package_folder
