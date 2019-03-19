# -*- coding: utf-8 -*-

from bison_base import BisonBase

class Bison(BisonBase):
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    settings = "os", "arch", "compiler", "build_type"
    exports = ["bison_base.py", "bison.py"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def package_info(self):
        self.cpp_info.libs = ["y"]
