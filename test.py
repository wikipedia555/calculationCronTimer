cronString = "45 17 31 7"
cronStringLst = cronString.split()
errFlag = False

def checkValue(value):
    if value == "*" or value.isdigit():
        al = value.isdigit()
        return al
    else:
        return "err"

def checkErr(errFlag, a,b, value):
    if checkValue(value) == True:
        if not (a <= int(value) <= b):
            errFlag = True
    elif checkValue(value) == "err":
        errFlag = True
    else:
        pass

    return errFlag

def enumerationCheckErr(cronStringLst, errFlag):

    for i in range(len(cronStringLst)):
        if i == 0:
            errFlag = checkErr(errFlag, 0, 59, cronStringLst[i])
        elif i == 1:
            errFlag = checkErr(errFlag, 0, 23, cronStringLst[i])
        elif i == 2:
            errFlag = checkErr(errFlag, 1, 31, cronStringLst[i])
        elif i == 3:
            errFlag = checkErr(errFlag, 1, 7, cronStringLst[i])
        else:
            pass

    print(errFlag)

enumerationCheckErr(cronStringLst,errFlag)