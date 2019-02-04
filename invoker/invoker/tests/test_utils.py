# -*- coding: utf-8 -*-

from unittest import TestCase
import logging

from invoker.utils import AliasDict
from logging import StreamHandler

LOGGER = logging.getLogger(__name__)
sh = StreamHandler()
sh.setLevel(logging.DEBUG)
LOGGER.addHandler(sh)
LOGGER.setLevel(logging.DEBUG)


class TestAliasDict(TestCase):

    def test_replace(self):

        config = AliasDict({
            'test': {
                'base': 'aaa/bbb',
                'concat': "${test.base}/ccc"
            }
        })

        self.assertEqual(config.get('test.concat'), 'aaa/bbb/ccc')
