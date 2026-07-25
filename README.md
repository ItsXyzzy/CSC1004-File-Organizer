# CSC1004 File Organizer

A simple Python utility script to consolidate and organize lab files for **CSC1004: Computer Programming II** at Dublin City University (DCU).

---

## Overview

If your lab files are buried inside multiple subfolders or scattered around your directory, this script cleans everything up in two quick steps:

1. **Flattens the directory:** Pulls all `.py` files out of nested subfolders and moves them into the main root folder (renaming duplicates automatically so nothing gets overwritten).
2. **Organizes by Week and Lab:** Reads the `_WWL.py` naming pattern (e.g., `count_102.py` for Week 10, Lab 2) and sorts every file into structured folders:

```text
Week_05/
└── Lab_1/
    └── rain_051.py
Week_10/
└── Lab_2/
    └── count_102.py
```

## Instructions

### Prerequisites

* **Python 3.6 or higher** installed on your system.
* No external libraries required (uses standard modules: `pathlib`, `shutil`, and `re`).

### Setup

1. Copy the `organizer.py` file into the main folder where your lab files or subfolders are located.

### How to Run

Open your terminal or command prompt, navigate to your folder, and run:

```bash
python organizer.py

```

### File Naming Format

For the auto-sorting phase to work, your Python files must follow the course standard naming format ending in `_WWL.py`:

* `WW` = Two-digit week number (e.g., `05`, `10`)
* `L` = Single-digit lab number (e.g., `1`, `2`)

**Examples:**

* `rain_051.py` ➔ Moved to `Week_05/Lab_1/`
* `count_102.py` ➔ Moved to `Week_10/Lab_2/`

> **Note:** Any file that does not match this pattern (as well as `organizer.py` itself) will remain untouched in the root directory.

> **Note:** I haven't tested this on TermCast, only my personal machine running Linux using the download provided by Einstein, use at your own risk.
