#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Script to set the BitDay wallpaper depending on the current time and location.
The wallpapers can be downloaded here:
http://danny.care/bitday/download/
"""

from os import listdir
from os.path import isfile, join, expanduser, expandvars
from datetime import datetime
from time import sleep, localtime
from subprocess import check_output, run
import math

# Modify if necessary
imgPath = '~/Bilder/BitDay/1600x900'    # Path to image files
location = [49.0117, 12.1002]           # Geographic coordinates [latitude, longitude]

switchPoint = [0.1, 0.2, 0.3, 0.8]

def calculateSunriseSunset(T, latitude, longitude):
    # Geografische Breite in Bogenmaß
    B = latitude * math.pi / 180.0
    # Sonnendeklination
    DK = 0.409526325277017 * math.sin(0.0169060504029192 * (T - 80.0856919827619))
    # Zeitdifferenz
    ZD = 12.0 * math.acos((math.sin(-(50.0/60.0) * math.pi / 180.0) - \
         math.sin(B) * math.sin(DK)) / (math.cos(B) * math.cos(DK))) / math.pi
    # Zeitgleichung
    ZG = -0.170869921174742 * math.sin(0.0336997028793971 * T + 0.465419984181394) \
         - 0.129890681040717 * math.sin(0.0178674832556871 * T - 0.167936777524864)
    # Aufgangszeit
    sunrise = 12 - ZD - ZG
    sunrise = sunrise - longitude / 15.0
    # Untergangszeit
    sunset = 12 + ZD - ZG
    sunset = sunset - longitude / 15.0
    return [sunrise + localtime().tm_gmtoff / 3600, sunset + localtime().tm_gmtoff / 3600]


print(datetime.now().strftime('%a %w. %b %H:%M:%S %Y: BitDay wallpaper changer is running...'))
imgPath = expandvars(expanduser(imgPath))
pics = sorted([f for f in listdir(imgPath) if isfile(join(imgPath, f))])
numOfPics = len(pics)
pic = join(imgPath, pics[0])
while True:
    currTime = datetime.now().hour + datetime.now().minute / 60.0
    sunrise, sunset = calculateSunriseSunset(datetime.now().timetuple().tm_yday, location[0], location[1])
    if (currTime >= sunrise and currTime < ((12.0 - sunrise) * switchPoint[0] + sunrise)):
        pic = join(imgPath, pics[0])
    elif (currTime >= ((12.0 - sunrise) * switchPoint[0] + sunrise) and currTime < ((12.0 - sunrise) * switchPoint[1] + sunrise)):
        pic = join(imgPath, pics[1])
    elif (currTime >= ((12.0 - sunrise) * switchPoint[1] + sunrise) and currTime < ((12.0 - sunrise) * switchPoint[2] + sunrise)):
        pic = join(imgPath, pics[2])
    elif (currTime >= ((12.0 - sunrise) * switchPoint[2] + sunrise) and currTime < ((12.0 - sunrise) * switchPoint[3] + sunrise)):
        pic = join(imgPath, pics[3])
    elif (currTime >= ((12.0 - sunrise) * switchPoint[3] + sunrise) and currTime < ((sunset - 12.0) * (1 - switchPoint[3]) + 12.0)):  # Mittag
        pic = join(imgPath, pics[4])
    elif (currTime >= ((sunset - 12.0) * (1 - switchPoint[3]) + 12.0) and currTime < ((sunset - 12.0) * (1 - switchPoint[2]) + 12.0)):
        pic = join(imgPath, pics[5])
    elif (currTime >= ((sunset - 12.0) * (1 - switchPoint[2]) + 12.0) and currTime < ((sunset - 12.0) * (1 - switchPoint[1]) + 12.0)):
        pic = join(imgPath, pics[6])
    elif (currTime >= ((sunset - 12.0) * (1 - switchPoint[1]) + 12.0) and currTime < ((sunset - 12.0) * (1 - switchPoint[0]) + 12.0)):
        pic = join(imgPath, pics[7])
    elif (currTime >= ((sunset - 12.0) * (1 - switchPoint[0]) + 12.0) and currTime < sunset):
        pic = join(imgPath, pics[8])
    elif (currTime >= sunset and currTime < (((24.0 - sunset) / 2.0) + sunset)):
        pic = join(imgPath, pics[9])
    elif (currTime >= (((24.0 - sunset) / 2.0) + sunset) or currTime < (sunrise / 2.0)):  # Mitternacht
        pic = join(imgPath, pics[10])
    elif (currTime >= (sunrise / 2.0) and currTime < sunrise):
        pic = join(imgPath, pics[11])

    currPic = check_output(['gsettings', 'get', 'org.gnome.desktop.background', 'picture-uri']).decode().strip()
    if '\'file://' + pic + '\'' != currPic:
        print(datetime.now().strftime('%a %w. %b %H:%M:%S %Y: Changing wallpaper to \'') + pic + '\'')
        run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://' + pic])

    sleep(30)
