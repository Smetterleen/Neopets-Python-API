from datetime import tzinfo, timedelta, datetime, date, time
        
class NST(tzinfo):
    
    def utcoffset(self, dt):
        return timedelta(hours=-8)

    def tzname(self, dt):
        return "NST"

    def dst(self, dt):
        return timedelta(0)    

timezone = NST()

def NST_date():
    return datetime.now(timezone).date()

def NST_time():
    return datetime.now(timezone)

def NST_epoch():
    return datetime(2000,1,1,tzinfo=timezone)

def NST_datetime(given_datetime):
    return datetime(given_datetime.year, given_datetime.month, given_datetime.day, given_datetime.hour,
                    given_datetime.minute, given_datetime.second, tzinfo=timezone)
    
def NST_tomorrow():
    return datetime.combine(date.today() + timedelta(days=1), time(0,5,0,tzinfo=timezone))

def parse_time_string(datestring):
    temptime = datetime.strptime(datestring, '%X%x')
    return datetime(temptime.year, temptime.month, temptime.day, temptime.hour, temptime.minute, temptime.second, tzinfo=timezone)
    
def get_time_string(given_datetime):
    return given_datetime.strftime('%X%x')
