# -*- coding: utf-8 -*-

import logging
import logging.config
import re
from logging import Logger
from pathlib import Path
import yaml
from typing import Callable, Tuple, Dict, List
from collections.abc import Mapping
import os

from injector import Injector, Binder, singleton
from .utils import AliasDict

LOGGER = logging.getLogger(__name__)


class InvokerContext():

    logger = LOGGER.getChild('InvokerContext')  # type: Logger

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
                 logging_config_path: Path = None):

        if logging_config_path:
            self.set_logging_config(logging_config_path)

        self.injector = None  # type: Injector

        # logging default setting.
        config = AliasDict({})
        for c_file in config_file_list:
            cl = AliasDict.load_from_yaml(c_file)
            config.update(cl)

        self.app_config = config
        self.injector = Injector(modules=[self._injector_bind])  # type: Injector

    def _injector_bind(self, binder: Binder):
        binder.bind(AliasDict, to=self.app_config, scope=singleton)

    def invoke(self, func: Callable, args: Tuple, kwargs: Dict) -> any:

        self.logger.info('func: %s  args: %s, kwargs: %s', func, args, kwargs)
        try:
            ret = self.injector.call_with_injection(
                func, args=args, kwargs=kwargs)
            return ret
        except Exception as e:
            self.logger.exception('unexpected error. %s', func)
            raise e
