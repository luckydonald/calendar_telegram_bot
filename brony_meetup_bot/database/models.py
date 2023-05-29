from datetime import datetime
from random import randint
from typing import Self

from icalevents.icalparser import Event as CalenderEvent
from fastorm import FastORM


class TypedCalenderEvent(CalenderEvent):
    uid: int
    calendar: int
    summary: None | str
    description: None | str
    start: None | datetime
    end: None | datetime
    all_day: bool
    transparent: bool
    recurring: bool
    location: None | str  # ???
    private: bool
    created: None | datetime
    last_modified: None | datetime
    sequence: None | int

    # Spec defines that if DTSTART is a date RECURRENCE-ID also is to be interpreted as a date
    recurrence_id: None | str
    attendee: None | str
    organizer: None | str
    categories: None | list[str]
    floating: None | bool
    status: None | str
    url: None | str
# end class


class Event(TypedCalenderEvent, FastORM):
    _ignored_fields = []
    _primary_keys = ['uid']
    _automatic_fields = []
    _table_name='event'
# end class
