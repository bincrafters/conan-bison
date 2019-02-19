# -*- coding: utf-8 -*-

from conans import AutoToolsBuildEnvironment, tools
from conans.client.tools.oss import detected_os
from conans.client.tools.win import vcvars
from conans.util.env_reader import get_env
from contextlib import contextmanager
import os
import shutil
import tempfile


def conanfile_os(conanfile):
    if conanfile.is_installer:
        return detected_os()
    else:
        return conanfile.settings.os


def bison_build_requirements(conanfile):
    if detected_os() == "Windows":
        conanfile.build_requires("msys2_installer/latest@bincrafters/stable")


def bison_configure(conanfile):
    del conanfile.settings.compiler.libcxx


def bison_source(conanfile):
    name = "bison"
    filename = "{}-{}.tar.gz".format(name, conanfile.version)
    url = "https://ftp.gnu.org/gnu/{}/{}".format(name, filename)
    sha256 = "0fda1d034185397430eb7b0c9e140fb37e02fbfc53b90252fa5575e382b6dbd1"

    dlfilepath = os.path.join(tempfile.gettempdir(), filename)
    if os.path.exists(dlfilepath) and not get_env("BISON_FORCE_DOWNLOAD", False):
        conanfile.output.info("Skipping download. Using cached {}".format(dlfilepath))
    else:
        conanfile.output.info("Downloading {} from {}".format(name, url))
        tools.download(url, dlfilepath)
    tools.check_sha256(dlfilepath, sha256)
    tools.untargz(dlfilepath)
    extracted_dir = "{}-{}".format(name, conanfile.version)
    os.rename(extracted_dir, conanfile._source_subfolder)

    # Fix path of bison in yacc script (use environment variable)
    yacc_in = os.path.join(conanfile.source_folder, conanfile._source_subfolder, "src", "yacc.in")
    tools.replace_in_file(yacc_in,
                          "@prefix@",
                          "${}_ROOT".format(conanfile.name.upper()))
    tools.replace_in_file(yacc_in,
                          "@bindir@",
                          "${}_ROOT/bin".format(conanfile.name.upper()))


@contextmanager
def create_build_environment(conanfile):
    if conanfile.settings.compiler == "Visual Studio":
        with vcvars(conanfile.settings):
            with tools.environment_append({'LD': "link"}):
                yield
    else:
        yield


def bison_build(conanfile):
    if conanfile.should_build:
        with create_build_environment(conanfile):
            env_build = AutoToolsBuildEnvironment(conanfile, win_bash=detected_os() == "Windows")
            env_build.fpic = True
            configure_args = []
            env_build.configure(configure_dir=os.path.join(conanfile.source_folder, conanfile._source_subfolder), args=configure_args)
            env_build.make()


def bison_package(conanfile):
    with tools.chdir(conanfile.build_folder):
        env_build = AutoToolsBuildEnvironment(conanfile)
        env_build.install()
    if conanfile.is_installer:
        shutil.rmtree(os.path.join(conanfile.package_folder, "lib"))
    conanfile.copy("COPYING", src=os.path.join(conanfile.source_folder, conanfile._source_subfolder), dst="licenses")
    conanfile.copy("LICENSE.md", src=conanfile.source_folder, dst="licenses")

    bison_bin = "bison.exe" if conanfile_os(conanfile) == "Windows" else "bison"
    conanfile.run("strip \"{}\"".format(os.path.join(conanfile.package_folder, "bin", bison_bin)))
