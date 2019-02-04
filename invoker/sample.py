# -*- coding: utf-8 -*-

import logging
from injector import inject
from invoker.utils import AliasDict

LOGGER = logging.getLogger(__name__)


@inject
def sample_function(config: AliasDict,
                    key: str):

    LOGGER.info('key: %s, value: %s', key, config.get(key))
