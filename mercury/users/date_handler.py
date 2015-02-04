import datetime

class DateHandler:
    def __init__(self):
        self.date=None
        self.date_string = None

    def to_string(self, date=None):
        if not date:
            date = self.date
        if date:
            self.date_string = '%d-%d-%d %d:%d:%d' % (date.year,
                                                      date.month,
                                                      date.day,
                                                      date.hour,
                                                      date.month,
                                                      date.second)
        return self.date_string

    def to_date(self, date_string=None):
        if not date_string:
            date_string = self.date_string
        if date_string and date_string != '':
            date_list = self.parse_date_string()
            if date_list:
                self.date = datetime.datetime(year=date_list[0],
                                              month=date_list[1],
                                              day=date_list[2],
                                              hour=date_list[3],
                                              minute=date_list[4],
                                              second=date_list[5])
        return self.date

    def parse_date_string(self):
        if self.date_string and self.date_string != '':
            parts = self.date_string.split(' ')
            date_string, time_string = parts[0], parts[1]
            date_parts = date_string.split('-')
            time_parts = time_string.split(':')
            date_list = []
            for part in date_parts:
                date_list.append(int(part))
            for part in time_parts:
                date_list.append((int(part)))
            return date_list
        return None