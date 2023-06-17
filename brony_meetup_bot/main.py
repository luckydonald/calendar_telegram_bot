# This is a sample Python script.
import asyncio
from asyncio import sleep
from datetime import datetime, timedelta

# libs
import httpx
from asyncpg import Connection
from fastorm import FastORM
from icalevents.icalevents import events as parse_events
from icalevents.icalparser import Event as CalenderEvent

from luckydonaldUtils.logger import logging
from pytgbot.bot.asynchronous import Bot
from pytgbot.exceptions import TgApiServerException

# local
from .classes import CalendarDetail
from .database.models import Event
from .settings import CALENDARS, TELEGRAM_API_KEY, TELEGRAM_CHAT_ID, POSTGRES_URL, MONTHS
from .text.helper import append_last_changed
from .environment import TELEGRAM_DISABLE_NOTIFICATIONS

logger = logging.getLogger(__name__)
bot = Bot(TELEGRAM_API_KEY)


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# Press ⌘F8 to toggle a breakpoint.
# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

async def main_looper():
    while True:
        # noinspection PyBroadException
        try:
            await main_loop()
        except Exception as e:
            logger.exception('⚠️ Error:')
        # end try
        logger.info('Loop done, waiting a minute.')
        await sleep(60)
    # end while
# end def


async def main_loop():
    logger.info(f'POSTGRES_URL: {POSTGRES_URL}, establishing connection...')
    conn = await FastORM.create_connection(database_url=POSTGRES_URL)
    events: list[tuple[CalendarDetail, CalenderEvent]] = []
    async with httpx.AsyncClient() as client:
        for calendar in CALENDARS:
            request = await client.get(calendar.url)
            ics_events = parse_events(
                string_content=request.content,
                start=datetime.now(),
                end=datetime.now() + timedelta(days=30 * MONTHS)
            )
            for event in ics_events:
                events.append((calendar, event))
            # end def
        # end for
    # end with
    events.sort(key=lambda x: x[1].start)
    for calendar, event in events:
        db_event = await Event.get(conn=conn, uid=str(event.uid))
        if db_event is None:
            db_event = Event.from_ical(ical=event, calendar=calendar.calendar_id, new_uid=False)
            await db_event.insert(conn=conn)
            await send_to_telegram(conn, db_event, calendar)
        else:
            id = db_event.uid
            changes = db_event.get_changes()
            logger.info(f'Changes Event[{id}]: {changes}')
            db_event.apply_ical(ical=event, calendar=calendar.calendar_id)
            changes = db_event.get_changes()
            for key, new in changes.items():
                changes[key] = (db_event._database_cache[key], new)
            # end for
            logger.info(f'Changes Event[{id}]: {changes}')
            if changes:
                await db_event.update(conn=conn)
                await send_to_telegram(conn, db_event, calendar)
            # end if
        # end if
    # end for
# end def


async def send_to_telegram(conn: Connection, db_event: Event, calendar: CalendarDetail):
    text = str(db_event.to_entry_text(calendar))
    shared_params = dict(
        # chat_id=TELEGRAM_CHAT_ID,  # this one differs
        text=append_last_changed(text),
        parse_mode='html',
        disable_web_page_preview=not db_event.url,
        reply_markup=None,
        entities=None,
    )
    for i in range(10):
        try:
            if not db_event.telegram_channel_id and not db_event.telegram_message_id:
                msg = await bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    **shared_params,
                    disable_notification=TELEGRAM_DISABLE_NOTIFICATIONS,
                    protect_content=False,
                )
                db_event.telegram_channel_id = msg.chat.id
                db_event.telegram_message_id = msg.message_id
                db_event.telegram_text = text
                await db_event.update(conn=conn)
                break
            elif text != db_event.telegram_text:
                await bot.edit_message_text(
                    chat_id=db_event.telegram_channel_id,
                    **shared_params,
                    message_id=db_event.telegram_message_id,
                    inline_message_id=None,
                )
                db_event.telegram_text = text
                await db_event.update(conn=conn)
                break
            else:
                break
            # end if
        except TgApiServerException as e:
            logger.warning(e.response.json())
            if e.error_code == 429:
                from httpx import Response
                response: Response = e.response

                await sleep(response.json()['parameters']['retry_after'])
                continue
            # end if
            if e.error_code == 400 and 'message is not modified' in e.description:
                break
            # end if
        # end try
    # end try
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


def start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_looper())
# end def


if __name__ == '__main__':
    start()
# end def
