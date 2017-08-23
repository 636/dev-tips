#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import ast
import os
import collections
from pathlib import Path

LOGGER = logging.getLogger(__name__)


class ConfigLoader():
    """
      Configuration Loader
    """

    logger = LOGGER.getChild('ConfigLoader')  # type: logging.Logger

    @staticmethod
    def load_from_yaml(cls, path: Path, **kargs) -> 'ConfigLoader':
        """
          load from yaml
        """

        assert path.exists()

        try:
            import yaml
        except ImportError as e:
            cls.logger.exception('yaml is required module.', e)
            raise e

        with path.open('r', encoding='utf-8') as f:
            return cls(yaml.load(f), **kargs)

    def __init__(self, config: dict,
                 replace_pattern: str='\${(.*)}'):
        self.config = config

        self.replace_pattern = re.compile(replace_pattern)
        self.cache = {}

    def replacer(self, match):
        return self.get(match.group()[2:-1])

    def get(self, keys: str):
        if keys in self.cache:
            return self.cache.get(keys)

        keys = keys.split('.')
        last = keys[-1]

        try:
            ret = self.__get(self.config, keys)
            if isinstance(ret, str):
                ret = self.replace_pattern.sub(self.replacer, ret)

            if last == 'dir':
                ret = os.path.expanduser(ret)

            if last == 'eval':
                ret = ast.literal_eval(ret)

            self.cache.setdefault('.'.join(keys), ret)
            return ret
        except KeyError:
            self.logger.error('Not found spec key:%s', keys)
            return None

    def __get(self, config, keys):

        if len(keys) == 1:
            return config[keys[0]]
        else:
            return self.__get(config[keys[0]], keys[1:])

    @classmethod
    def update(cls, d, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                r = cls.update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]

        return d


if __name__ == '__main__':

    loader = ConfigLoader({
        'test': {
            'base': 'aaa/bbb',
            'concat': '${test.base}/ccc'
        }
    })

    print(loader.get('test.concat') == 'aaa/bbb/ccc')
