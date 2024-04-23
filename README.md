# Day Tracker
This is a desktop program designed to help you track daily statistics. 

## Requirements
 * **Python 3** (developed on 3.12.2)
 * Some Python packages (run **pip install -r requirements.txt**) 

 ## How to Run
 * Navigate to this project's root directory and run **python controller.py** to run this program.
   * Note: if your Python installation recognizes .py files, you can simply create a shortcut for **controller.py** and run it like that.

## Features
### Current
 * Each "Category" has an "Entry" for any given day.
   * An "Entry" can currently be a number, text, or time.
 * Ability to set runtime reminders for filling out certain category entries
 * Ability to create backups
   * Note: at the moment, backup loading must be performed manually. Day Tracker uses the database file called **tracker.db** located in the root project directory. You can substitute any backup as long as you rename it to "tracker.db".

### To-do
 * Load backup feature
 * Generate graphs for given time spans (Web interface)
 * Jump-to-date feature

## Known issues
 * Descriptions are currently unavailable
 * Math functions are currently unavailable
 * Float values throw an exception when being read
 * Terminal runs behind GUI
