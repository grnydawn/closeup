# -*- coding: UTF-8 -*-
"""Implement logging functions."""

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
_logger = logging.getLogger('closeup')

def debug(msg, *args, **kwargs):
    _logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    _logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    _logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    _logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    _logger.critical(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    _logger.exception(msg, *args, **kwargs)
