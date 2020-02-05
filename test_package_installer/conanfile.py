import os
from conans import ConanFile, tools, CMake
from six import StringIO


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake",

    def build_requirements(self):
        if not tools.cross_building(self.settings):
            if tools.os_info.is_windows and not tools.get_env("CONAN_BASH_PATH") and \
                    tools.os_info.detect_windows_subsystem() != "msys2":
                self.build_requires("msys2/20190524")

    def build(self):
        # verify CMake integration
        if not tools.cross_building(self.settings):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            # verify bison may run
            self.run("bison --version", run_environment=True)
            # verify yacc may run
            self.run("yacc --version", run_environment=True, win_bash=tools.os_info.is_windows)
            # verify bison may preprocess something
            mc_parser = os.path.join(self.source_folder, "mc_parser.yy")
            self.run("bison -d %s" % mc_parser, run_environment=True)
            # verify bison doesn't have hard-coded paths
            bison = tools.which("bison")
            if tools.which("strings") and tools.which("grep"):
                self.run('strings %s | grep "\.bison" > strings_bison || true' % bison)
                output = tools.load("strings_bison").strip()
                if output:
                    raise Exception("bison has hard-coded paths to conan: %s" % output)
            # verify bison works without BISON_PKGDATADIR and M4 environment variables
            with tools.environment_append({"BISON_PKGDATADIR": None, "M4": None}):
                self.run("bison -d %s" % mc_parser, run_environment=True)
