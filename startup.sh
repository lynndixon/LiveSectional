#!/usr/bin/bash
sudo echo -e "\nStarting up LiveSectional" >> /var/log/livesectional.log
sudo python /LiveSectional/test.py
sudo python /LiveSectional/live_sectional_daemon.py start
exit
