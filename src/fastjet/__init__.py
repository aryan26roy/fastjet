from . import _core


class fastjet:  # wrapper class on python side
    @staticmethod
    def printer():
        _core.interface()
