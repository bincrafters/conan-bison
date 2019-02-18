# -*- coding: utf-8 -*-

from conans import AutoToolsBuildEnvironment, tools
from conans.client.tools.oss import detected_os
from conans.errors import ConanInvalidConfiguration
from conans.util.env_reader import get_env
import os
import shutil
import tempfile


def conanfile_os(conanfile):
    if conanfile.is_installer:
        return detected_os()
    else:
        return conanfile.settings.os


def bison_configure(conanfile):
    if conanfile_os(conanfile) == "Windows":
        raise ConanInvalidConfiguration("Bison is not supported on Windows.")
    del conanfile.settings.compiler.libcxx


def bison_source(conanfile):
    name = "bison"
    filename = "{}-{}.tar.gz".format(name, conanfile.version)
    url = "https://ftp.gnu.org/gnu/{}/{}".format(name, filename)
    sha256 = "cd399d2bee33afa712bac4b1f4434e20379e9b4099bce47189e09a7675a2d566"

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
    tools.replace_in_file(os.path.join(conanfile.source_folder, conanfile._source_subfolder, "Makefile.in"),
                          "echo \"exec '$(bindir)/bison'",
                          "echo \"exec \"'\"$${}_ROOT/bin/bison\"'\"".format(conanfile.name.upper()))


def bison_build(conanfile):
    env_build = AutoToolsBuildEnvironment(conanfile)
    env_build.fpic = True
    configure_args = []
    env_build.configure(configure_dir=os.path.join(conanfile.source_folder, conanfile._source_subfolder), args=configure_args)
    env_build.make()


def bison_package(conanfile):
    with tools.chdir(conanfile.build_folder):
        env_build = AutoToolsBuildEnvironment(conanfile)
        env_build.install()
    conanfile.copy("COPYING", src=conanfile.source_folder, dst="licenses")
    if conanfile.is_installer:
        shutil.rmtree(os.path.join(conanfile.package_folder, "lib"))
    conanfile.run("strip '{}'".format(os.path.join(conanfile.package_folder, "bison")))
