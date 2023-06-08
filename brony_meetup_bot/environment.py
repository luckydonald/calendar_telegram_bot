# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging
import os
from luckydonaldUtils.interactions import string_is_yes

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)

# generic telegram setting
TELEGRAM_API_KEY: str = os.getenv('TELEGRAM_API_KEY', None)
assert(TELEGRAM_API_KEY is not None)  # TELEGRAM_API_KEY environment variable

TELEGRAM_CHAT_ID: str = os.getenv('TELEGRAM_CHAT_ID', None)
assert(TELEGRAM_CHAT_ID is not None)  # TELEGRAM_CHAT_ID environment variable
TELEGRAM_CHAT_ID: int = int(TELEGRAM_CHAT_ID)

# database settings
POSTGRES_USER: str = os.getenv('POSTGRES_USER', None)
assert POSTGRES_USER is not None  # $POSTGRES_USER environment variable

POSTGRES_PASS: str = os.getenv('POSTGRES_PASS', None)
assert POSTGRES_PASS is not None  # $POSTGRES_PASS environment variable

POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', None)
assert POSTGRES_HOST is not None  # $POSTGRES_HOST environment variable

POSTGRES_DB: str = os.getenv('POSTGRES_DB', None)
assert POSTGRES_DB is not None  # $POSTGRES_DB environment variable
