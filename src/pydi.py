import glob
import inspect
import os
import re
import sys
from os.path import dirname, basename, isfile
import logging
import importlib

# from src.test.dude import Dude
sys.path.append('/home/user/Documents/dev/pydi')

class Pydi:
    def __init__(self, directory=None):
        self._logger = logging.getLogger(__name__)
        self._directory = directory or os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self._src = '/home/user/Documents/dev/pydi/src'

    def detect_classes(self):
        self._logger.info('Detecting project\'s classes')

        current_dir = self._directory

        modules = glob.glob(current_dir + "/**/*.py", recursive=True)

        reg = re.compile('src.*(?=\.)')

        __all__ = [reg.findall(f)[0].replace('/', '.') for f in modules if isfile(f) and not f.endswith('__init__.py')]
        x = 1

        print(f'All: {__all__}')

        class_types = set()

        for name in __all__[1:]:
            x = importlib.import_module(name)
            class_types.add(inspect.getmembers(sys.modules[x.__name__], inspect.isclass)[0][1])

        print(class_types)

        objs = [type() for type in class_types]

        print(objs)


pydi = Pydi()
pydi.detect_classes()


# dude = Dude()
