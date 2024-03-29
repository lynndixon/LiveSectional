import urllib2
import xml.etree.ElementTree as ET
import time
from neopixel import *
import sys
import os
import datetime


# LED strip configuration:
LED_COUNT      = 136      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 64     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
now            = now = datetime.datetime.now()
timestamp      = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
logfile        = open("/var/log/livesectional.log", "a+")

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

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


for metar in root.iter('METAR'):
	if airportcode == "NULL":
		continue
	stationId = metar.find('station_id').text
	#print stationId
	if metar.find('flight_category') is None:
		#print "Skipping"
		continue

	flightCateory = metar.find('flight_category').text
	#print stationId + " " + flightCateory
	#logfile.write("\n"+ stationId + " " + flightCateory)
	if stationId in mydict:
            continue
	#	logfile.write("\nduplicate, only save first metar")
	else:
		mydict[stationId] = flightCateory



#print mydict

i = 0
for airportcode in airports:
	if airportcode == "NULL":
		i = i +1
		continue
	#print
	color = Color(0,0,0)

	flightCateory = mydict.get(airportcode,"No")
	#print airportcode + " " + flightCateory

	if  flightCateory != "No":

		if flightCateory == "VFR":
			#print "VFR"
			color = Color(255,0,0)
		elif flightCateory == "MVFR":
			color = Color(0,0,255)
			#print "MVFR"
		elif flightCateory == "IFR":
			color = Color(0,255,0)
			#print "IFR"
		elif flightCateory == "LIFR":
			color = Color(0,128,128)
			#print "LIFR"
	else:
		color = Color(128,128,128)
		#print "N/A"

	# print "Setting light " + str(i) + " for " + airportcode + " " + flightCateory + " " + str(color)
	logfile.write("\nSetting light " + str(i) + " for " + airportcode + " " + flightCateory + " " + str(color))
	strip.setPixelColor(i, color)
	strip.show()

	i = i+1
#print
logfile.write("\nLiveSectional updated succesfully at: " +str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))+"\n")
print "fin"
quit()
