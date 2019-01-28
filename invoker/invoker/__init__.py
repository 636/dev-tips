# -*- coding: utf-8 -*-

import logging
import logging.config
from logging import Logger
from pathlib import Path
import yaml
from typing import Callable, Tuple, Dict

from injector import Injector, Binder, singleton

LOGGER = logging.getLogger(__name__)


class Invoker():

    logger = LOGGER.getChild('Invoker')  # type: Logger

    IS_ALREADY_LOADED_LOGGING = False

    @classmethod
    def set_logging_config(cls, logging_config_file: Path):

        if cls.IS_ALREADY_LOADED_LOGGING:
            cls.logger.warning('already initilize logging configuration. skip.')

        else:
            cls.logger.info('initilize logging configuration. start')
            with logging_config_file.open('r', encoding='utf-8') as f:
                config = yaml.load(f)

            logging.config.dictConfig(config)
            cls.IS_ALREADY_LOADED_LOGGING = True
            cls.logger.info('initilize logging configuration. end: \n%s', config)

    def __init__(self):

        self.injector = None  # type: Injector

    def initilize(self, logging_config_file: Path):

        # logging default setting.
        self.set_logging_config(logging_config_file)
        self.injector = Injector()  # type: Injector

    def invoke(self, func: Callable, args: Tuple, kwargs: Dict) -> any:

        self.logger.info('func: %s  args: %s, kwargs: %s', func, args, kwargs)
        try:
            ret = self.injector.call_with_injection(func, args=args, kwargs=kargs)
            return ret
        except Exception as e:
            self.logger.exception('unexpected error. %s', func)
            raise e
