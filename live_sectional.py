#!/usr/bin/python
import urllib2
import xml.etree.ElementTree as ET
import time
from neopixel import *
import sys
import os
import datetime
from daemon import runner

def update_map():
    # LED strip configuration:
    LED_COUNT      = 136      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 16     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
    now            = now = datetime.datetime.now()
    timestamp      = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

    logfile        = open("/var/log/livesectional.log", "a+")
    logfile.write("\n-----------------------------------------------------------------------------")
    logfile.write("\nMETAR update Began on: " + str(timestamp))

    strip.begin()


    with open("/LiveSectional/airports") as f:
        airports = f.readlines()
    airports = [x.strip() for x in airports]
    #print airports


    mydict = {
        "":""
    }


    url = "https://aviationweather.gov/cgi-bin/data/dataserver.php?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=1.5&mostRecentForEachStation=true&stationString="
    for airportcode in airports:
        if airportcode == "NULL":
            continue
        #print airportcode
        url = url + airportcode + ","

    #print url
    content = urllib2.urlopen(url).read()
    #print content


    root = ET.fromstring(content)

    if root.find('num_results') == '0':
        logfile.write("\nNo results found from aviationweather.gov. Possible connection issue.")
        logfile.write("\nLiveSectional update failed at: " +str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))+"\n")
        flightCategory = "No"
        weather = "NONE"
    else:
        for metar in root.iter('METAR'):
            if airportcode == "NULL":
                continue
            stationId = metar.find('station_id').text
            #print stationId
            if metar.find('flight_category') is None: # If we can't find the flight category in the XML, lets try and determine it.
                logfile.write("\nNO CATEGORY FOUND IN XML. Attempting to determine the category for " + airportcode)

                flightCategory = "VFR" #intialize flight category

                #There can be multiple layers of clouds in each METAR, but they are always listed lowest AGL first.
                #Check the lowest (first) layer and see if it's overcast, broken, or obscured. If it is, then compare to cloud base height to set flight category.
                #This algorithm basically sets the flight category based on the lowest OVC, BKN or OVX layer.

                for sky_condition in metar.iter('sky_condition'):   #for each sky_condition from the XML
                        sky_cvr = sky_condition.attrib['sky_cover']     #get the sky cover (BKN, OVC, SCT, etc)
                        if sky_cvr in ("OVC","BKN","OVX"): #If the layer is OVC, BKN or OVX, set Flight category based on height AGL
                                cld_base_ft_agl = sky_condition.attrib['cloud_base_ft_agl'] #get cloud base AGL from XML
                                cld_base_ft_agl = int(cld_base_ft_agl)                      #convert string to integer
                                if cld_base_ft_agl < 500:
                                        flightCategory = "LIFR"
                                        break
                                elif 500 <= cld_base_ft_agl < 1000:
                                        flightCategory = "IFR"
                                        break
                                elif 1000 <= cld_base_ft_agl <= 3000:
                                        flightCategory = "MVFR"
                                        break
                                elif cld_base_ft_agl > 3000:
                                        flightCategory = "VFR"
                                        break

                #visibilty can also set flight category. If the clouds haven't set the fltcat to LIFR. See if visibility will
                if flightCategory != "LIFR": #if it's LIFR due to cloud layer, no reason to check any other things that can set flight category.
                        if metar.find('visibility_statute_mi') is not None: #check XML if visibility value exists
                                visibility_statute_mi = metar.find('visibility_statute_mi').text   #get visibility number
                                visibility_statute_mi = float(visibility_statute_mi)               #convert string to float
                                if visibility_statute_mi < 1.0:
                                        flightCategory = "LIFR"
                                elif 1.0 <= visibility_statute_mi < 3.0:
                                        flightCategory = "IFR"
                                elif 3.0 <= visibility_statute_mi <= 5.0 and flightCategory != "IFR":  #if Flight Category was already set to IFR by clouds, it can't be reduced to MVFR
                                        flightCategory = "MVFR"
            else:
                flightCategory = metar.find('flight_category').text
                #print stationId + " " + flightCategory
                logfile.write("\n"+ stationId + " " + str(flightCategory))
            if stationId in mydict:
                    logfile.write("\nduplicate, only save first metar")
                    continue     	
            else:
                mydict[stationId] = flightCategory



    #print mydict

    i = 0
    for airportcode in airports:
        if airportcode == "NULL":
            i = i +1
            continue
        #print
        color = Color(0,0,0)

        flightCategory = mydict.get(airportcode,"No")
        #print airportcode + " " + flightCategory

        if  flightCategory != "No":

            if flightCategory == "VFR":
                #print "VFR"
                color = Color(255,0,0)
            elif flightCategory == "MVFR":
                color = Color(0,0,255)
                #print "MVFR"
            elif flightCategory == "IFR":
                color = Color(0,255,0)
                #print "IFR"
            elif flightCategory == "LIFR":
                color = Color(0,128,128)
                #print "LIFR"
        else:
            color = Color(128,128,128)
            #print "N/A"

        # print "Setting light " + str(i) + " for " + airportcode + " " + flightCategory + " " + str(color)
        logfile.write("\nSetting light " + str(i) + " for " + airportcode + " " + str(flightCategory) + " " + str(color))
        strip.setPixelColor(i, color)

        i = i+1

    logfile.write("\nLiveSectional updated succesfully at: " +str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))+"\n")
    strip.show()
    print("LiveSectional Update completed!")
    logfile.close()

if __name__ == "__main__":
      update_map()
            