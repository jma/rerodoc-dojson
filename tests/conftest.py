# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import pytest
import os


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     help="Run also slow tests")
