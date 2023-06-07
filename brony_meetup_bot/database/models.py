from datetime import datetime
from random import randint
from typing import Self

from icalevents.icalparser import Event as CalenderEvent
from fastorm import FastORM

from brony_meetup_bot.classes import CalendarEntryText, CalendarDetail


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

    @classmethod
    def from_ical(
        cls,
        ical: CalenderEvent,
        new_uid: bool | str = False,
        new_start: None | datetime = None,
    ) -> Self:
        """
        Create a new database event equal to the given one with optional new start date.

        :param ical: the event to copy.
        :param new_uid: UID of new event.
        :param new_start: new start date.
        :return: new event.
        """
        new = cls()
        return new.apply_ical(ical=ical, new_uid=new_uid, new_start=new_start)
    # end def

    def apply_ical(
        self,
        ical: CalenderEvent,
        new_uid: bool | str = False,
        new_start: None | datetime = None,
    ) -> Self:
        """
        Apply data from the given one, with optional new start date.

        :param ical: the event to copy.
        :param new_uid: UID of new event.
        :param new_start: new start date.
        :return: new event.
        """

        # basically the same as `Event.copy_to()`, but using `cls()` instead of `Event()`
        if not new_start:
            new_start = ical.start
        # end if

        uid = ical.uid
        if isinstance(new_uid, bool) and new_uid:
            uid = "%s_%d" % (ical.uid, randint(0, 1000000))
        # end if

        self.summary = ical.summary
        self.description = ical.description
        self.start = new_start

        if ical.end:
            duration = ical.end - ical.start
            self.end = new_start + duration
        # end if

        self.all_day = ical.all_day
        self.recurring = ical.recurring
        self.location = ical.location
        self.attendee = ical.attendee
        self.organizer = ical.organizer
        self.private = ical.private
        self.transparent = ical.transparent
        self.uid = uid
        self.created = ical.created
        self.last_modified = ical.last_modified
        self.categories = ical.categories
        self.floating = ical.floating
        self.status = ical.status
        self.url = ical.url

        return self
    # end def
# end class


class Event(TypedCalenderEvent, FastORM):
    _ignored_fields = []
    _primary_keys = ['uid']
    _automatic_fields = []
    _table_name = 'event'

    telegram_channel_id: None | int
    telegram_message_id: None | int

    def apply_ical(
        self,
        ical: CalenderEvent,
        new_uid: bool | str = False,
        new_start: None | datetime = None,
    ) -> Self:
        """
        Apply data from the given one, with optional new start date.

        :param ical: the event to copy.
        :param new_uid: UID of new event.
        :param new_start: new start date.
        :return: new event.
        """
        super().from_ical(ical, new_uid, new_start)
        # now we could add values which are required in the database but are not part of the parent class.
        return self
    # end def

    def to_entry_text(self, calendar: CalendarDetail):
        return CalendarEntryText(
            calendar=calendar,
            name=self.summary,
            start_date=self.start,
            end_date=self.end,
            place=self.location,
            link=self.url,
        )
    # end def
# end class
