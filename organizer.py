import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

CLR = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"

PATTERN = re.compile(r'_(\d{2})(\d)(?:_dup\d+)?\.py$')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(root_dir):
    print(f"  {DIM}╭────────────────────────────────────╮{CLR}")
    print(f"  {DIM}│{CLR}      {BOLD}DCU Lab File Organizer{CLR}        {DIM}│{CLR}")
    print(f"  {DIM}╰────────────────────────────────────╯{CLR}")
    print(f"  {DIM}Working In:{CLR} {CYAN}{root_dir}{CLR}\n")

def show_menu(root_dir):
    clear_screen()
    print_header(root_dir)
    
    options = [
        ("1", "Flatten + Organize", "Run full pipeline"),
        ("2", "Flatten Only", "Pull .py files out of subfolders"),
        ("3", "Organize Only", "Sort root files into Week_XX/Lab_Y/"),
        ("4", "Dry Run", "Simulate without moving files"),
        ("0", "Exit", "Close organizer")
    ]

    print(f"  {BOLD}MAIN MENU{CLR}")
    print(f"  {DIM}╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌{CLR}")
    for key, name, desc in options:
        print(f"   {CYAN}[{key}]{CLR} {BOLD}{name:<20}{CLR} {DIM}{desc}{CLR}")
    print(f"  {DIM}╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌{CLR}\n")

    while True:
        choice = input(f"  {MAGENTA}❯{CLR} Select option: ").strip()
        if choice in {"0", "1", "2", "3", "4"}:
            return choice
        print(f"  {RED}✘ Invalid option. Try again.{CLR}")

def confirm(prompt):
    res = input(f"\n  {YELLOW}⚠ {prompt} (y/N): {CLR}").strip().lower()
    return res == "y"

def flatten(root_dir, script_path, dry_run, log_lines):
    print(f"\n  {BOLD}┌── PHASE 1: Flattening Directory Structure{CLR}")
    flattened_count = 0
    claimed = set()

    nested_files = [
        f for f in root_dir.rglob("*.py")
        if f.parent != root_dir
        and f.resolve() != script_path
        and not any(part.startswith("Week_") for part in f.relative_to(root_dir).parts)
    ]

    if not nested_files:
        print(f"  {DIM}│  No nested files found to flatten.{CLR}")
        print(f"  {BOLD}└── Finished Phase 1{CLR}")
        return 0

    for file_path in nested_files:
        destination = root_dir / file_path.name

        counter = 1
        while destination.exists() or destination.name in claimed:
            destination = root_dir / f"{file_path.stem}_dup{counter}{file_path.suffix}"
            counter += 1
        claimed.add(destination.name)

        tag = f" {YELLOW}(renamed duplicate){CLR}" if destination.name != file_path.name else ""
        action = f"{YELLOW}Would Flatten{CLR}" if dry_run else f"{GREEN}Flattened{CLR}"
        
        print(f"  │  {action}: {DIM}{file_path.relative_to(root_dir)}{CLR} ➔ {BOLD}{destination.name}{CLR}{tag}")
        log_lines.append(f"FLATTEN: {file_path.relative_to(root_dir)} -> {destination.name}")

        if not dry_run:
            shutil.move(file_path, destination)
        flattened_count += 1

    print(f"  {BOLD}└── Phase 1 Complete:{CLR} {flattened_count} file(s) processed.")
    return flattened_count

def organize(root_dir, script_path, dry_run, log_lines):
    print(f"\n  {BOLD}┌── PHASE 2: Organizing by Week & Lab{CLR}")
    organized_count = 0
    week_summary = defaultdict(int)
    claimed = set()

    for file_path in sorted(root_dir.glob("*.py")):
        if file_path.resolve() == script_path:
            continue

        match = PATTERN.search(file_path.name)
        if not match:
            print(f"  │  {DIM}Skipped (non-matching format): {file_path.name}{CLR}")
            continue

        week_num, lab_num = match.group(1), match.group(2)
        target_dir = root_dir / f"Week_{week_num}" / f"Lab_{lab_num}"
        destination = target_dir / file_path.name

        if destination.exists() or destination in claimed:
            counter = 1
            while destination.exists() or destination in claimed:
                destination = target_dir / f"{file_path.stem}_dup{counter}{file_path.suffix}"
                counter += 1
            tag = f" {YELLOW}(renamed duplicate){CLR}"
        else:
            tag = ""
        claimed.add(destination)

        action = f"{YELLOW}Would Organize{CLR}" if dry_run else f"{GREEN}Organized{CLR}"
        dest_rel = f"Week_{week_num}/Lab_{lab_num}/{destination.name}"
        
        print(f"  │  {action}: {BOLD}{file_path.name}{CLR} ➔ {CYAN}{dest_rel}{CLR}{tag}")
        log_lines.append(f"ORGANIZE: {file_path.name} -> {dest_rel}")

        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(file_path, destination)

        organized_count += 1
        week_summary[f"Week_{week_num}"] += 1

    print(f"  {BOLD}└── Phase 2 Complete:{CLR} {organized_count} file(s) organized.")

    if week_summary:
        print(f"\n  {BOLD}Breakdown by Week:{CLR}")
        for week in sorted(week_summary):
            print(f"   {CYAN}•{CLR} {week}: {BOLD}{week_summary[week]}{CLR} file(s)")

    return organized_count

def write_log(root_dir, log_lines, dry_run):
    if dry_run or not log_lines:
        return
    log_path = root_dir / "organizer_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"\n--- Run at {timestamp} ---\n")
        f.write("\n".join(log_lines) + "\n")
    print(f"\n  {DIM}Detailed log saved to {log_path.name}{CLR}")

def run(choice, root_dir, script_path):
    dry_run = choice == "4"
    do_flatten = choice in {"1", "2", "4"}
    do_organize = choice in {"1", "3", "4"}
    log_lines = []

    if dry_run:
        print(f"\n  {MAGENTA}ℹ [DRY RUN MODE] Simulating operations without changing files.{CLR}")

    if do_flatten and not dry_run:
        if not confirm("This will move .py files out of subfolders into the root directory. Proceed?"):
            print(f"\n  {RED}Operation cancelled by user.{CLR}")
            return

    flattened_count = flatten(root_dir, script_path, dry_run, log_lines) if do_flatten else 0
    organized_count = organize(root_dir, script_path, dry_run, log_lines) if do_organize else 0

    write_log(root_dir, log_lines, dry_run)

    verb = "Would have processed" if dry_run else "Successfully processed"
    print(f"\n  {GREEN}{BOLD}✔ Done!{CLR} {verb} {BOLD}{flattened_count}{CLR} flattened, {BOLD}{organized_count}{CLR} organized.\n")

def main():
    root_dir = Path.cwd()
    script_path = Path(__file__).resolve()

    while True:
        choice = show_menu(root_dir)
        if choice == "0":
            print(f"\n  {CYAN}Goodbye!{CLR}\n")
            break

        run(choice, root_dir, script_path)
        
        input(f"  {DIM}Press Enter to return to the menu...{CLR}")

if __name__ == "__main__":
    main()