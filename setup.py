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
# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension  # isort:skip

# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

try:
    import cmake

    CMAKE = os.path.join(cmake.CMAKE_BIN_DIR, "cmake")
except ImportError:
    CMAKE = "cmake"   
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)
class CMakeBuild(setuptools.command.build_ext.build_ext):
    def build_extensions(self):
        try:
            out = subprocess.check_output([CMAKE, "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(x.name for x in self.extensions)
            )

        for x in self.extensions:
            self.build_extension(x)

    def build_extension(self, ext):
        subprocess.Popen(["echo","$PWD"])
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        build_args = []
        cmake_args = [
            "-DCGAL_HEADER_ONLY=OFF".format(extdir),
            "-DCMAKE_BUILD_TYPE=Release".format(sys.executable),
            "..",
        ]
        try:
            compiler_path = self.compiler.compiler_cxx[0]
            cmake_args += ["-DCMAKE_CXX_COMPILER={0}".format(compiler_path)]
        except AttributeError:
            print("Not able to access compiler path, using CMake default")

        cfg = "Debug" if self.debug else "Release"
        build_args += ["--config", cfg]
        cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]

        if platform.system() == "Windows":
            #cmake_args += [
                #"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{0}={1}".format(cfg.upper(), extdir),
                #"-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE",
            #]
            cmake_generator = os.environ.get("CMAKE_GENERATOR", "")
            if (
                sys.maxsize > 2 ** 32
                and cmake_generator != "NMake Makefiles"
                and "Win64" not in cmake_generator
            ):
                cmake_args += ["-A", "x64"]

        elif "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            build_args += ["-j", str(multiprocessing.cpu_count())]

        if (
            platform.system() == "Darwin"
            and "MACOSX_DEPLOYMENT_TARGET" not in os.environ
        ):
            cmake_args += ["-DCMAKE_OSX_DEPLOYMENT_TARGET=10.9"]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        build_dir = self.build_temp
        cwdd = os.getcwd() 
        #subprocess.Popen([CMAKE,"-DCGAL_HEADER_ONLY=OFF","-DCMAKE_BUILD_TYPE=Release",".."],cwd= cwdd+"/cgal/build_dir")
        #except subprocess.CalledProcessError as e:
        #	print(e.output)
        #try:
        #    subprocess.check_call(["make"],cwd=cwdd+"cgal/build_dir")
        #except subprocess.CalledProcessError as e:
        #    print(e.output)
        #try:
        #    subprocess.check_call(["make", "install"],cwd=cwd"cgal/build_dir")
        #except subprocess.CalledProcessError as e:
       # 	print(e.output)
        #try:
        #raise ValueError(cwdd)
        path = "--prefix="+cwdd+"/cgal/buildf_dir"
        subprocess.call(["pwd"],cwd=cwdd+"/fastjet")
        subprocess.call(
            	["./configure", path, "--enable-trackjet", "--enable-atlascone", "--enable-cmsiterativecone", "--enable-d0runicone", "--enable-d0runiicone", "--enable-swig", "--enable-pyext", "--enable-pxcone"],cwd=cwdd+"/fastjet")
        	#subprocess.check_call(["make"],cwd=cwdd+"/fastjet")
        #except subprocess.CalledProcessError as e:
        	#print(e.output)	
        subprocess.call(["make", "check"],cwd=cwdd+"/fastjet")	
        subprocess.call(["make", "install"],cwd=cwdd+"/fastjet")
        #subprocess.check_call([CMAKE, "--build", build_dir] + build_args)
        #subprocess.check_call(
            #[CMAKE, "--build", build_dir, "--config", cfg, "--target", "install"]
        #)

ext_modules = [CMakeExtension("Fastjet"),
    Pybind11Extension(
        "fastjet._core",
        ["src/main.cpp"],
        cxx_std=11,
    ),
]


setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": CMakeBuild}, #"install": Install},
    setup_requires=['pybind11>=2.2'],
    install_requires=[
        'numpy','pybind11>=2.2'
    ]
)
