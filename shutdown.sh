#!/usr/bin/bash
sudo echo -e "\nStopping LiveSectional" >> /var/log/livesectional.log
sudo python /LiveSectional/live_sectional_daemon.py stop
sudo python /LiveSectional/wipe.py
exit
