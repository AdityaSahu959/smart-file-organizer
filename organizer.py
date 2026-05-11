from pathlib import Path
import shutil
import logging
import argparse

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def organize_folder(folder_path, dry_run=False):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist.")
        return

    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Videos": [".mp4", ".mkv", ".avi"],
        "Documents": [".pdf", ".docx", ".txt"],
        "Audio": [".mp3", ".wav"],
        "Archives": [".zip", ".rar"],
    }

    summary = {
    "Images": 0,
    "Videos": 0,
    "Documents": 0,
    "Audio": 0,
    "Archives": 0,
    "Others": 0
     }

    for category in file_types:
        (folder / category).mkdir(exist_ok=True)

    for file in folder.iterdir():
        if file.is_file():
            moved = False

            for category, extensions in file_types.items():
                if file.suffix.lower() in extensions:
                    destination = folder / category / file.name

                    counter = 1
                    while destination.exists():
                        destination = folder / category / f"{file.stem}_{counter}{file.suffix}"
                        counter += 1

                    if not dry_run:
                        shutil.move(str(file), str(destination))

                    if dry_run:
                        message = f"[DRY RUN] Would move {file.name} -> {category}"
                    else:
                        message = f"Moved {file.name} -> {category}"
                    print(message)
                    logging.info(message)
                    summary[category] += 1
                    moved = True
                    break

            if not moved:
                (folder / "Others").mkdir(exist_ok=True)
                destination = folder / "Others" / file.name

                counter = 1
                while destination.exists():
                    destination = folder / "Others" / f"{file.stem}_{counter}{file.suffix}"
                    counter += 1
                shutil.move(str(file), str(destination))
                if dry_run:
                    message = f"[DRY RUN] Would move {file.name} -> Others"
                else:
                    message = f"Moved {file.name} -> Others"
                
                print(message)
                logging.info(message)
                summary[category] += 1
    print("\n===== Summary =====")

    total = sum(summary.values())

    print(f"Total files processed: {total}")

    for category, count in summary.items():
        print(f"{category}: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart File Organizer")
    parser.add_argument("path", help="Path of folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")

    args = parser.parse_args()

    organize_folder(args.path, dry_run=args.dry_run)