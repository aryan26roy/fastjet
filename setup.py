#!/usr/bin/env python
# Copyright (c) 2021, Aryan Roy
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/aryan26roy/fastjet.git for details.

from setuptools import setup  # isort:skip
import setuptools
import setuptools.command.build_ext
import setuptools.command.install
from setuptools import setup, Extension
import os
import platform
import subprocess
import sys
import distutils.util
import shutil
import multiprocessing
import sysconfig
from setuptools.extension import Library
from pathlib import Path

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension  # isort:skip

# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)


DIR = Path(__file__).parent.resolve()
MAINDIR = DIR / "fastjet"

class FastJetBuild(setuptools.command.build_ext.build_ext):
    def build_extensions(self):
        subprocess.Popen(["echo", "$PWD"])
        build_args = []
        try:
            compiler_path = self.compiler.compiler_cxx[0]
        except AttributeError:
            print("Not able to access compiler path, using CMake default")

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        build_dir = self.build_temp


        path = f"--prefix={DIR}/cgal/buildf_dir"
        print("HENRYIII", self.build_temp, MAINDIR, path, flush=True)
        subprocess.call(["pwd"], cwd=MAINDIR)
        env = os.environ.copy()
        env["NOCONFIGURE"] = "1"
        env["PYTHON"] = sys.executable
        env["PYTHON_INCLUDE"] = f'-I{sysconfig.get_path("include")}'
        env["CXXFLAGS"] = "-fPIC"

        subprocess.run(["./autogen.sh"], cwd=MAINDIR, env=env, check=True)
        subprocess.run(
            [
                "./configure",
                path,
                "--enable-trackjet",
                "--enable-atlascone",
                "--enable-cmsiterativecone",
                "--enable-d0runicone",
                "--enable-d0runiicone",
                "--enable-swig",
                "--enable-pyext",
                "--enable-pxcone",
            ],
            cwd=MAINDIR,
            check=True,
            env=env,
        )
        subprocess.call(["make", "check"], cwd=MAINDIR)
        subprocess.call(["make", "install"], cwd=MAINDIR)

        setuptools.command.build_ext.build_ext.build_extensions(self)


ext_modules = [
    Pybind11Extension(
        "fastjet._core",
        ["src/main.cpp"],
        cxx_std=11,
        include_dirs=["fastjet/include"],
        extra_objects=[f"{DIR}/cgal/buildf_dir/lib/libfastjet.a"],
    ),
]


setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": FastJetBuild},
    install_requires=["numpy"],
)
