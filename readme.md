# Apple Journal to Diarium (or maybe Diaro) Migration Tool

I just couldn't believe that this kind of Apple Journal migration tool still doesn't exist, so I made it myself.  
This tool allows you to migrate your entries from Apple Journal to Diarium by converting Apple Journal's HTML export to a format that can be imported into Diarium.  
Tested on Apple Journal backup from English and Korean language iPhone, and Diarium Android version.  

## Overview

This Python script parses the HTML export from Apple Journal and converts it into trimmed Diaro backup format, which can be imported into the Diarium app. The tool preserves your journal entries including titles, dates, content, and photos.  
While it uses Diaro's backup format, it's roughly trimmed for Diarium import and may not be compatible with Diaro directly. If you want to migrate to Diaro, refer "Notes" section below.  

## Prerequisites

- Python 3.x
- Apple Journal HTML export files
- Diarium app installed on your device

## How to Use

### Step 1: Export from Apple Journal
1. Export your journal entries from Apple Journal. (Settings -> Apps -> Journal -> Export All Journal Entries)
2. Unzip it. `AppleJournalEntries` might be there now.

### Step 2: Prepare the Script
1. Clone this repo or download as ZIP, then place `AppleJournalEntries` folder in the project root directory. (where readme.md and run.py exists)

### Step 3: Run the Script
python run.py

### Step 4: Set Your Timezone
- Enter your timezone offset when prompted. (values between -12 and 14)
- You can use decimal values for half-hour timezones. (e.g., 5.5 for +05:30)

### Step 5: Import to Diarium
1. The script will create a zip file named `Backup_[timestamp].zip`.
2. Open Diarium app.
3. Import the zip file as a "Diaro" backup.

## Notes

- This tool is specifically designed for migrating from Apple Journal to Diarium.
- While it uses Diaro's backup format, it's roughly trimmed for Diarium import and may not be compatible with Diaro directly.
- If you want to eventually import to Diaro, you can:
  1. Import the backup into Diarium first.
  2. Use Diarium's backup feature to create a `Diarium.diary` file.
  3. Import this file into Diaro, using import from Diarium feature. (tested)

## Troubleshooting

- If you encounter any file not found errors, make sure your `AppleJournalEntries` folder is correctly placed.

## Limitations

- The script preserves text content and photos, but may not transfer other types of attachments
- Some formatting or special features from Apple Journal might not be preserved in the migration
