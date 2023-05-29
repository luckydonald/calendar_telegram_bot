from datetime import datetime


def time_if_non_zero(
        date: datetime,
        prefix: str = ' ', suffix: str = '',
        default: str = '',
) -> str:
    """
    Returns a formatted time if it's not midnight.

    :param date: the date to print the time of
    :param prefix: text to put in front of the date (if not midnight)
    :param suffix: text to append after the date (if not midnight)
    :param default: text to put instead of a date (if midnight)
    :return: formatted time if it's not midnight.
    """
    if time_is_zero(date):
        return prefix + date.strftime('%H:%M:%S') + suffix
    # end if
    return default
# end def

def times_if_non_zero(
        start: datetime,
        end: datetime,
        *,
        prefix: str = ' (', suffix: str = ')',
        middle: str = '-'
) -> str:
    if not time_is_zero(start) or not time_is_zero(end):
        return prefix + start.strftime('%H:%M') + middle + end.strftime('%H:%M') + suffix
    # end if
    return ''
# end def


def time_is_zero(date: datetime) -> bool:
    return date.hour != 0 or date.minute != 0 or date.second != 0
# end def


def format_date_interval(start: datetime, end: datetime) -> str:
    """
    Return a string format of that date interval.

    - 24.12.1999
    - 24.12.1999 (12:34)
    - 24.12.1999 (00:00-12:34)
    - 24.-25.12.1999
    - 24.-25.12.1999 (12:20-12:10)
    - 24.11.-23.12.1999
    - 24.11.-23.12.1999 (12:20-12:10)
    - 31.12.1999 - 01.01.2000
    - 31.12.1999 (12:10) - 01.01.2000
    - 31.12.1999 (12:10) - 01.01.2000 (12:09)
    - 31.12.1999 - 01.01.2000 (12:09)

    :param start:
    :param end:
    :return:
    """
    if start.year == end.year:
        if start.month == end.month:
            if start.day == end.day:
                if start == end:
                    # everything equal
                    # 24.12.1999
                    # 24.12.1999 (12:34)
                    return end.strftime('%d.%m.%Y') + time_if_non_zero(end)
                else:
                    # time differs
                    # 24.12.1999 (00:00-12:34)
                    return end.strftime('%d.%m.%Y') + times_if_non_zero(start, end)
            else:
                # day differs
                # 24.-25.12.1999
                # 24.-25.12.1999 (12:20-12:10)
                return start.strftime('%d.') + '-' + end.strftime('%d.%m.%Y') + times_if_non_zero(start, end)
        else:
            # month differs
            # 24.11.-23.12.1999
            # 24.11.-23.12.1999 (12:20-12:10)
            return start.strftime('%d.%m.') + '-' + end.strftime('%d.%m.%Y') + times_if_non_zero(start, end)
    else:
        # year differs
        if time_is_zero(start) and time_is_zero(end):
            # year differs, midnight
            # 31.12.1999-01.01.2000
            return start.strftime('%d.%m.%Y') + ' - ' + end.strftime('%d.%m.%Y')
        else:
            # year differs, non-midnight
            # 31.12.1999 (12:10) - 01.01.2000
            # 31.12.1999 (12:10) - 01.01.2000 (12:09)
            # 31.12.1999 - 01.01.2000 (12:09)
            return start.strftime('%d.%m.%Y') + time_if_non_zero(start, prefix=' (', suffix=')') + ' - ' + end.strftime('%d.%m.%Y') + time_if_non_zero(end, prefix=' (', suffix=')')
    # end if
# end def
