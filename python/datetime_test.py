import datetime


def GetWeekNumberLastDate(year, weekNumber):
    yearFirstDate = datetime.datetime(year, 1, 1)
    currentDate = yearFirstDate + datetime.timedelta(weeks=weekNumber - 1)
    targetDate = currentDate - datetime.timedelta(days=currentDate.isoweekday() % 7 - 7)
    results = targetDate.strftime('%Y%m%d')
    return results

def GetWeekNumberFirstDate(year, weekNumber):
    yearFirstDate = datetime.datetime(year, 1, 1)
    currentDate = yearFirstDate + datetime.timedelta(weeks=weekNumber - 1)
    targetDate = currentDate - datetime.timedelta(days=currentDate.isoweekday() % 7 - 1)
    results = targetDate.strftime('%Y%m%d')
    return results

print(GetWeekNumberFirstDate(2019, 1)) # 2018-12-31 00:00:00

print(GetWeekNumberLastDate(2019, 1)) # 2019-01-07 00:00:00









