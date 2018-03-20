import urllib.request
import json
import sys
import datetime

def getAreaId(areaName):
    #print("Was loaded")
    f = urllib.request.urlopen('https://tp.uio.no/ntnu/timeplan/?type=room')
    f = f.read().decode('utf-8')
    location = json.loads(((f.split('<script id="menu-js">['))[1].split(']</script>'))[0])
    if(areaName == 'all'):
        allset = True
        allList = []
    else:
        allset = False

    for areas in location['areas']:
        if(len(sys.argv)>0):
            if(areaName==areas['name']):
                num = areas['id']
            elif(areaName=='all'):
                allList.append(areas['name']+":"+areas['id'])

    try:
        if(allset != True):
            return num
        else:
            return allList

    except NameError:
        return "Variable was not defined"

def getBuildingId(areaId, building):
    week = datetime.date.today().isocalendar()[1]
    year = datetime.date.today().isocalendar()[0]
    f = urllib.request.urlopen('https://tp.uio.no/ntnu/timeplan/?type=room&area='+areaId+'&week='+str(week)+'&ar='+str(year))
    f = f.read().decode('utf-8')
    location = json.loads(((f.split('<script id="menu-js">['))[1].split(']</script>'))[0])
    if(building == 'all'):
        allset = True
        allList = []
    else:
        allset = False
    #print(location)
    for areas in location['buildings']:
        if(len(sys.argv)>0):
            if(building==areas['name']):
                num = areas['id']
            elif(allset):
                allList.append(areas['name']+":"+areas['id'])


    try:
        if(allset != True):
            return num
        else:
            return allList

    except NameError:
        return "Variable was not defined"

def getBuildingBooking(areaId, buildingId, week=datetime.date.today().isocalendar()[1], year=datetime.date.today().isocalendar()[0]):
    f = urllib.request.urlopen('https://tp.uio.no/ntnu/timeplan/?type=room&area='+areaId+'&building='+buildingId+'&id='+buildingId+'allRooms&week='+str(week)+'&ar='+str(year))
    f = f.read().decode('utf-8')
    location = json.loads(json.dumps((((f.split('<script id="data-js">['))[1].split(']</script>'))[0])))
    #print(location)

    try:
        return location

    except NameError:
        return "Variable was not defined"


if(len(sys.argv)==2):
    print(getAreaId(sys.argv[1]))
elif(len(sys.argv)==3):
    if((sys.argv[1]=='all') and (sys.argv[2]=='all')):
        print("Not allowed! Would currently cause to much spam")
    print(getBuildingId(sys.argv[1], sys.argv[2]))
elif(len(sys.argv)>3):
    print(getBuildingBooking(sys.argv[1], sys.argv[2]))
