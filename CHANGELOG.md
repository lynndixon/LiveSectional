# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

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
