import glob
import importlib
import inspect
import logging
import os
import re
import sys
from os.path import isfile, basename


class Pydi:
    def __init__(self, directory=None):
        self._logger = logging.getLogger(__name__)
        self._directory = directory or os.getcwd()
        self._class_type_map = self._detect_classes()
        print(self._class_type_map)

    def _detect_classes(self):
        self._logger.info('Detecting project\'s classes')

        current_dir = self._directory
        modules = glob.glob(current_dir + "/**/*.py", recursive=True)
        top_folder = basename(os.getcwd())

        class_type_names = [f.split(top_folder + '\\')[-1].replace('\\', '.').replace('.py', '') or f.split(top_folder + '/')[-1].replace('/', '.').replace('.py', '') for f in modules if isfile(f) and not f.endswith('__init__.py')]

        class_types = set((inspect.getmembers(sys.modules[importlib.import_module(name).__name__], inspect.isclass)[0][1]) for name in class_type_names[1:])

        return {type.__name__.lower(): type for type in class_types}

    def build_dependency(self, dependency_name):
        return self._class_type_map[dependency_name]()
