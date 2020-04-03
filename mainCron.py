import datetime

class Cron:

    def __init__(self, cronString):

        self.dayOfMonth = [31,28,31,30,31,30,31,31,30,31,30,31]
        self.cronStringLst = cronString.split()


    def checkValue(self, value):
        if value == "*" or value.isdigit():
            al = value.isdigit()
            return al
        else:
            return "err"

    def checkErr(self, errFlag, a, b, value):
        if self.checkValue(value) == True:
            if not (a <= int(value) <= b):
                errFlag = True
        elif self.checkValue(value) == "err":
            errFlag = True
        else:
            pass

        return errFlag

    def enumerationCheckErr(self, cronStringLst, errFlag):
        for i in range(len(cronStringLst)):
            if i == 0:
                errFlag = self.checkErr(errFlag, 0, 59, cronStringLst[i])
            elif i == 1:
                errFlag = self.checkErr(errFlag, 0, 23, cronStringLst[i])
            elif i == 2:
                errFlag = self.checkErr(errFlag, 1, 31, cronStringLst[i])
            elif i == 3:
                errFlag = self.checkErr(errFlag, 1, 7, cronStringLst[i])
            else:
                pass

        print(errFlag)
        return(errFlag)

    def zeroMinutes(self, timerTime):
        if self.cronStringLst[0] == "*":
            timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).minute * 60

        return timerTime

    def zeroHour(self, timerTime):
        if self.cronStringLst[1] == "*":
            timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).hour * 3600

        return timerTime


    def calcDayForWeekday(self, timerTime, dayTimer):
        while int(datetime.datetime.fromtimestamp(timerTime).day) != int(dayTimer):
            timerTime = timerTime + 7 * 86400

        return timerTime


    def calcDayForMonth (self, timerTime, day):
        if int(self.dayOfMonth[datetime.datetime.fromtimestamp(timerTime).month - 1]) > int(day):
            pass
        else:
            today = datetime.datetime.fromtimestamp(timerTime).day
            timerTime = timerTime + (int(self.dayOfMonth[datetime.datetime.fromtimestamp(timerTime).month - 1]) - today + 1) * 86400
            while int(self.dayOfMonth[datetime.datetime.fromtimestamp(timerTime).month - 1]) < int(day):
                timerTime = timerTime + int(self.dayOfMonth[datetime.datetime.fromtimestamp(timerTime).month - 1]) * 86400

        return timerTime

    def calcCron(self, nowTime):
        timerTime = nowTime.timestamp()
        nowTimeLst = [nowTime.minute, nowTime.hour, nowTime.day, nowTime.month, nowTime.year, nowTime.weekday()]
        for i in range(len(self.cronStringLst)):
            if i == 0:
                if self.cronStringLst[i] == "*":
                    if self.cronStringLst[i + 1] == "*":
                        timerTime = timerTime + 60
                    else:
                        if int(datetime.datetime.fromtimestamp(timerTime).hour) == int(self.cronStringLst[i+1]):
                            timerTime = timerTime + 60
                        else:
                            timerTime = timerTime - ((int(datetime.datetime.fromtimestamp(timerTime).minute)) * 60)
                else:
                    if int(nowTimeLst[i]) < int(self.cronStringLst[i]):
                        timerTime = timerTime + (int(self.cronStringLst[i]) - int(nowTimeLst[i]))*60
                    elif int(nowTimeLst[i]) > int(self.cronStringLst[i]):
                        timerTime = timerTime + (60-int(nowTimeLst[i]) + int(self.cronStringLst[i])) * 60
                    else:
                        timerTime = timerTime + 3600
            elif i == 1:
                if self.cronStringLst[i] == "*":
                    pass
                else:
                    nowHour = datetime.datetime.fromtimestamp(timerTime).hour
                    if int(nowHour) < int(self.cronStringLst[i]):
                        timerTime = timerTime + (int(self.cronStringLst[i]) - nowHour) * 3600
                    elif int(nowHour) > int(self.cronStringLst[i]):
                        timerTime = timerTime + (24-nowHour + int(self.cronStringLst[i]))*3600
                    else:
                        pass
            elif i == 2:
                if(self.cronStringLst[i] == '*'):
                    pass
                else:
                    nowDay = datetime.datetime.fromtimestamp(timerTime).day
                    if nowDay < int(self.cronStringLst[i]):
                        timerTime = self.calcDayForMonth(timerTime, self.cronStringLst[i])
                        timerTime = timerTime + (int(self.cronStringLst[i]) - nowDay) * 86400
                        timerTime = self.zeroHour(timerTime)
                        timerTime = self.zeroMinutes(timerTime)
                    elif nowDay > int(self.cronStringLst[i]):
                        timerTime = self.calcDayForMonth(timerTime, self.cronStringLst[i])
                        numberOfDays = self.dayOfMonth[datetime.datetime.fromtimestamp(timerTime).month - 1]
                        timerTime = self.zeroHour(timerTime)
                        timerTime = self.zeroMinutes(timerTime)
                        if datetime.datetime.fromtimestamp(timerTime).month == 2:
                            if datetime.datetime.fromtimestamp(timerTime).year % 4 == 0:
                                numberOfDays = numberOfDays + 1
                        timerTime = timerTime + (numberOfDays - nowDay + int(self.cronStringLst[i])) * 86400
                    else:
                        pass
            elif i == 3:
                if(self.cronStringLst[i] == "*"):
                    pass
                else:
                    if(self.cronStringLst[i-1] == "*"):
                        numberOfWeekday = datetime.datetime.fromtimestamp(timerTime).weekday() + 1
                        if numberOfWeekday < int(self.cronStringLst[i]):
                            timerTime = timerTime + (int(self.cronStringLst[i]) - numberOfWeekday) * 86400
                        elif numberOfWeekday > int(self.cronStringLst[i]):
                            timerTime = timerTime + (7 - numberOfWeekday + int(self.cronStringLst[i])) * 86400
                        else:
                            pass
                    else:
                        #dayTimer = int(self.cronStringLst[i-1])
                        numberOfWeekday = datetime.datetime.fromtimestamp(timerTime).weekday() + 1
                        if numberOfWeekday < int(self.cronStringLst[i]):
                            timerTime = timerTime + (int(self.cronStringLst[i]) - numberOfWeekday) * 86400
                            timerTime = self.calcDayForWeekday(timerTime, self.cronStringLst[i-1])
                        elif numberOfWeekday > int(self.cronStringLst[i]):
                            timerTime = timerTime + (7 - numberOfWeekday + int(self.cronStringLst[i])) * 86400
                            timerTime = self.calcDayForWeekday(timerTime, self.cronStringLst[i-1])
                        else:
                            timerTime = self.calcDayForWeekday(timerTime, self.cronStringLst[i-1])




        print(datetime.datetime.fromtimestamp(timerTime).isoformat())
        return timerTime

if __name__ == "__main__":
    cronStr = "* 11 3 5"
    errFlag = False
    cron = Cron(cronStr)
    errFlag = cron.enumerationCheckErr(cron.cronStringLst, errFlag)
    if errFlag:
        print("err")
    else:
        nowTime = datetime.datetime.now().replace(microsecond=0).replace(second=0)
        cron.calcCron(nowTime)
