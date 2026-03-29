"""
picker.py
Pick a script from the bank deterministically by day-of-year
(cycles through all scripts, no randomness needed).
Copies it into daily/YYYY-MM-DD_<name>.py for the daily commit.
"""

import datetime
import glob
import os
import shutil

today = datetime.date.today()

scripts = sorted(glob.glob("bank/**/*.py", recursive=True))
if not scripts:
    print("No scripts found in bank/")
    exit(1)

chosen = scripts[today.toordinal() % len(scripts)]
name = os.path.basename(chosen)
dest = f"daily/{today}_{name}"

os.makedirs("daily", exist_ok=True)
shutil.copy2(chosen, dest)

print(f"Today's script: {chosen}")
print(f"Copied to:      {dest}")
