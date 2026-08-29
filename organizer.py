from pathlib import Path
import shutil
import logging
import argparse
import json


logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def load_config(config_path="config.json"):
    config_file = Path(config_path)

    if not config_file.exists():
        print("Configuration file not found.")
        logging.error("Configuration file not found.")
        return None

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            file_types = json.load(file)

        return file_types

    except json.JSONDecodeError:
        print("Invalid JSON format in configuration file.")
        logging.error("Invalid JSON format in configuration file.")
        return None

    except OSError as error:
        print(f"Error reading configuration file: {error}")
        logging.error(f"Error reading configuration file: {error}")
        return None


def organize_folder(folder_path, dry_run=False, recursive=False):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist.")
        return

    logging.info("========== New Session ==========")

    file_types = load_config()

    if file_types is None:
        return

    summary = {category: 0 for category in file_types}
    summary["Others"] = 0

    # Create category folders
    for category in file_types:
        (folder / category).mkdir(exist_ok=True)

    (folder / "Others").mkdir(exist_ok=True)

    # Determine which files should be processed
    if recursive:
        excluded_folders = list(file_types.keys()) + ["Others"]

        files_to_process = [
            file
            for file in folder.rglob("*")
            if file.is_file()
            and file.relative_to(folder).parts[0]
            not in excluded_folders
        ]

    else:
        files_to_process = [
            file
            for file in folder.iterdir()
            if file.is_file()
        ]

    # Process files
    for file in files_to_process:

        moved = False

        for category, extensions in file_types.items():

            if file.suffix.lower() in extensions:

                destination = folder / category / file.name

                # Handle duplicate filenames
                counter = 1

                while destination.exists():
                    destination = (
                        folder
                        / category
                        / f"{file.stem}_{counter}{file.suffix}"
                    )
                    counter += 1

                # Move file unless dry-run is enabled
                if not dry_run:
                    shutil.move(
                        str(file),
                        str(destination)
                    )

                if dry_run:
                    message = (
                        f"[DRY RUN] Would move "
                        f"{file.name} -> {category}"
                    )
                else:
                    message = (
                        f"Moved "
                        f"{file.name} -> {category}"
                    )

                print(message)
                logging.info(message)

                summary[category] += 1
                moved = True

                break

        # Handle unknown file types
        if not moved:

            destination = folder / "Others" / file.name

            # Handle duplicate filenames
            counter = 1

            while destination.exists():
                destination = (
                    folder
                    / "Others"
                    / f"{file.stem}_{counter}{file.suffix}"
                )
                counter += 1

            # Move file unless dry-run is enabled
            if not dry_run:
                shutil.move(
                    str(file),
                    str(destination)
                )

            if dry_run:
                message = (
                    f"[DRY RUN] Would move "
                    f"{file.name} -> Others"
                )
            else:
                message = (
                    f"Moved "
                    f"{file.name} -> Others"
                )

            print(message)
            logging.info(message)

            summary["Others"] += 1

    # Display summary
    print("\n===== Summary =====")

    total = sum(summary.values())

    print(f"Total files processed: {total}")

    for category, count in summary.items():
        print(f"{category}: {count}")

    # Log summary
    logging.info(f"Total files processed: {total}")
    logging.info("===============================")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Smart File Organizer"
    )

    parser.add_argument(
        "path",
        help="Path of folder to organize"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process files inside subfolders"
    )

    args = parser.parse_args()

    organize_folder(
        args.path,
        dry_run=args.dry_run,
        recursive=args.recursive
    )