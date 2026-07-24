# CSC1004 File Organizer

A simple Python utility script to consolidate and organize lab files for **CSC1004: Computer Programming II** at Dublin City University (DCU).

### What it does

If your lab files are buried inside multiple subfolders or scattered around your directory, this script cleans everything up in two quick steps:

1. **Flattens the directory:** Pulls all `.py` files out of nested subfolders and moves them into the main directory (renaming duplicates automatically to prevent overwriting).
2. **Organizes by Week and Lab:** Reads the `_WWL.py` naming pattern (e.g., `count_102.py` for Week 10, Lab 2) and sorts every file into structured folders:

```text
Week_05/
└── Lab_1/
    └── rain_051.py
Week_10/
└── Lab_2/
    └── count_102.py
