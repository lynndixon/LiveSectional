sudo echo -e "\nStarting up LiveSectional" >> /var/log/livesectional.log
sudo python /LiveSectional/test.py
sleep 60
sudo python /LiveSectional/live_sectional.py
exit
