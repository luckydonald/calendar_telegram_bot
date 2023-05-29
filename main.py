# This is a sample Python script.
import asyncio
from asyncio import sleep
from datetime import datetime, timedelta
from typing import NamedTuple

# libs
import httpx
from icalevents.icalevents import events as parse_events
from icalevents.icalparser import Event as FileEvent
from luckydonaldUtils.logger import logging

logger = logging.getLogger(__name__)


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# Press ⌘F8 to toggle a breakpoint.
# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

class CalendarDetail(NamedTuple):
    name: str
    calendar_id: int
    emoji: str
    url: str

CALENDARS = [
]

class Event(FileEvent):
    uid: int
    calendar: int
    summary: None | str
    description: None | str
    start: None | datetime
    end: None | datetime
    all_day: bool
    transparent: bool
    recurring: bool
    location: None | str # ???
    private: bool
    created: None
    last_modified: None
    sequence: None
    recurrence_id: None
    attendee: None
    organizer: None
    categories: None
    floating: None
    status: None
    url: None


async def main_loop():
    async with httpx.AsyncClient() as client:
        for calendar in CALENDARS:
            request = await client.get(calendar.url)
            events = parse_events(
                string_content=request.content,
                start=datetime.now(),
                end=datetime.now() + timedelta(days=30*6)
            )
            for event in events
    # end with
# end def


async def main():
    while True:
        try:
            await main_loop()
        except Exception as e:
            logger.debug(f'⚠️ Error: ', exc_info=e)
            await sleep(5)
        # end try
    # end while
# end def


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_loop())


