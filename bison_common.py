# -*- coding: utf-8 -*-

from conans import AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
from conans.tools import get_env
from contextlib import contextmanager
import os
import tempfile


class BisonCommon:
    def __init__(self, conanfile):
        self.conanfile = conanfile

    @property
    def os(self):
        if self.conanfile.is_installer:
            return self.conanfile.settings.os_build
        else:
            return self.conanfile.settings.os

    def build_requirements(self):
        if tools.os_info.is_windows:
            self.conanfile.build_requires("msys2_installer/latest@bincrafters/stable")

    def configure(self):
        if self.os == "Windows":
            raise ConanInvalidConfiguration("Flex is not supported on Windows.")
        if self.conanfile.settings.compiler in ("gcc", "clang", ):
            del self.conanfile.settings.compiler.libcxx

    def source(self):
        name = "bison"
        filename = "{}-{}.tar.gz".format(name, self.conanfile.version)
        url = "https://ftp.gnu.org/gnu/{}/{}".format(name, filename)
        sha256 = "0fda1d034185397430eb7b0c9e140fb37e02fbfc53b90252fa5575e382b6dbd1"

        dlfilepath = os.path.join(tempfile.gettempdir(), filename)
        if os.path.exists(dlfilepath) and not get_env("BISON_FORCE_DOWNLOAD", False):
            self.conanfile.output.info("Skipping download. Using cached {}".format(dlfilepath))
        else:
            self.conanfile.output.info("Downloading {} from {}".format(name, url))
            tools.download(url, dlfilepath)
        tools.check_sha256(dlfilepath, sha256)
        tools.untargz(dlfilepath)
        extracted_dir = "{}-{}".format(name, self.conanfile.version)
        os.rename(extracted_dir, self.conanfile._source_subfolder)

        # Fix path of bison in yacc script (use environment variable)
        yacc_in = os.path.join(self.conanfile.source_folder, self.conanfile._source_subfolder, "src", "yacc.in")
        tools.replace_in_file(yacc_in,
                              "@prefix@",
                              "${}_ROOT".format(self.conanfile.name.upper()))
        tools.replace_in_file(yacc_in,
                              "@bindir@",
                              "${}_ROOT/bin".format(self.conanfile.name.upper()))

    @contextmanager
    def create_build_environment(self):
        if self.conanfile.settings.compiler == "Visual Studio":
            with tools.vcvars(self.conanfile.settings):
                with tools.environment_append({'LD': "link"}):
                    yield
        else:
            yield

    @property
    def configure_dir(self):
        return os.path.join(self.conanfile.source_folder, self.conanfile._source_subfolder)

    def build(self):
        with self.create_build_environment():
            env_build = AutoToolsBuildEnvironment(self.conanfile, win_bash=tools.os_info.is_windows)
            env_build.fpic = True
            env_build.configure(configure_dir=self.configure_dir)
            env_build.make()

    def package(self):
        with tools.chdir(self.conanfile.build_folder):
            env_build = AutoToolsBuildEnvironment(self.conanfile, win_bash=tools.os_info.is_windows)
            env_build.install()

        self.conanfile.copy("COPYING", src=self.configure_dir, dst="licenses")

        bison_bin = "bison.exe" if self.os == "Windows" else "bison"
        self.conanfile.run("strip \"{}\"".format(os.path.join(self.conanfile.package_folder, "bin", bison_bin)))
