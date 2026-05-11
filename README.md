# Smart File Organizer

A Python-based command-line automation tool that organizes messy folders into structured categories such as images, videos, documents, audio, and archives.

This project was built to practice real-world Python automation, file handling, logging, and command-line interface development.

---

## Features

* Automatically categorizes files based on extension
* Creates folders automatically if they do not exist
* Prevents duplicate file overwriting using dynamic renaming
* Supports dry-run mode to preview changes safely
* Logs all file operations into a log file
* Displays execution summary after processing
* Handles unknown file types safely using an `Others` folder
* Command-line interface using `argparse`

---

## Technologies Used

* Python
* pathlib
* shutil
* logging
* argparse

---

## Project Structure

```text
smart-file-organizer/
│
├── organizer.py
├── organizer.log
├── .gitignore
├── README.md
└── venv/
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AdityaSahu959/smart-file-organizer.git
cd smart-file-organizer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows (PowerShell)

```bash
venv\Scripts\Activate
```

#### Windows (CMD)

```bash
venv\Scripts\activate.bat
```

---

## Usage

### Normal Mode

```bash
python organizer.py "C:\Projects\TestFolder"
```

### Dry Run Mode

```bash
python organizer.py "C:\Projects\TestFolder" --dry-run
```

Dry-run mode previews all actions without actually moving files.

---

## Example Output

```text
[DRY RUN] Would move photo.jpg -> Images
[DRY RUN] Would move notes.txt -> Documents
[DRY RUN] Would move song.mp3 -> Audio

===== Summary =====
Total files processed: 3
Images: 1
Videos: 0
Documents: 1
Audio: 1
Archives: 0
Others: 0
```

---

## Example Folder Structure

### Before

```text
TestFolder/
│
├── photo.jpg
├── notes.txt
├── song.mp3
├── movie.mp4
```

### After

```text
TestFolder/
│
├── Images/
│   └── photo.jpg
│
├── Documents/
│   └── notes.txt
│
├── Audio/
│   └── song.mp3
│
├── Videos/
│   └── movie.mp4
```

---

## Future Improvements

* Recursive directory traversal
* Automatic scheduling support
* GUI version using Tkinter or PyQt
* Executable (.exe) generation
* Custom user-defined categories

---

## Learning Outcomes

This project helped practice:

* Python automation
* File system operations
* Command-line interface development
* Logging and debugging
* Defensive programming
* Git and GitHub workflow

---

## Author

Aditya Sahu

GitHub: [https://github.com/AdityaSahu959](https://github.com/AdityaSahu959)
