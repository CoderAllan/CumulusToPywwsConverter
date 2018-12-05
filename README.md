
# CumulusToPiConverter.py

A nice tool for converting existing Cumulus data files to the data format used by pywws

To run the script just start your favorite console and execute the script:
```
python ConvertCumulusToPywws.py
```

The paths for the input and output directories are hardcoded into the script, so if your data is not placed in the current directory, then just change the paths:

```python
cumulusLogFilesDirectory = ".\\CumulusData"
pywwsDataFolder = ".\\pywwsData"
```

# Motivation

I have implemented this script because i used the [Cumulus weather station software](https://cumuluswiki.wxforum.net/a/Main_Page) for downloading data from my Rosenborg weather station.
But it is a manual and tedious task because i did not have a PC near the weather station that i could use to continuously download data from the weather station, so a coouple of time a month i had to connect the weather station to my PC and wait for it to download the data.

Now I finaly got a Rabpberry Pi Model A+ permanently connected to the weather station. On the Pi I run [Pywws](https://github.com/jim-easterbrook/pywws) once every hour to download data and process it. Pywws also creates a overview of the historical data and this is why I created the CumulusToPiConverter.py script.

