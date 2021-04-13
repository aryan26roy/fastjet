#!/usr/bin/env python
# Copyright (c) 2021, Aryan Roy
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/aryan26roy/fastjet.git for details.

from setuptools import setup  # isort:skip
import os
import subprocess
import sys
import sysconfig
from pathlib import Path
import distutils.util
import shutil

import setuptools
import setuptools.command.build_ext
import setuptools.command.install

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
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        path = f"--prefix={DIR}/cgal/buildf_dir"
        subprocess.call(["pwd"], cwd=MAINDIR)
        env = os.environ.copy()
        env["NOCONFIGURE"] = "1"
        env["PYTHON"] = sys.executable
        env["PYTHON_INCLUDE"] = f'-I{sysconfig.get_path("include")}'
        # env["CXXFLAGS"] = "-fPIC"  # maybe not needed anymore
        if sys.platform.startswith("darwin"):
            env["FC"] = "gfortran"

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
        subprocess.call(["make", "check", "-j"], cwd=MAINDIR)
        subprocess.call(["make", "install"], cwd=MAINDIR)

        setuptools.command.build_ext.build_ext.build_extensions(self)

def tree(x):
    print(x + (" (dir)" if os.path.isdir(x) else ""))
    if os.path.isdir(x):
        for y in os.listdir(x):
            tree(os.path.join(x, y))


class Install(setuptools.command.install.install):
    def run(self):
        outerdir = os.path.join(
            os.path.join(
                "build",
                "lib.%s-%d.%d"
                % (
                    distutils.util.get_platform(),
                    sys.version_info[0],
                    sys.version_info[1],
                ),
            )
        )

        print("--- this directory --------------------------------------------")
        for x in sorted(os.listdir(".")):
            print(x)

        print("--- build directory -------------------------------------------")
        tree("build")

        print("--- copying includes ------------------------------------------")
        shutil.copytree(
            os.path.join(f"{DIR}/cgal/buildf_dir/lib/python3.8/site-packages"),
            os.path.join(outerdir, "fastjet", "include"),
        )
        shutil.copyfile(
            os.path.join(f"{DIR}/cgal/buildf_dir/lib/libfastjet.so.0"),
            os.path.join(outerdir, "fastjet", "include", "libfastjet.so.0"),
        )
        shutil.copyfile(
            os.path.join(f"{DIR}/cgal/buildf_dir/lib/libfastjettools.so.0"),
            os.path.join(outerdir, "fastjet", "include", "libfastjettools.so.0"),
        )
        shutil.copyfile(
            os.path.join(f"{DIR}/src/__init__.py"),
            os.path.join(outerdir, "fastjet", "include", "__init__.py"),
        )

        print("--- outerdir after copy ---------------------------------------")
        # tree(outerdir)

        print("--- begin normal install --------------------------------------")
        setuptools.command.install.install.run(self)

    def get_outputs(self):
        outerdir = os.path.join(
            os.path.join(
                "build",
                "lib.%s-%d.%d"
                % (
                    distutils.util.get_platform(),
                    sys.version_info[0],
                    sys.version_info[1],
                ),
            )
        )
        outputdir = os.path.join(outerdir, "fastjet")
        outbase = self.install_lib.rstrip(os.path.sep)
        subprocess.call(
            ["export", 'LD_LIBRARY_PATH="$PWD"'],
            cwd=os.path.join(outerdir, "fastjet", "include"),
        )
        outputs = []

        for original in setuptools.command.install.install.get_outputs(self):
            if "egg-info" in original:
                outputs.append(original)
            if original.startswith(os.path.join(outbase, "fastjet") + os.path.sep):
                outputs.append(original)

        for root, dirs, files in os.walk(outputdir):
            root = root[len(outerdir) :].lstrip(os.path.sep)
            for file in files:
                trial = os.path.join(outbase, os.path.join(root, file))
                if trial not in outputs:
                    outputs.append(trial)

        return outputs


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
    cmdclass={"build_ext": FastJetBuild, "install": Install},
)
