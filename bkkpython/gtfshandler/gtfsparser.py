from datetime import datetime
import os
from requests import get
from gtfshandler.models import HevDeparture
import zipfile
from django.utils import timezone
from django.utils.timezone import make_aware
gtfsFolder = 'latestgtfs'
scriptDir = os.path.dirname(__file__)

def downloadAndUnzipGtfsPackage():
    url = 'https://go.bkk.hu/api/static/v1/public-gtfs/budapest_gtfs.zip'
    response = get(url, allow_redirects=True)
    gtfsZipPathPath = os.path.join(scriptDir, 'budapest_gtfs.zip')
    open(gtfsZipPathPath, 'wb').write(response.content)
    gtfsUnzipPathPath = os.path.join(scriptDir, 'latestgtfs')
    with zipfile.ZipFile(gtfsZipPathPath, 'r') as zip_ref:
        zip_ref.extractall(gtfsUnzipPathPath)

def loadDeparturesToDatabase():
    print("Load departures into database...")

    calendarDatesPath = os.path.join(scriptDir, 'latestgtfs/calendar_dates.txt')
    with open(calendarDatesPath, encoding='utf8') as f:
        calendarDatesLines = f.readlines()

    tripsPath = os.path.join(scriptDir, 'latestgtfs/trips.txt')
    with open(tripsPath, encoding='utf8') as f:
        lines = f.readlines()

    serviceIds = []
    h5tripIdsToBatyi = []
    now = datetime.now()
    for line in lines:
        if line.startswith("H5"):
            splitLine = line.split(',')
            directionId = splitLine[4]
            if directionId == '1':
                foundInCalendar = False
                numOfFound = 0
                for calendarDate in calendarDatesLines:
                    splitCalendarDate = calendarDate.split(',')
                    if splitCalendarDate[0] == splitLine[2]: ## only use it if it is in the calendar_dates
                        calendarYear = splitCalendarDate[1][0:4]
                        nowYear = str(now.year)

                        calendarMonth = splitCalendarDate[1][4:6]
                        prefix = ''
                        if now.month < 10:
                            prefix = '0'
                        nowMonth = prefix + str(now.month)

                        prefix = ''
                        if now.day < 10:
                            prefix = '0'
                        calendarDay = splitCalendarDate[1][6:]
                        nowDay = prefix + str(now.day)
                        if calendarYear == nowYear and calendarMonth == nowMonth and calendarDay == nowDay:
                            h5tripIdsToBatyi.append(splitLine[1])
                            break

    stopTimesPath = os.path.join(scriptDir, 'latestgtfs/stop_times.txt')
    with open(stopTimesPath, encoding='utf8') as f:
        lines = f.readlines()

    h5stopBekasTimes = []
    for i in range(len(lines)):
        splitLine = lines[i].split(',')
        tripId = splitLine[0]
        if tripId in h5tripIdsToBatyi: # only check trips which go to Batyi
            if 'F00472' in lines[i]: #F00472 is Bekasmegyer stop
                bekasStart = True
                
                if splitLine[4] == '7':
                    bekasStart = False
                if [splitLine[3], bekasStart] not in h5stopBekasTimes:#vmiert vannak duplikalt bejegyzesek TODO kitalalni miert
                    h5stopBekasTimes.append([splitLine[3], bekasStart, splitLine[0], splitLine[1], splitLine[2], splitLine[4], splitLine[5], splitLine[6], splitLine[7], splitLine[8]])
                
    #print(h5stopBekasTimes)
    h5stopDates = []
    for time in h5stopBekasTimes:
        now = datetime.now()
        dateTime = str(now.day)+'/'+str(now.month)+'/'+str(now.year)[2:4] + ' ' + time[0]
        h5stopDates.append([datetime.strptime(dateTime, '%d/%m/%y %H:%M:%S'), time[1], time[2], time[3], time[4],time[5],time[6],time[7],time[8],time[9]])

    h5stopDates.sort(key=lambda x: x[0])
    now = datetime.now()
    sum = 0
    finalH5Format = []
    for i in range(len(h5stopDates)):
        #if h5stopDates[i] > now:
        #sum = sum+1
        untilDepartMin = (h5stopDates[i][0] - now).total_seconds()/60
        #print(untilDepartMin)

        isBekasi = h5stopDates[i][1]
        #print(isBekasi)
        departureMin = str(h5stopDates[i][0].minute)
        if h5stopDates[i][0].minute < 10:
            departureMin = '0' + str(h5stopDates[i][0].minute)
        departureTime = str(h5stopDates[i][0].hour) + ':' + departureMin
        #print(departureTime)
        finalH5Format.append([departureTime, untilDepartMin, isBekasi ,h5stopDates[i][2], h5stopDates[i][3], h5stopDates[i][4], h5stopDates[i][5], h5stopDates[i][6], h5stopDates[i][7], h5stopDates[i][8], h5stopDates[i][9]])
    #print(sum)
    for departure in finalH5Format:
        print(departure)
        now = datetime.now()
        splitDeparture = departure[0].split(':')
        dateTime = str(now.day)+'/'+str(now.month)+'/'+str(now.year)[2:4] + ' ' + splitDeparture[0] + ':' + splitDeparture[1] + ':0'
        tempDepartureTime = make_aware(datetime.strptime(dateTime, '%d/%m/%y %H:%M:%S'))
        d = HevDeparture(departureTime=tempDepartureTime, startsFromBekas=departure[2])
        d.save()