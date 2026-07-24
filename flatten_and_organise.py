import re
import shutil
from pathlib import Path


def flatten_and_organize():
    root_dir = Path.cwd()
    script_path = Path(__file__).resolve() if '__file__' in globals() else None

    # Regex pattern matching: _(2-digit week)(1-digit lab).py at the end of the filename
    pattern = re.compile(r'_(\d{2})(\d)\.py$')

    print("--- PHASE 1: Flattening directory structure ---")
    flattened_count = 0

    # Collect all .py files in subdirectories (using list() so we don't mutate while iterating)
    nested_files = [
        f for f in root_dir.rglob("*.py")
        if f.parent != root_dir and f.resolve() != script_path
    ]

    for file_path in nested_files:
        destination = root_dir / file_path.name

        # Resolve filename collisions in the root directory before moving
        counter = 1
        while destination.exists():
            destination = root_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1

        print(f"Flattening: {file_path.relative_to(root_dir)}  ➔  {destination.name}")
        shutil.move(file_path, destination)
        flattened_count += 1

    print(f"Flattened {flattened_count} file(s).\n")

    print("--- PHASE 2: Organizing by Week and Lab ---")
    organized_count = 0

    # Scan root directory for all .py files
    for file_path in root_dir.glob("*.py"):
        # Skip the script itself
        if file_path.resolve() == script_path:
            continue

        match = pattern.search(file_path.name)
        if match:
            week_num = match.group(1)  # e.g., '05' or '10'
            lab_num = match.group(2)   # e.g., '1' or '2'

            # Build destination path: Week_WW/Lab_L/
            target_dir = root_dir / f"Week_{week_num}" / f"Lab_{lab_num}"
            target_dir.mkdir(parents=True, exist_ok=True)

            destination = target_dir / file_path.name

            print(f"Organizing: {file_path.name}  ➔  Week_{week_num}/Lab_{lab_num}/")
            shutil.move(file_path, destination)
            organized_count += 1
        else:
            print(f"Skipped (non-matching format): {file_path.name}")

    print(f"\nAll done! Flattened {flattened_count} file(s) and organized {organized_count} file(s).")


if __name__ == "__main__":
    flatten_and_organize()