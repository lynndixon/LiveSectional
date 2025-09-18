#!/usr/bin/python
import urllib2
import xml.etree.ElementTree as ET
import time
from neopixel import *
import sys
import os
import datetime
from daemon import runner
from live_sectional import update_map

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/livesectional.log'
        self.stderr_path = '/var/log/livesectional.log'
        self.pidfile_path =  '/var/run/livesectional.pid'
        self.pidfile_timeout = 5
    def run(self):
        while True:
            update_map()
            time.sleep(450)

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
