# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-09-18
### Added
-  `config.py` - Config file to store all our configurations. 
-  `archive` - Directory for older code, kept for reference only.  Will go away soon?

### Changed
-  `live_sectional_daemon.py` - Cleaned this up immensley by importing the method(s) from `live_sectional.py`. 
-  `live_sectiona.py` - Refacorted this entire file, Its actually used and not a manual copy from the daemon. Makes for cleaner troubleshooting and updating.  Also corrected the FAA url, as it changed on 2025-09-17. 

## [1.1.0] - 2018-10-27

### Added

- `live_sectional_daemon.py` - New method that runs as a daemon using python-daemon. Does `strip.show()` after the color setting loop so there isn't a wipe effect.  Only LED's that change category will change color....not the entire strip.
- `shutdown.sh` - Modified to use live_sectional_daemon.py as its stopping script.

### Changed

- `startup.sh` - Modified to use live_sectional_daemon.py as its starter script.
- Renamed `shutdown.py` to `wipe.py` because all it does is wipe the strip to dark colors.
- `live_sectional.service` modified to point to new `shutdown.sh` script instead of `shutdown.py`
- `live_sectional_daemon.py` - include a logfile.close() to close up the log file after the loop is done.
- `live_sectional_daemon.py` - Bumped the refresh down to 7.5 minutes, and adjusted the brightness down...it was retina melting bright.

## [1.0.1] - 2018-10-12

### Added

- `livesectional` - Added in etc/logrotate.d/ directory to configure logrotatation
- `shutdown.py` - Script to wipe all the LEDs on shutdown.
- `livesectional.service` - SystemD service file to start / stop the service

### Changed

- `airports` - Final update for the entire ATL sectional
- `live_sectional.py` - Removed the print lines for performance and updated writing to log file.
- `test.py` - Updated to include a color wipe back to off on the LEDs.


## [1.0.0] - 2018-08-03

### Added

- Initial commit. Building the initial structure, and adding a Changelog to help keep track of changes
- Added entire ATL sectional into `airports` file.  Only covers those stations that are reporting METARs as of todays date.
- `test.py` added to test all LED's during startup.  Might change this to a normal sequence in the future. Just using generic rainbow animations for now.
- `startup.sh` bash script to help startup LiveSectional.

### Changed

- `test_lights.py` - Modified to include an argument for the number of LED's to light up.
- `test_leds.py` has been renamed to `led_test.py` for easier tab completion, because I'm lazy like that.
- Updated Namespaces in `live_sectional.py` for to our LiveSectional directory.
- Updated `README.MD` to be a bit better.
