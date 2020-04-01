cronString = "45 23 31 7"
cronStringLst = cronString.split()
errFlag = False

def checkValue(value):
    if value == "*" or value.isdigit():
        al = value.isdigit()
        return al
    else:
        return "err"

def checkErr(errFlag, a,b):
    if checkValue(cronStringLst[i]) == True:
        if not (a <= int(cronStringLst[i]) <= b):
            errFlag = True
    elif checkValue(cronStringLst[i]) == "err":
        errFlag = True
    else:
        pass

    return errFlag


for i in range(len(cronStringLst)):
    if i == 0:
        errFlag = checkErr(errFlag, 0, 59)
    elif i == 1:
        errFlag = checkErr(errFlag, 0, 23)
    elif i == 2:
        errFlag = checkErr(errFlag, 1, 31)
    elif i == 3:
        errFlag = checkErr(errFlag, 1, 7)
    else:
        pass

print(errFlag)