import re
import datetime
# we will try to use dateutil if is available
try:
    import dateutil.parser
    dateutil_parser = dateutil.parser.parser()
except:
    dateutil_parser = None
import sys


class FlexiDate(object):
    """Store dates as strings and present them in a slightly extended version
    of ISO8601.

    Modifications:
        * Allow a trailing qualifiers e.g. fl.
        * Allow replacement of unknown values by ? e.g. if sometime in 1800s
          can do 18??

    Restriction on ISO8601:
        * Truncation (e.g. of centuries) is *not* permitted.
        * No week and day representation e.g. 1999-W01
    """
    # pass

    def __init__(self, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, qualifier=''):
        # force = month or day or qualifier
        force = False
        self.year = self._cvt(year, rjust=4, force=force)
        self.month = self._cvt(month)
        self.day = self._cvt(day)
        self.hour = self._cvt(hour)
        self.minute = self._cvt(minute)
        self.second = self._cvt(second)
        self.microsecond = self._cvt(microsecond)
        self.qualifier = qualifier

    def _cvt(self, val, rjust=2, force=False):
        # Changed from simple check to allow 0 values for minutes or seconds
        if val is not None:
            tmp = str(val).strip()
            if tmp.startswith('-'):
                tmp = '-' + tmp[1:].rjust(rjust, '0')
            else:
                tmp = tmp.rjust(rjust, '0')
            return tmp
        elif force:
            # use '!' rather than '?' as '!' < '1' while '?' > '1'
            return rjust * '!'
        else:
            return ''

    def __str__(self):
        out = self.isoformat()
        if self.qualifier:
            # leading space is important as ensures when no year sort in right
            # order as ' ' < '1'
            out += u' [%s]' % self.qualifier
        return out

    def __repr__(self):
        return u'%s %s' % (self.__class__, self.__str__())

    def isoformat(self, strict=False):
        '''Return date in isoformat (same as __str__ but without qualifier).

        WARNING: does not replace '?' in dates unless strict=True.
        '''
        out = self.year
        # what do we do when no year ...
        for val in [self.month, self.day]:
            if not val:
                break
            out += u'-' + val
        if strict:
            out = out.replace('?', '0')

        if self.hour:
            out += u' '
            out += self.hour
            for val in [self.minute, self.second]:
                if not val:
                    break
                out += u':' + val
            if self.microsecond:
                out += u'.' + self.microsecond
        return out

    our_re_pat = '''
        (?P<year> -?[\d?]+)
        (?:
                \s* - (?P<month> [\d?]{1,2})
            (?: \s* - (?P<day> [\d?]{1,2}) )?
            (?: \s* - (?P<hour> [\d?]{1,2}) )?
            (?: \s* - (?P<minute> [\d?]{1,2}) )?
            (?: \s* - (?P<second> [\d?]{1,2}) )?
            (?: \s* - (?P<microsecond> [\d?]{1,2}) )?
        )?
        \s*
        (?: \[ (?P<qualifier>[^]]*) \])?
        '''
    our_re = re.compile(our_re_pat, re.VERBOSE)

    @classmethod
    def from_str(self, instr):
        '''Undo affect of __str__'''
        if not instr:
            return FlexiDate()

        out = self.our_re.match(instr)
        if out is None:  # no match TODO: raise Exception?
            return None
        else:
            return FlexiDate(
                out.group('year'),
                out.group('month'),
                out.group('day'),
                out.group('hour'),
                out.group('minute'),
                out.group('second'),
                out.group('microsecond'),
                qualifier=out.group('qualifier')
            )

    def as_float(self):
        '''Get as a float (year being the integer part).

        Replace '?' in year with 9 so as to be conservative (e.g. 19?? becomes
        1999) and elsewhere (month, day) with 0

        @return: float.
        '''
        if not self.year:
            return None
        out = float(self.year.replace('?', '9'))
        if self.month:
            # TODO: we are assuming months are of equal length
            out += float(self.month.replace('?', '0')) / 12.0
            if self.day:
                out += float(self.day.replace('?', '0')) / 365.0
        return out

    def as_datetime(self):
        '''Get as python datetime.datetime.

        Require year to be a valid datetime year. Default month and day to 1 if
        do not exist.

        @return: datetime.datetime object.
        '''
        year = int(self.year)
        month = int(self.month) if self.month else 1
        day = int(self.day) if self.day else 1
        hour = int(self.hour) if self.hour else 0
        minute = int(self.minute) if self.minute else 0
        second = int(self.second) if self.second else 0
        microsecond = int(self.microsecond) if self.microsecond else 0
        return datetime.datetime(year, month, day, hour, minute, second, microsecond)


def parse(date, dayfirst=True):
    '''Parse a `date` into a `FlexiDate`.

    @param date: the date to parse - may be a string, datetime.date,
    datetime.datetime or FlexiDate.

    TODO: support for quarters e.g. Q4 1980 or 1954 Q3
    TODO: support latin stuff like M.DCC.LIII
    TODO: convert '-' to '?' when used that way
        e.g. had this date [181-]
    '''
    if not date:
        return None
    if isinstance(date, FlexiDate):
        return date
    if isinstance(date, int):
        return FlexiDate(year=date)
    elif isinstance(date, datetime.datetime):
        parser = PythonDateTimeParser()
        return parser.parse(date)
    elif isinstance(date, datetime.date):
        parser = PythonDateParser()
        return parser.parse(date)
    else:  # assuming its a string
        parser = DateutilDateParser()
        out = parser.parse(date, **{'dayfirst': dayfirst})
        if out is not None:
            return out
        # msg = 'Unable to parse %s' % date
        # raise ValueError(date)
        val = 'UNPARSED: %s' % date
        val = val.encode('ascii', 'ignore')
        return FlexiDate(qualifier=val)


class DateParserBase(object):

    def parse(self, date):
        raise NotImplementedError

    def norm(self, date):
        return str(self.parse(date))


class PythonDateParser(object):

    def parse(self, date):
        return FlexiDate(date.year, date.month, date.day, 0, 0, 0, 0)


class PythonDateTimeParser(object):

    def parse(self, date):
        return FlexiDate(date.year, date.month, date.day, date.hour, date.minute, date.second, date.microsecond)


class DateutilDateParser(DateParserBase):
    _numeric = re.compile("^[0-9]+$")

    def parse(self, date, **kwargs):
        '''
        :param **kwargs: any kwargs accepted by dateutil.parse function.
        '''
        qualifiers = []
        if dateutil_parser is None:
            return None
        date = orig_date = date.strip()

        # various normalizations
        # TODO: call .lower() first
        date = date.replace('B.C.E.', 'BC')
        date = date.replace('BCE', 'BC')
        date = date.replace('B.C.', 'BC')
        date = date.replace('A.D.', 'AD')
        date = date.replace('C.E.', 'AD')
        date = date.replace('CE', 'AD')

        # deal with pre 0AD dates
        if date.startswith('-') or 'BC' in date or 'B.C.' in date:
            pre0AD = True
        else:
            pre0AD = False
        # BC seems to mess up parser
        date = date.replace('BC', '')

        # deal with circa: 'c.1950' or 'c1950'
        circa_match = re.match('([^a-zA-Z]*)c\.?\s*(\d+.*)', date)
        if circa_match:
            # remove circa bit
            qualifiers.append("Note 'circa'")
            date = ''.join(circa_match.groups())

        # deal with p1980 (what does this mean? it can appear in
        # field 008 of MARC records
        p_match = re.match("^p(\d+)", date)
        if p_match:
            date = date[1:]

        # Deal with uncertainty: '1985?'
        uncertainty_match = re.match('([0-9xX]{4})\?', date)
        if uncertainty_match:
            # remove the ?
            date = date[:-1]
            qualifiers.append('Uncertainty')

        # Parse the numbers intelligently
        # do not use std parser function as creates lots of default data
        res = dateutil_parser._parse(date, **kwargs)
        try:
            res = res[0]
        except:
            res = res
        if res is None:
            # Couldn't parse it
            return None
        # Note: Years of less than 3 digits not interpreted by
        #      dateutil correctly
        #      e.g. 87 -> 1987
        #           4  -> day 4 (no year)
        # Both cases are handled in this routine
        if res.year is None and res.day:
            year = res.day
        # If the whole date is simply two digits then dateutil_parser makes
        # it '86' -> '1986'. So strip off the '19'. (If the date specified
        # day/month then a two digit year is more likely to be this century
        # and so allow the '19' prefix to it.)
        elif self._numeric.match(date) and (len(date) == 2 or date.startswith('00')):
            year = res.year % 100
        else:
            year = res.year

        # finally add back in BC stuff
        if pre0AD:
            year = -year

        if not qualifiers:
            qualifier = ''
        else:
            qualifier = ', '.join(qualifiers) + (' : %s' % orig_date)
        return FlexiDate(year, res.month, res.day, res.hour, res.minute, res.second, res.microsecond, qualifier=qualifier)
