# This is a sample Python script.
import asyncio
from asyncio import sleep
from datetime import datetime, timedelta

# libs
import httpx
from asyncpg import Connection
from fastorm import FastORM
from icalevents.icalevents import events as parse_events
from luckydonaldUtils.logger import logging

# local
from .classes import CalendarDetail, CalendarEntryText
from .database.models import Event
from .settings import CALENDARS

logger = logging.getLogger(__name__)


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# Press ⌘F8 to toggle a breakpoint.
# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


async def main_loop():
    conn = await FastORM.get_connection(database_url="")
    async with httpx.AsyncClient() as client:
        for calendar in CALENDARS:
            request = await client.get(calendar.url)
            events = parse_events(
                string_content=request.content,
                start=datetime.now(),
                end=datetime.now() + timedelta(days=30*6)
            )
            for event in events:
                db_event = await Event.get(conn=conn, uid=event.uid)
                if db_event is None:
                    db_event = Event.from_ical(ical=event)
                    await db_event.insert(conn=conn)
                    await print_new(conn, db_event, calendar)
                else:
                    db_event.apply_ical(ical=event)
                    await print_change(conn, db_event, calendar)
                    await db_event.update(conn=conn)
                # end if
    # end with
# end def


async def print_new(conn: Connection, db_event: Event, calendar: CalendarDetail):
    pass
# end def


async def print_change(conn: Connection, db_event: Event, calendar: CalendarDetail):
    pass
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


