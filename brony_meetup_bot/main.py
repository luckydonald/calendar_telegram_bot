# This is a sample Python script.
import asyncio
from asyncio import sleep
from datetime import datetime, timedelta

# libs
import httpx
from icalevents.icalevents import events as parse_events
from luckydonaldUtils.logger import logging

# local
from .classes import CalendarDetail, CalendarEntryText
from .database.models import Event

logger = logging.getLogger(__name__)


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# Press ⌘F8 to toggle a breakpoint.
# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/



CALENDARS = [
    CalendarDetail(
        name='Meetup',
        calendar_id=1,
        emoji='🟦',
        url='https://export.kalender.digital/ics/1772771/04a1b8fbed2d7268bc93/meetups.ics?past_months=3&future_months=36',
    ),
    CalendarDetail(
        name='Convention',
        calendar_id=2,
        emoji='🟥',
        url='https://export.kalender.digital/ics/1772772/04a1b8fbed2d7268bc93/conventions.ics?past_months=3&future_months=36',
    ),
    CalendarDetail(
        name='Internationale Convention',
        calendar_id=3,
        emoji='🟪',
        url='https://export.kalender.digital/ics/1772773/04a1b8fbed2d7268bc93/conventionsint.ics?past_months=3&future_months=36',
    ),
    CalendarDetail(
        name='Stammtisch',
        calendar_id=4,
        emoji='🟧',
        url='https://export.kalender.digital/ics/1772774/04a1b8fbed2d7268bc93/stammtische.ics?past_months=3&future_months=36',
    ),
]


example = CalendarEntryText(
    calendar=CALENDARS[0],
    name='Pinkies Chocolate Rain Party 2023',
    date='18.-20.08.2023',
    place=None,
    link=None,
)







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


