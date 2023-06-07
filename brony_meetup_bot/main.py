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
from pytgbot.bot.asynchronous import Bot

# local
from .classes import CalendarDetail, CalendarEntryText
from .database.models import Event
from .settings import CALENDARS, TELEGRAM_API_KEY, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)
bot = Bot(TELEGRAM_API_KEY)


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
                    await send_to_telegram(conn, db_event, calendar)
                else:
                    db_event.apply_ical(ical=event)
                    changes = db_event.get_changes()
                    logger.debug(f'Changes: {changes}')
                    await db_event.update(conn=conn)
                    await send_to_telegram(conn, db_event, calendar)
                # end if
            # end for
        # end for
    # end with
# end def


async def send_to_telegram(conn: Connection, db_event: Event, calendar: CalendarDetail):
    text = db_event.to_entry_text(calendar)
    shared_params = dict(
        # chat_id=TELEGRAM_CHAT_ID,  # this one differs
        text=text,
        parse_mode='html',
        disable_web_page_preview=False,
        reply_markup=None,
        entities=None,
    )
    if not db_event.telegram_channel_id and not db_event.telegram_message_id:
        msg = await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            **shared_params,
            disable_notification=False,
            protect_content=False,
        )
        db_event.telegram_channel_id = msg.chat.id
        db_event.telegram_message_id = msg.message_id
        await db_event.update(conn=conn)
    else:
        await bot.edit_message_text(
            chat_id=db_event.telegram_channel_id,
            **shared_params,
            message_id=db_event.telegram_message_id,
            inline_message_id=None,
            disable_web_page_preview=False,
        )
        await db_event.update(conn=conn)
    # end if
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


