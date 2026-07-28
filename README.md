# CSC1004 File Organizer

A simple Python utility script to consolidate and organize lab files for **CSC1004: Computer Programming II** at Dublin City University (DCU). I wrote this for CSC1004 but with hopes that other modules use similar naming conventions and I can reuse the script.

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
> **Note:** I haven't tested this on TermCast, only my personal machine running Linux using the download provided by Einstein, use at your own risk.

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
---

## Changelog

### [2.0.0] - Interactive CLI & Safety Update - 28/07/2026

#### Added
* **Interactive Terminal Menu:** Choose between full run, flatten only, organize only, or dry run without editing code.
* **Working Directory Display:** Menu now explicitly shows the target folder path before running actions.
* **Dry Run Mode:** Preview all file moves and renames without making actual changes to the filesystem.
* **Collision Protection:** Automatically appends `_dupX` suffixes if a file with the same name already exists in the destination.
* **Execution Logging:** Automatically generates an `organizer_log.txt` file recording all moved files and timestamps.
* **Terminal UI:** Added ANSI color styling, structured tree output, and a post-run breakdown showing file counts by week.

#### Changed
* Loop now returns to the main menu after execution instead of exiting immediately.
* Filter skips existing `Week_XX` directories during phase 1 flattening to prevent recursive looping on re-runs.

---

### [1.0.0] - Initial Release - 22/07/2026

#### Added
* Recursive directory flattening for `.py` files.
* Auto-sorting based on `_WWL.py` regex naming pattern into `Week_WW/Lab_L` directory structure.
