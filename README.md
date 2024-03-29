# Day Tracker
This is a desktop program designed to help you track daily statistics. 

Navigate to this project's directory and run **python controller.py** to execute this program.

## Requirements
 * **Python 3** (developed on 3.9.4)
 * Some packages (run **pip install -r requirements.txt**) 

## Features
### Current
 * Each "Category" has an "Entry" for any given day.
   * An "Entry" can currently be a number, text, or time.
 * Ability to set runtime reminders for filling out certain category entries
 * Ability to create backups
   * Note: loading a backup is currently done manually by moving it to the project directory and naming it "tracker.db"

### To-do
 * Web sync
 * Load backups feature
 * Generate graphs for given time spans (Web version only)
 * Jump-to-date feature

## Known issues
 * Descriptions are currently unavailable
 * Math functions are currently unavailable
 * Float values throw an exception when being read
 * Terminal runs behind GUI
