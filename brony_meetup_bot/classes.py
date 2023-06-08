from dataclasses import dataclass
from datetime import date, datetime
from html import escape
from textwrap import dedent

from luckydonaldUtils.text import convert_to_underscore

from .utils import format_date_interval


class TagifyNameMixin:
    name: str

    @property
    def tagified(self):
        return convert_to_underscore(self.name.replace(' ', '_')).replace('__', '_').lower()
    # end def
# end class#


@dataclass
class CalendarDetail(TagifyNameMixin):
    name: str
    calendar_id: int
    emoji: str
    url: str

    def __str__(self):
        return self.name
    # end def
# end class


@dataclass
class CalendarEntryText(TagifyNameMixin):
    calendar: CalendarDetail
    name: str | None
    start_date: date | datetime
    end_date: date | datetime
    place: str | None
    link: str | None
    details: str | None

    NO_TITLE = 'Nicht verraten'
    NO_PLACE = 'Noch unbekannt'
    NO_LINK = 'Noch keinen'
    NO_DETAILS = 'Unbekannt'

    TEMPLATE = dedent("""
        {emoji} <b><u>{name}</u></b> {emoji}
        <b>Kalender:</b> {calendar}
        <b>Datum:</b> {date}
        <b>Ort:</b> {place}
        <b>Link:</b> {link}
        <b>Details:</b> {details}
        
        {tags}
    """).strip()

    @property
    def formatted_date_range(self) -> str:
        return format_date_interval(self.start_date, self.end_date)
    # end def

    def __str__(self):
        from .settings import CALENDAR_LINK

        return self.TEMPLATE.format(
            calendar=f'<a href="{ escape(CALENDAR_LINK) }">{ escape(self.calendar.name) }</a>',
            name=escape(self.name or self.NO_TITLE),
            date=escape(self.formatted_date_range),
            place=escape(self.place or self.NO_PLACE),
            link=escape(self.link or self.NO_LINK),
            details=escape(self.details or self.NO_DETAILS),
            emoji=f'<a href="{ escape(self.link) }">{ escape(self.calendar.emoji) }</a>' if self.link else escape(self.calendar.emoji),
            tags=" ".join(
                dict.fromkeys(  # <- dedupe
                    f'#{escape(str(tag))}'
                    for tag in
                    [
                        self.calendar.tagified,
                        self.start_date.year,
                        self.end_date.year,
                        self.tagified.removesuffix(f'_{self.end_date.year}'),
                    ]
                )
            ),
        )
    # end def
# end class

