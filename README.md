# LiveSectional

Controls NeoPixel LED's to display conditions at airports.

Heres a quick video that demonstrates what this does: [LiveSectional Demo on YouTube](https://www.youtube.com/watch?v=QGhew5iJEAY)

## Installation and setup

1. Fully update the Pi:
    * `sudo apt-get update && sudo apt-get upgrade`

2. Install the following required packages:
    * `sudo apt-get install build-essential python-dev git scons swig python-pip`

3. Use pip to install the NeoPixel controller libraries
    * `sudo pip install rpi_ws281x`

4. Installation of the following software is optional.
    * `sudo apt-get install vim`

### More Information

* More about NeoPixels: <https://learn.adafruit.com/neopixels-on-raspberry-pi/>
