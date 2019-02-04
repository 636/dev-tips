# -*- coding: utf-8 -*-

import logging
import os
import re
from collections import UserDict, Mapping
from logging import Logger
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import yaml
from injector import Binder, Injector, singleton

LOGGER = logging.getLogger(__name__)


class AliasDict():
    """
      Alias Dictionary
    """

    logger = LOGGER.getChild('AliasDict')  # type: logging.Logger

    @classmethod
    def load_from_yaml(cls, path: Path, **kargs) -> 'AliasDict':
        """
          load from yaml
        """

        assert path.exists()

        with path.open('r', encoding='utf-8') as f:
            return cls(yaml.load(f), **kargs)

    def __init__(self, config: dict,
                 replace_pattern: str='\${(.*)}',
                 suffix_handler={
                     'dir': lambda val: os.path.expanduser(val)
                 }):

        self._replace_pattern = re.compile(replace_pattern)
        self._cache = {}
        self._suffix_handler = suffix_handler

        self.data = config

    def _replacer(self, match):
        return self.get(match.group()[2:-1])

    def get(self, key: str, default=None):
        if key in self._cache:
            return self._cache.get(key)

        keys = key.split('.')
        last = keys[-1]

        try:
            ret = self.__get(self.data, keys)
            if isinstance(ret, str):
                ret = self._replace_pattern.sub(self._replacer, ret)

            ret = self._suffix_handler.get(last, lambda x: x)(ret)

            self._cache.setdefault(key, ret)
            return ret
        except KeyError:
            self.logger.error('Not found spec key:%s', keys)
            return None

    def __get(self, config, keys):

        if len(keys) == 1:
            return config[keys[0]]
        else:
            return self.__get(config[keys[0]], keys[1:])

    def update(self, u):
        if isinstance(u, AliasDict):
            u = u.data

        self.data = AliasDict.deep_update(self.data, u)

    @classmethod
    def deep_update(cls, d, u):
        for k, v in u.items():
            if isinstance(v, Mapping):
                r = cls.deep_update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]

        return d
