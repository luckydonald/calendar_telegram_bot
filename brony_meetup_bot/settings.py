from datetime import datetime

from .classes import CalendarDetail, CalendarEntryText

CALENDAR_LINK = 'https://www.bronymeetup.de'
MONTHS = 36

CALENDARS = [
    CalendarDetail(
        name='Meetup',
        calendar_id=1,
        emoji='🟦',
        url=f'https://export.kalender.digital/ics/1772771/04a1b8fbed2d7268bc93/meetups.ics?past_months=0&future_months={MONTHS}',
    ),
    CalendarDetail(
        name='Convention',
        calendar_id=2,
        emoji='🟥',
        url=f'https://export.kalender.digital/ics/1772772/04a1b8fbed2d7268bc93/conventions.ics?past_months=0&future_months={MONTHS}',
    ),
    CalendarDetail(
        name='Internationale Convention',
        calendar_id=3,
        emoji='🟪',
        url=f'https://export.kalender.digital/ics/1772773/04a1b8fbed2d7268bc93/conventionsint.ics?past_months=0&future_months={MONTHS}',
    ),
    CalendarDetail(
        name='Stammtisch',
        calendar_id=4,
        emoji='🟧',
        url=f'https://export.kalender.digital/ics/1772774/04a1b8fbed2d7268bc93/stammtische.ics?past_months=0&future_months={MONTHS}',
    ),
]


example = CalendarEntryText(
    calendar=CALENDARS[0],
    name='Pinkies Chocolate Rain Party 2023',
    details="So 'ne con halt",
    start_date=datetime(2023, 8, 18),
    end_date=datetime(2023, 8, 20),
    place=None,
    link=None,
)


TELEGRAM_CHAT_ID = 123
TELEGRAM_API_KEY = "asd:asd"
POSTGRES_URL = "postgres://127.0.0.1:5432/brony_meetup_calendar_bot"