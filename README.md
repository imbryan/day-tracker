# Day Tracker
This is a desktop program designed to help you track daily statistics. 

Navigate to this project's directory and run **python controller.py** to execute this program.

## Requirements
 * **Python 3** (developed on 3.9.4)
 * Some packages (run **pip install -r requirements.txt**) 


## Building an executable (optional)
 * Run **pyinstaller controller.py**. 
 * The executable will be found at "dist/controller/controller.exe". 
   * Note: if you run the program with the executable, it will use "dist/controller/" as its root directory (meaning that the databases under "dist/controller/" will be used instead of those at the project root).

## Features
### Current
 * Each "Category" has an "Entry" for any given day.
   * An "Entry" can currently be a number, text, or time.
 * Ability to set runtime reminders for filling out certain category entries
 * Ability to create backups
   * Note: loading a backup is currently done manually by moving it to the project directory and naming it "tracker.db"

### To-do
 * Web sync
 * Button to load backups
 * Generate graphs for given time spans (Web version only)
 * Make a streamlined executable that doesn't require convoluted instructions
 * Make it easier to jump to non-adjacent days

## Known issues
 * Descriptions are currently unavailable
 * Math functions are currently unavailable
 * Float values throw an exception when being read
 * Terminal runs behind GUI
