/bin/echo -e "\nStopping LiveSectional" >> /var/log/livesectional.log
/usr/bin/python /LiveSectional/live_sectional_daemon.py stop
/usr/bin/python /LiveSectional/wipe.py
exit
