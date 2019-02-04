# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="invoker",
    version="1.0.0",
    description='',
    pakages=find_packages(),
    install_requires=["injector==0.14.1", "pyyaml>=4.2b1"],
    extras_require={
        "develop": ["autopep8", "pep8"]
    },
    entry_points={
        "console_scripts": [
            "invoker = invoker.cmd:execute"
        ],
    }
)
