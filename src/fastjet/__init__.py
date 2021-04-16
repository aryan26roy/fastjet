from . import _core
import sys
import os
import ctypes

libfastjet_so_path = os.path.join(os.path.split(__file__)[0],"libs","libfastjet.so.0")
libfastjettools_so_path = os.path.join(os.path.split(__file__)[0],"libs","libfastjettools.so.0")

libfastjet_so = ctypes.cdll.LoadLibrary(libfastjet_so_path)
libfastjettool_so = ctypes.cdll.LoadLibrary(libfastjettools_so_path)

class fastjet:  # wrapper class on python side
    @staticmethod
    def printer():
        _core.interface()
