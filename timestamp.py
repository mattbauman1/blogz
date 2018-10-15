from calendarkeeper import CalendarKeeper

class Timestamp:
    def __init__(self, timestamp):
        self.timestamp = str(timestamp)

    def getmonth(self):
        return self.timestamp[5] + self.timestamp[6]

    def getdate(self):
        return self.timestamp[8] + self.timestamp[9]

    def getyear(self):
         return self.timestamp[0] + self.timestamp[1] + self.timestamp[2] + self.timestamp[3]
    
    def gethour(self):
        return self.timestamp[11] + self.timestamp[12]

    def getminute(self):
        return self.timestamp[14] + self.timestamp[15]

    def getsecond(self):
        return self.timestamp[17] + self.timestamp[18]

    def totalstamp(self):
        return int(self.getmonth()) + int(self.getdate()) + int(self.getyear()) + int(self.gethour()) + int(self.getminute()) + int(self.getsecond())

    def timestampformatter(self):
        month = int(self.getmonth())
        date = int(self.getdate())
        year = int(self.getyear())
        hour = int(self.gethour())
        hour = hour - 5
        if hour < 0:
            date = date - 1
            if date == 0:
                month = month - 1
                if month == 0:
                    month = 12
                    year = year - 1
                date = CalendarKeeper(month, year).getdateforendof()
        hour = hour % 24
        minute = self.getminute()
        second = self.getsecond()
        if hour == 0:
            hour = 12
            ampm = "AM"
        else:
            if hour != 12:
                if hour < 12:
                    ampm = "AM"
                else:
                    ampm = "PM"
                hour = int(hour) % 12
            else:
                ampm = "PM"
        return str(month) + '/' + str(date) + '/' + str(year) + '@' +  str(hour) + ':' + minute + ':' + second + " " + ampm + " CST"
