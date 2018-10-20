/bin/echo -e "\nStarting up LiveSectional" >> /var/log/livesectional.log
/usr/bin/python /LiveSectional/test.py
/usr/bin/python /LiveSectional/live_sectional_daemon.py start
exit
