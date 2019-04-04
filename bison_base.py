# -*- coding: utf-8 -*-

from conans.errors import ConanInvalidConfiguration
from conans import ConanFile, AutoToolsBuildEnvironment, tools
import glob
import os
import shutil


class BisonBase(ConanFile):
    version = "3.3.2"
    url = "https://github.com/bincrafters/conan-bison"
    homepage = "https://www.gnu.org/software/bison/"
    description = "Bison is a general-purpose parser generator"
    license = "GPL-3.0-or-later"
    authors = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    exports_sources = ["patches/*.patch"]
    _source_subfolder = "source_subfolder"
    requires = ("m4_installer/1.4.18@bincrafters/stable",)

    @property
    def _is_msvc(self):
        return self.settings.compiler == "Visual Studio"

    def build_requirements(self):
        if tools.os_info.is_windows:
            if "CONAN_BASH_PATH" not in os.environ:
                self.build_requires("msys2_installer/latest@bincrafters/stable")
        if self._is_msvc:
            self.build_requires("automake_build_aux/1.16.1@bincrafters/stable")

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/bison/"
        tools.get("{0}/{1}-{2}.tar.gz".format(source_url, "bison", self.version),
                  sha256="0fda1d034185397430eb7b0c9e140fb37e02fbfc53b90252fa5575e382b6dbd1")
        extracted_dir = "bison-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        for filename in glob.glob("patches/*.patch"):
            self.output.info('applying patch "%s"' % filename)
            tools.patch(base_path=self._source_subfolder, patch_file=filename)
        with tools.vcvars(self.settings) if self._is_msvc else tools.no_op():
            self._build_configure()

    def _build_configure(self):
        args = ["HELP2MAN=/bin/true"]
        build = None
        host = None
        if self._is_msvc:
            for filename in ["compile", "ar-lib"]:
                shutil.copy(os.path.join(self.deps_cpp_info["automake_build_aux"].rootpath, filename),
                            os.path.join(self._source_subfolder, "build-aux", filename))
            build = False
            if self.settings.arch == "x86":
                host = "i686-w64-mingw32"
            elif self.settings.arch == "x86_64":
                host = "x86_64-w64-mingw32"
            args.extend(['CC=$PWD/build-aux/compile cl -nologo',
                         'CFLAGS=-%s' % self.settings.compiler.runtime,
                         'LD=link',
                         'NM=dumpbin -symbols',
                         'STRIP=:',
                         'AR=$PWD/build-aux/ar-lib lib',
                         'RANLIB=:'])

        env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        with tools.chdir(self._source_subfolder):
            tools.replace_in_file("Makefile.in",
                                  "dist_man_MANS = $(top_srcdir)/doc/bison.1",
                                  "dist_man_MANS =")
            tools.replace_in_file(os.path.join("src", "yacc.in"),
                                  "@prefix@",
                                  "${}_ROOT".format(self.name.upper()))
            tools.replace_in_file(os.path.join("src", "yacc.in"),
                                  "@bindir@",
                                  "${}_ROOT/bin".format(self.name.upper()))

            env_build.configure(args=args, build=build, host=host)
            env_build.make()
            env_build.install()

        if self._is_msvc:
            shutil.move(os.path.join(self.package_folder, "lib", "liby.a"),
                        os.path.join(self.package_folder, "lib", "y.lib"))

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
