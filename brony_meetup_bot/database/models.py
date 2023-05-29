from datetime import datetime

from icalevents.icalparser import Event as FileEvent
from fastorm import FastORM

class Event(FileEvent, FastORM):
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
    sequence: None
    recurrence_id: None
    attendee: None | str
    organizer: None | str
    categories: None
    floating: None
    status: None
    url: None | str
# end class
