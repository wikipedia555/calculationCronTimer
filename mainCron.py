import datetime

class Cron:

    def __init__(self, cronString):

        self.dayOfMonth = [31,28,31,30,31,30,31,31,30,31,30,31]
        self.cronStringLst = cronString.split()
        print(self.cronStringLst)

    def checkInterval (self, value,a,b):
        vlst = value.split('-')
        if vlst[0].isdigit() and vlst[1].isdigit() and len(vlst) == 2:
            if (a <= int(vlst[0]) <= b) and (a <= int(vlst[1]) <= b) and int(vlst[0]) <= int(vlst[1]):
                return False
            else:
                return True

        vlst = value.split('/')
        if vlst[0] == "*" and vlst[1].isdigit() and len(vlst) == 2:
            if a <= int(vlst[1]) <= b:
                return False
            else:
                return True
        else:
            return True


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
            errFlag = self.checkInterval(value, a, b)
        else:
            pass

        return errFlag

    def enumerationCheckErr(self, cronStringLst, errFlag):
        for i in range(len(cronStringLst)):
            if(not errFlag):
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
    def zeroMinutesInterval(self, timerTime, cronFakeStr):
        if not self.cronStringLst[0].isdigit() and self.cronStringLst[0] != "*":
            timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).minute * 60 + int(cronFakeStr[0]) * 60
        return timerTime


    def zeroHourInterval(self, timerTime, cronFakeStr):
        if not self.cronStringLst[1].isdigit() and self.cronStringLst[1] != "*":
            timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).hour * 3600 + int(cronFakeStr[1]) * 3600

        return timerTime


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

    def calcDayForWeekdayInterval(self, timerTime, dayTimer, a, b):
        while int(datetime.datetime.fromtimestamp(timerTime).day) != int(dayTimer):
            counter = int(a)
            while counter <= int(b) and datetime.datetime.fromtimestamp(timerTime).day != int(dayTimer):
                timerTime = timerTime + 86400
            if datetime.datetime.fromtimestamp(timerTime).day != int(dayTimer):
                timerTime = timerTime + (7 - datetime.datetime.fromtimestamp(timerTime).weekday()+1 + int(a)) * 86400

        return timerTime

    def calcIntervalDayForWeekdayInterval(self, timerTime, a, b, da, db):
        check = True
        www = datetime.datetime.fromtimestamp(timerTime).weekday()
        dadada = datetime.datetime.fromtimestamp(timerTime).isoformat()
        while check:
            if(int(da) <= int(datetime.datetime.fromtimestamp(timerTime).day) <= int(db) and int(a) <= datetime.datetime.fromtimestamp(timerTime).weekday()+1 <= int(b)):
                check = False
            else:
                timerTime = timerTime + 86400

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


    def calcDayForWeekdaySteps(self, timerTime, cronStringlst, cronFakeLst, value):

        lst = cronStringlst[2].split('-')
        if len(lst) == 2:
            if lst[0].isdigit():
                while  not(int(lst[0]) <= datetime.datetime.fromtimestamp(timerTime).day <= int(lst[1]) and (datetime.datetime.fromtimestamp(timerTime).weekday() + 1) % int(value) == 0):
                    timerTime = timerTime + 86400

        lst = cronStringlst[2].split('/')

        if len(lst) == 2:
            if lst[1].isdigit():
                while not ((datetime.datetime.fromtimestamp(timerTime).weekday() + 1) % int(value) == 0 and datetime.datetime.fromtimestamp(timerTime).day % int(value) == 0):
                    timerTime = timerTime + 86400

        if cronStringlst[2].isdigit():
            while not(datetime.datetime.fromtimestamp(timerTime).day == int(cronStringlst[2]) and (datetime.datetime.fromtimestamp(timerTime).weekday() + 1) % int(value) == 0):
                timerTime = timerTime + 86400

        if cronStringlst[2] == "*":
            while not (datetime.datetime.fromtimestamp(timerTime).weekday() + 1) % int(value) == 0:
                timerTime = timerTime + 86400

        if int(cronFakeLst[1] == -1):
            timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).hour * 3600
        if int(cronFakeLst[0] == -1):
            timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).minute * 60

        return timerTime


    def calcCron(self, nowTime):
        cronFakeStr = ['-1', '-1', '-1', '-1']
        timerTime = nowTime.timestamp()
        nowTimeLst = [nowTime.minute, nowTime.hour, nowTime.day, nowTime.month, nowTime.year, nowTime.weekday()]
        for i in range(len(self.cronStringLst)):
            if i == 0:
                if self.cronStringLst[i].isdigit() or self.cronStringLst[i] == "*":
                    if self.cronStringLst[i] == "*":
                        #pass
                        if self.cronStringLst[i + 1] == "*":
                            timerTime = timerTime + 60
                        if self.cronStringLst[i+1].isdigit():
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
                else:
                    lst = self.cronStringLst[i].replace('/','-').split("-")
                    print(lst)
                    if lst[0].isdigit():
                        cronFakeStr[i] = lst[0]
                        if int(lst[0])<=int(datetime.datetime.fromtimestamp(timerTime).minute)<int(lst[1]):
                            timerTime = timerTime + 60
                        elif int(lst[0]) > datetime.datetime.fromtimestamp(timerTime).minute:
                            timerTime = timerTime + (int(lst[0]) - datetime.datetime.fromtimestamp(timerTime).minute) * 60
                        else:
                            timerTime = timerTime + (60 - datetime.datetime.fromtimestamp(timerTime).minute + int(lst[0])) * 60
                    else:
                        cronFakeStr[i] = 0
                        lst = self.cronStringLst[i].split('/')
                        nowMin = datetime.datetime.fromtimestamp(timerTime).minute
                        if nowMin == 0:
                            timerTime = timerTime + int(lst[1]) * 60
                        elif (nowMin - (nowMin % int(lst[1]))+ int(lst[1])) < 59:
                            timerTime = timerTime + int(lst[1]) * 60 - (nowMin%int(lst[1])) * 60
                        else:
                            timerTime = timerTime + (60 - nowMin) * 60


            elif i == 1:
                if self.cronStringLst[i].isdigit() or self.cronStringLst[i] == "*":
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
                else:
                    lst = self.cronStringLst[i].replace('/', '-').split("-")
                    print(lst)
                    if lst[0].isdigit():
                        cronFakeStr[i] = lst[0]
                        if int(lst[0]) <= int(datetime.datetime.fromtimestamp(timerTime).hour) < int(lst[1]):
                            pass
                        elif int(lst[0]) > datetime.datetime.fromtimestamp(timerTime).hour:
                            timerTime = timerTime + (int(lst[0]) - datetime.datetime.fromtimestamp(timerTime).hour) * 3600
                            if self.cronStringLst[0] == "*":
                                timerTime = timerTime - (datetime.datetime.fromtimestamp(timerTime).minute) * 60
                            if not self.cronStringLst[0].isdigit() and self.cronStringLst[0] != "*":
                                timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).minute * 60 + int(cronFakeStr[0])*60


                        else:
                            timerTime = timerTime + (24 - datetime.datetime.fromtimestamp(timerTime).hour + int(lst[0])) * 3600
                    else:
                        cronFakeStr[i] = 0
                        lst = self.cronStringLst[i].split('/')
                        nowHour = datetime.datetime.fromtimestamp(timerTime).hour
                        if nowHour == 0:
                            timerTime = timerTime + int(lst[1]) * 3600
                        elif nowHour%int(lst[1]) == 0:
                            pass
                        elif (nowHour - (nowHour % int(lst[1])) + int(lst[1])) < 24 and nowHour%int(lst[1]) != 0:
                            timerTime = timerTime - nowHour * 3600 + (nowHour - (nowHour % int(lst[1])) + int(lst[1])) * 3600
                            if (int(cronFakeStr[i-1]) != -1):
                                timerTime = timerTime - (datetime.datetime.fromtimestamp(timerTime).minute) * 60
                        # elif (nowHour + int(lst[1])) < 24 and nowHour%int(lst[1]) != 0:
                        #     timerTime = timerTime + int(lst[1]) * 3600 - (nowHour % int(lst[1])) * 3600
                        #     timerTime = timerTime - (datetime.datetime.fromtimestamp(timerTime).minute) * 60
                        # elif
                        else:
                            timerTime = timerTime + (24 - nowHour) * 3600
                            if (int(cronFakeStr[i-1]) != -1):
                                timerTime = timerTime - (datetime.datetime.fromtimestamp(timerTime).minute) * 60


            elif i == 2:
                if self.cronStringLst[i].isdigit() or self.cronStringLst[i] == "*":
                    if(self.cronStringLst[i] == '*'):
                        pass
                    else:
                        nowDay = datetime.datetime.fromtimestamp(timerTime).day
                        if nowDay < int(self.cronStringLst[i]):
                            timerTime = self.calcDayForMonth(timerTime, self.cronStringLst[i])
                            timerTime = timerTime + (int(self.cronStringLst[i]) - nowDay) * 86400
                            timerTime = self.zeroHour(timerTime)
                            timerTime = self.zeroMinutes(timerTime)
                            timerTime = self.zeroHourInterval(timerTime,cronFakeStr)
                            timerTime = self.zeroMinutesInterval(timerTime,cronFakeStr)
                        elif nowDay > int(self.cronStringLst[i]):
                            timerTime = self.calcDayForMonth(timerTime, self.cronStringLst[i])
                            numberOfDays = self.dayOfMonth[datetime.datetime.fromtimestamp(timerTime).month - 1]
                            timerTime = self.zeroHour(timerTime)
                            timerTime = self.zeroMinutes(timerTime)
                            timerTime = self.zeroHourInterval(timerTime,cronFakeStr)
                            timerTime = self.zeroMinutesInterval(timerTime,cronFakeStr)
                            if datetime.datetime.fromtimestamp(timerTime).month == 2:
                                if datetime.datetime.fromtimestamp(timerTime).year % 4 == 0:
                                    numberOfDays = numberOfDays + 1
                            timerTime = timerTime + (numberOfDays - nowDay + int(self.cronStringLst[i])) * 86400
                        else:
                            pass
                else:
                    nowDay = datetime.datetime.fromtimestamp(timerTime).day
                    lst = self.cronStringLst[i].replace('/', '-').split("-")
                    print(lst)
                    if lst[0].isdigit():
                        cronFakeStr[i] = lst[0]
                        if int(lst[0]) <= int(datetime.datetime.fromtimestamp(timerTime).day) < int(lst[1]):
                            pass
                        elif int(lst[0]) > datetime.datetime.fromtimestamp(timerTime).day:
                            timerTime = timerTime + (int(lst[0]) - datetime.datetime.fromtimestamp(timerTime).day) * 86400
                            # # null time minute
                            # if self.cronStringLst[0] == "*":
                            #     timerTime = timerTime - (datetime.datetime.fromtimestamp(timerTime).minute) * 60
                            # if not self.cronStringLst[0].isdigit() and self.cronStringLst[0] != "*":
                            #     timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).minute * 60 + int(cronFakeStr[0]) * 60
                            # #null timer hour
                            # if self.cronStringLst[1] == "*":
                            #     timerTime = timerTime - (datetime.datetime.fromtimestamp(timerTime).hour) * 3600
                            # if not self.cronStringLst[1].isdigit() and self.cronStringLst[1] != "*":
                            #     timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).hour * 3600 + int(cronFakeStr[1]) * 3600
                            timerTime = self.zeroMinutes(timerTime)
                            timerTime = self.zeroHour(timerTime)
                            timerTime = self.zeroHourInterval(timerTime,cronFakeStr)
                            timerTime = self.zeroMinutesInterval(timerTime,cronFakeStr)

                        else:
                            timerTime = timerTime + (self.dayOfMonth[datetime.datetime.fromtimestamp(
                                timerTime).month - 1] - datetime.datetime.fromtimestamp(timerTime).day + int(lst[0])) * 86400
                    else:
                        cronFakeStr[i] = 1
                        lst = self.cronStringLst[i].split('/')
                        nowDay = datetime.datetime.fromtimestamp(timerTime).day
                        numberOfDays = self.dayOfMonth[datetime.datetime.fromtimestamp(timerTime).month - 1]
                        if nowDay - nowDay%int(lst[1]) + int(lst[1]) < numberOfDays:
                            timerTime = timerTime - nowDay%int(lst[1]) * 86400 + int(lst[1]) * 86400
                            if int(cronFakeStr[i-1] == -1):
                                timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).hour * 3600
                            if int(cronFakeStr[i-2] == -1):
                                timerTime = timerTime - datetime.datetime.fromtimestamp(timerTime).minute * 60


            elif i == 3:
                if self.cronStringLst[i].isdigit() or self.cronStringLst[i] == "*":
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
                            numberOfWeekday = datetime.datetime.fromtimestamp(timerTime).weekday() + 1
                            if numberOfWeekday < int(self.cronStringLst[i]):
                                timerTime = timerTime + (int(self.cronStringLst[i]) - numberOfWeekday) * 86400
                                timerTime = self.calcDayForWeekday(timerTime, self.cronStringLst[i-1])
                            elif numberOfWeekday > int(self.cronStringLst[i]):
                                timerTime = timerTime + (7 - numberOfWeekday + int(self.cronStringLst[i])) * 86400
                                timerTime = self.calcDayForWeekday(timerTime, self.cronStringLst[i-1])
                            else:
                                timerTime = self.calcDayForWeekday(timerTime, self.cronStringLst[i-1])
                else:
                    lst = self.cronStringLst[i].replace('/', '-').split("-")
                    if lst[0].isdigit():
                        if (self.cronStringLst[i - 1] == "*"):
                            numberOfWeekday = datetime.datetime.fromtimestamp(timerTime).weekday() + 1
                            if numberOfWeekday < int(lst[0]):
                                timerTime = timerTime + (int(lst[0]) - numberOfWeekday) * 86400
                            elif numberOfWeekday > int(lst[1]):
                                timerTime = timerTime + (7 - numberOfWeekday + int(lst[0])) * 86400
                            else:
                                pass
                        elif self.cronStringLst[i - 1].isdigit():
                            # dayTimer = int(self.cronStringLst[i-1])
                            numberOfWeekday = datetime.datetime.fromtimestamp(timerTime).weekday() + 1
                            if numberOfWeekday < int(lst[0]):
                                timerTime = timerTime + (int(lst[0]) - numberOfWeekday) * 86400
                                timerTime = self.calcDayForWeekdayInterval(timerTime, self.cronStringLst[i - 1], lst[0], lst[1])
                            elif numberOfWeekday > int(lst[1]):
                                timerTime = timerTime + (7 - numberOfWeekday + int(lst[0])) * 86400
                                timerTime = self.calcDayForWeekdayInterval(timerTime, self.cronStringLst[i - 1], lst[0], lst[1])
                            else:
                                timerTime = self.calcDayForWeekdayInterval(timerTime, self.cronStringLst[i - 1], lst[0], lst[1])
                        else:
                            lstday = self.cronStringLst[i-1].split("-")
                            timerTime = self.calcIntervalDayForWeekdayInterval(timerTime,lst[0], lst[1], lstday[0], lstday[1])

                    else:
                        nowWd = datetime.datetime.fromtimestamp(timerTime).weekday() + 1
                        if nowWd % int(lst[1]) == 0:
                            pass
                        else:
                            timerTime = self.calcDayForWeekdaySteps(timerTime, self.cronStringLst, cronFakeStr, lst[1])





        print(datetime.datetime.fromtimestamp(timerTime).isoformat())
        return timerTime

if __name__ == "__main__":
    cronStr = "30 * 25 */4"
    errFlag = False
    cron = Cron(cronStr)
    errFlag = cron.enumerationCheckErr(cron.cronStringLst, errFlag)
    if errFlag:
        print("err")
    else:
        nowTime = datetime.datetime.now().replace(microsecond=0).replace(second=0)
        cron.calcCron(nowTime)
