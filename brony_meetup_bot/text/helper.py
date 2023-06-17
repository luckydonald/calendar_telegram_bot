#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from luckydonaldUtils.logger import logging

from .unicode_fonts import replace, Fonts

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if


def append_last_changed(text: str, time: datetime|None = None) -> str:
    if not time:
        time: datetime = datetime.now()
    # end if
    time: str = time.strftime('%d.%m.%y %H:%M:%S')
    time: str = replace(time, font=Fonts.ITALIC)
    return f"{text}\n\n<i>Letztes Update: <code>{time}</code></i>"
