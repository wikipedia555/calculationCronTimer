import datetime
# weekday (0 = Monday)
# min. hour. day. weekday
cronString = "* 15 6 4"
nowTime = datetime.datetime.now().timestamp()
#check = (datetime.datetime.fromtimestamp(nowTime).day)
dayOfMount = [31,28,31,30,31,30,31,31,30,31,30,31]
nowTime = datetime.datetime.now().replace(microsecond=0).replace(second=0)
timerTime = nowTime.timestamp()
#print(int(nowTime.timestamp()))
#print(nowTime)
cronStringLst = cronString.split()
#print(cronStringLst)
nowTimeLst = [nowTime.minute, nowTime.hour, nowTime.day, nowTime.month, nowTime.year, nowTime.weekday()]
print(nowTimeLst)
def calcDayForWeekday(timerTime, dayTimer):
    while int(datetime.datetime.fromtimestamp(timerTime).day) != int(dayTimer):
        timerTime = timerTime + 7 * 86400

    return timerTime

for i in range(len(cronStringLst)):
    if i == 0:
        if cronStringLst[i] == "*":
            timerTime = timerTime + 60
        else:
            if int(nowTimeLst[i]) < int(cronStringLst[i]):
                timerTime = timerTime + (int(cronStringLst[i]) - int(nowTimeLst[i]))*60
            elif int(nowTimeLst[i]) > int(cronStringLst[i]):
                timerTime = timerTime + (60-int(nowTimeLst[i]) + int(cronStringLst[i])) * 60
            else:
                timerTime = timerTime + 3600
    elif i == 1:
        if cronStringLst[i] == "*":
            pass
        else:
            nowHour = datetime.datetime.fromtimestamp(timerTime).hour
            if int(nowHour) < int(cronStringLst[i]):
                timerTime = timerTime + (int(cronStringLst[i]) - nowHour) * 3600
            elif int(nowHour) > int(cronStringLst[i]):
                timerTime = timerTime + (24-nowHour + int(cronStringLst[i]))*3600
            else:
                pass
    elif i == 2:
        if(cronStringLst[i] == '*'):
            pass
        else:
            nowDay = datetime.datetime.fromtimestamp(timerTime).day
            if nowDay < int(cronStringLst[i]):
                timerTime = timerTime + (int(cronStringLst[i]) - nowDay) * 86400
            elif nowDay > int(cronStringLst[i]):
                #timerTime = timerTime + (int(dayOfMount[datetime.datetime.fromtimestamp(timerTime).month - 1]) - int(cronStringLst[i]) + nowDay) * 86400
                numberOfDays = dayOfMount[datetime.datetime.fromtimestamp(timerTime).month - 1]
                if datetime.datetime.fromtimestamp(timerTime).month == 2:
                    if datetime.datetime.fromtimestamp(timerTime).year % 4 == 0:
                        numberOfDays = numberOfDays + 1
                timerTime = timerTime + (numberOfDays - nowDay + int(cronStringLst[i])) * 86400
            else:
                pass
    elif i == 3:
        if(cronStringLst[i] == "*"):
            pass
        else:
            if(cronStringLst[i-1] == "*"):
                numberOfWeekday = datetime.datetime.fromtimestamp(timerTime).weekday() + 1
                if numberOfWeekday < int(cronStringLst[i]):
                    timerTime = timerTime + (int(cronStringLst[i]) - numberOfWeekday) * 86400
                elif numberOfWeekday > int(cronStringLst[i]):
                    timerTime = timerTime + (7 - numberOfWeekday + int(cronStringLst[i])) * 86400
                else:
                    pass
            else:
                dayTimer = int(cronStringLst[i-1])
                numberOfWeekday = datetime.datetime.fromtimestamp(timerTime).weekday() + 1
                if numberOfWeekday < int(cronStringLst[i]):
                    timerTime = timerTime + (int(cronStringLst[i]) - numberOfWeekday) * 86400
                    timerTime = calcDayForWeekday(timerTime, cronStringLst[i-1])
                elif numberOfWeekday > int(cronStringLst[i]):
                    timerTime = timerTime + (7 - numberOfWeekday + int(cronStringLst[i])) * 86400
                    timerTime = calcDayForWeekday(timerTime, cronStringLst[i-1])
                else:
                    timerTime = calcDayForWeekday(timerTime, cronStringLst[i-1])




print(datetime.datetime.fromtimestamp(timerTime).isoformat())

# print(nowTime.second)
# print(nowTime.minute)
# print(nowTime.hour)
# print(nowTime.weekday())
# print(nowTime.day)
# print(nowTime.month)
# print(nowTime.year)


