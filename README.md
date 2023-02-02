# Day Tracker
This is a desktop program designed to help you track daily statistics. Requires **Python 3** (developed on 3.9.4) as well as some packages (run **pip install -r requirements.txt**). 

Navigate to this project's directory and run **python controller.py** to execute this script.

You can also build an executable by running **pyinstaller controller.py**. The exe will be found at "dist/controller/controller.exe". Note: if you run the program with the exe, it will use "dist/controller/" as its root directory (meaning that the databases under "dist/controller/" will be used instead of those at the project root).

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
 * Make a streamlined executable that doesn't require convoluted instructions
 * Make it easier to jump to non-adjacent days

## Known issues
 * Float values throw an exception when being read
 * Terminal runs behind GUI
