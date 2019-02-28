import glob
import importlib
import inspect
import logging
import os
import re
import sys
from os.path import isfile


class Pydi:
    def __init__(self, something, directory=None):
        self._logger = logging.getLogger(__name__)
        self._directory = directory or os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self._class_type_map = self._detect_classes()
        self._something = self.build_dependency(something)

    def _detect_classes(self):
        self._logger.info('Detecting project\'s classes')

        current_dir = self._directory
        modules = glob.glob(current_dir + "/**/*.py", recursive=True)
        reg = re.compile('src.*(?=\.)')

        class_type_names = [reg.findall(f)[0].replace('/', '.') for f in modules if isfile(f) and not f.endswith('__init__.py')]
        # print(f'All: {class_type_names}')

        class_types = set((inspect.getmembers(sys.modules[importlib.import_module(name).__name__], inspect.isclass)[0][1]) for name in class_type_names[1:])
        # print(class_types)

        return {type.__name__.lower(): type for type in class_types}

    def build_dependency(self, dependency_name):
        return self._class_type_map[dependency_name]()

    def thing(self):
        self._something.do()


pydi = Pydi('something')
pydi.thing()
