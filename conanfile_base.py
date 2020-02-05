from conans.errors import ConanInvalidConfiguration
from conans import ConanFile, AutoToolsBuildEnvironment, tools
import glob
import os
import shutil


class ConanFileBase(ConanFile):
    _base_name = "bison"
    version = "3.3.2"
    url = "https://github.com/bincrafters/conan-bison"
    homepage = "https://www.gnu.org/software/bison/"
    description = "Bison is a general-purpose parser generator"
    topics = ("conan", "bison", "parser")
    license = "GPL-3.0-or-later"
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
                self.build_requires("msys2/20190524")
        if self._is_msvc:
            self.build_requires("automake/1.16.1")

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/bison/"
        tools.get("{0}/{1}-{2}.tar.gz".format(source_url, "bison", self.version),
                  sha256="0fda1d034185397430eb7b0c9e140fb37e02fbfc53b90252fa5575e382b6dbd1")
        extracted_dir = "bison-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def build(self):
        for filename in sorted(glob.glob("patches/*.patch")):
            self.output.info('applying patch "%s"' % filename)
            tools.patch(base_path=self._source_subfolder, patch_file=filename)
        with tools.vcvars(self.settings) if self._is_msvc else tools.no_op():
            self._build_configure()

    def _build_configure(self):
        true = tools.which("true") or "/bin/true"
        true = tools.unix_path(true) if tools.os_info.is_windows else true
        args = ["HELP2MAN=%s" % true, "MAKEINFO=%s" % true, "--disable-nls"]
        build = None
        host = None
        if self._is_msvc:
            build = False
            if self.settings.arch == "x86":
                host = "i686-w64-mingw32"
            elif self.settings.arch == "x86_64":
                host = "x86_64-w64-mingw32"
            automake_perldir = os.getenv('AUTOMAKE_PERLLIBDIR')
            if automake_perldir.startswith('/mnt/'):
                automake_perldir = automake_perldir[4:]
            args.extend(['CC=%s/compile cl -nologo' % automake_perldir,
                         'CFLAGS=-%s' % self.settings.compiler.runtime,
                         'LD=link',
                         'NM=dumpbin -symbols',
                         'STRIP=:',
                         'AR=%s/ar-lib lib' % automake_perldir,
                         'RANLIB=:',
                         "gl_cv_func_printf_directive_n=no"])

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
