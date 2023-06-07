from datetime import datetime

from .classes import CalendarDetail, CalendarEntryText


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
    start_date=datetime(2023, 8, 18),
    end_date=datetime(2023, 8, 20),
    place=None,
    link=None,
)