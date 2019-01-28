# -*- coding: utf-8 -*-

import logging
import logging.config
from pathlib import Path
import yaml

from injector import Injector, Binder, singleton

LOGGER = logging.getLogger(__name__)

class InvokeInitilizer():

  logger = LOGGER.getChild('InvokeInitilizer')
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
      cls.IS_ALREADY_LOADED_LOGGING = False
      cls.logger.info('initilize logging configuration. end: %s', config)
      

  def __init__(self):
    
    self.injector = None # type: Injector

  def initilize(self):

    
      
    

