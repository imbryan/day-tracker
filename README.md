# Day Tracker
This is a desktop program designed to help you track daily statistics. Currently requires python to be installed. Navigate to this project's directory and run **python controller.py** to execute this script.

## Features
### Current
 * Graphical user interface
 * Ability to create "category" & "data value" pairs for any given day
   * Categories can have descriptions
 * Ability to sum (numerical) values for months and years
 * Ability to average (numerical) values for months and years
 * Ability to set runtime reminders for filling out certain category entries
 * Ability to create backups
   * Note: loading a backup is currently done manually by moving it to the project directory and naming it "tracker.db"

### To-do
 * Button to load backups
 * Select category from list to lookup
 * Better interface for creating categories, including selecting data type
 * Generate graphs for given time spans
 * Compile an executable
 * Maybe make it easier to jump to non-adjacent days

## Known issues
 * Float values throw an exception when being read
 * Terminal runs behind GUI for now
