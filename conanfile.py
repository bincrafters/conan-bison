# -*- coding: utf-8 -*-

# NOTE: this is a temporary shim until new CPT is released with fix for
# https://github.com/conan-io/conan-package-tools/issues/354

import os

if "BUILD_INSTALLER" in os.environ:

    from bison_installer import BisonInstaller

    class ConanBisonInstaller(BisonInstaller):
        name = "bison_installer"
        version = BisonInstaller.version

else:

    from bison import Bison

    class ConanBison(Bison):
        name = "bison"
        version = Bison.version
