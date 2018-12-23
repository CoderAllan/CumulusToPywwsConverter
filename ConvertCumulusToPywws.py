import os
from os import listdir
from os.path import isfile, exists, join, basename

# Cumulus format, semicolon format
#  0 Date (dd/mm/yy)|
#  1 Time|
#  2 Temperature|
#  3 Humidity|
#  4 Dew point|
#  5 Wind speed|
#  6 Recent high gust|
#  7 Average wind bearing|
#  8 Rainfall rate|
#  9 Rainfall so far|
# 10 Sea level pressure|
# 11 Rainfall counter|
# 12 Inside temperature|
# 13 Inside humidity|
# 14 Current gust|Wind chill|Heat Index|UV Index|Solar Radiation|Evapotranspiration|Annual Evapotranspiration|Apparent temperature|Max Solar radiation|Hours of sunshine|Wind bearing|RG-11 Rain|Rain Since Midnight

# pywws format, comma seperated
# 'idx'          : WSDateTime.from_csv,
# 'delay'        : int,
# 'hum_in'       : int,
# 'temp_in'      : float,
# 'hum_out'      : int,
# 'temp_out'     : float,
# 'abs_pressure' : float,
# 'wind_ave'     : float,
# 'wind_gust'    : float,
# 'wind_dir'     : int,
# 'rain'         : float,
# 'status'       : WSStatus.from_csv,
# 'illuminance'  : float,
# 'uv'           : int,

def convertCumulusToPywws(date, cols):
    timestamp = date + " " + cols[1] + ":00"
    delay = "5"
    temp_in = cols[12].replace(",", ".")
    hum_in = cols[13].replace(",", ".")
    temp_out = cols[2].replace(",", ".")
    hum_out = cols[3].replace(",", ".")
    abs_pressure = cols[10].replace(",", ".")
    wind_ave = cols[5].replace(",", ".")
    wind_gust = cols[6].replace(",", ".")
    wind_dir = cols[24].replace(",", ".")
    rain = cols[11].replace(",", ".")
    status = "0"
    pywwsArr = [timestamp, delay, hum_in, temp_in, hum_out, temp_out,
                abs_pressure, wind_ave, wind_gust, wind_dir, rain, status]
    return ",".join(pywwsArr)

cumulusLogFilesDirectory = ".\\CumulusData"
pywwsDataFolder = ".\\pywwsData"

logfiles = [f for f in listdir(cumulusLogFilesDirectory) if (isfile(join(cumulusLogFilesDirectory, f)) & basename(f).endswith("log.txt"))]

dayDictionary = {}
for logfile in logfiles:
    print(f"Reading: {logfile}")
    with open(join(cumulusLogFilesDirectory, logfile)) as lf:
        for line in lf:
            cols = line.split(";")
            dateparts = cols[0].split("-")
            year = str("20" + dateparts[2])
            month = str(dateparts[1])
            day = str(dateparts[0])
            timestamp = f"{year}-{month}-{day}"
            line = convertCumulusToPywws(timestamp, cols)
            if timestamp not in dayDictionary:
                dayDictionary.setdefault(timestamp, [])
            dayDictionary[timestamp].append(line)

for key in dayDictionary:
    (year, month, day) = key.split("-")
    # monthFolder = join(yearFolder, year + "-" + month)
    currentYearMonth = join(pywwsDataFolder, year, f"{year}-{month}")
    if not exists(currentYearMonth):
        os.makedirs(currentYearMonth)
    
    weatherData = dayDictionary[key]
    timestamp = weatherData[0].split(",")[0]
    (day, time) = timestamp.split(" ")
    filename = join(currentYearMonth, day + ".txt")
    if exists(filename):
        os.remove(filename)

    print(f"Writing: {filename}")
    pywws_file = open(filename, "w")
    pywws_file.writelines("\n".join(weatherData))
    pywws_file.close()


