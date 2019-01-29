# -*- coding: utf-8 -*-

import importlib
import logging
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Callable

import yaml

from . import InvokerContext

LOGGER = logging.getLogger(__name__)


def define_args_parser() -> ArgumentParser:

    parser = ArgumentParser(description="invoke specify function with DI")

    parser.add_argument('log_config', help='specify logging.yml path')
    parser.add_argument('app_config', help='specify configuration.yml path')
    parser.add_argument('invoke_options', help='specify invoke.yml path')

    return parser


def execute():

    parser = define_args_parser()  # type* ArgumentParser
    args = parser.parse_args()

    invoker = InvokerContext([args.app_config], args.log_config)

    with Path(args.invoke_options).open('r', encoding='utf-8') as f:
        invoke_options = yaml.load(f)

    qualified_token = invoke_options['invoke'].split('.')  # type: str
    _package = '.'.join(qualified_token[:-1])
    _callable = qualified_token[-1]

    _func = importlib.import_module(_callable, package=_module)  # type: Callable

    kwargs = invoke_options.get('args', {})
    try:
        ret = invoker.invoke(_func, kwargs-kwargs)
    except Exception as e:
        LOGGER.exception('invoke function internal error.')
        sys.exit(10)

    sys.exit(0)


if __name__ == '__main__':
    execute()
