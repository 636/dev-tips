# -*- coding: utf-8 -*-

import logging
import logging.config
from logging import Logger
from pathlib import Path
import yaml
from typing import Callable, Tuple, Dict, List
from collections import Mapping
import os

from injector import Injector, Binder, singleton

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
            if isinstance(v, Mapping):
                r = cls.update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]

        return d


class Invoker():

    logger = LOGGER.getChild('Invoker')  # type: Logger

    IS_ALREADY_LOADED_LOGGING = False

    @classmethod
    def set_logging_config(cls, logging_config_file: Path):

        if cls.IS_ALREADY_LOADED_LOGGING:
            cls.logger.warning(
                'already initilize logging configuration. skip.')

        else:
            cls.logger.info('initilize logging configuration. start')
            with logging_config_file.open('r', encoding='utf-8') as f:
                config = yaml.load(f)

            logging.config.dictConfig(config)
            cls.IS_ALREADY_LOADED_LOGGING = True
            cls.logger.info(
                'initilize logging configuration. end: \n%s', config)

    def __init__(self, config_file_list: List[Path],
                 logging_config_path: Path=None):

        if logging_config_path:
            self.set_logging_config(logging_config_path)

        
        self.injector = None  # type: Injector

        # logging default setting.
        self.set_logging_config(logging_config_file)
        self.injector = Injector()  # type: Injector

    def invoke(self, func: Callable, args: Tuple, kwargs: Dict) -> any:

        self.logger.info('func: %s  args: %s, kwargs: %s', func, args, kwargs)
        try:
            ret = self.injector.call_with_injection(
                func, args=args, kwargs=kargs)
            return ret
        except Exception as e:
            self.logger.exception('unexpected error. %s', func)
            raise e
