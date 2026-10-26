
from pathlib import Path
import shutil
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

DOWNLOADS = Path.home() / "Downloads"

FOLDERS = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".tx"],
    "Programs": [".deb", ".AppImage", ".xz", ".msi", ".exe", ".sh", ".AppImage"],
}

TEMP_SUFFIXES = (".part", ".crdownload", ".tmp")


def organize_file(file_path: Path):
    if not file_path.is_file():
        return

    if file_path.name.lower().endswith(TEMP_SUFFIXES):
        return

    for folder_name, extensions in FOLDERS.items():
        if file_path.suffix.lower() in extensions:
            destination_folder = DOWNLOADS / folder_name
            destination_folder.mkdir(parents=True, exist_ok=True)

            destination = destination_folder / file_path.name

            if destination.exists():
                print(f"Skipped duplicate: {file_path.name}")
                return

            shutil.move(str(file_path), str(destination))
            print(f"Organized: {file_path.name} -> {folder_name}/")
            return

    print(f"No category found for: {file_path.name}")


def wait_until_ready(file_path: Path):
    """Wait until a new file's size stops changing."""
    previous_size = -1
    stable_checks = 0

    for _ in range(30):
        if not file_path.exists():
            return

        try:
            current_size = file_path.stat().st_size
        except OSError:
            time.sleep(1)
            continue

        if current_size == previous_size:
            stable_checks += 1
        else:
            stable_checks = 0

        if stable_checks >= 2:
            organize_file(file_path)
            return

        previous_size = current_size
        time.sleep(1)

    print(f"Skipped file that may still be downloading: {file_path.name}")


class OrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            path = Path(event.src_path)

            if path.parent == DOWNLOADS:
                wait_until_ready(path)

    def on_moved(self, event):
        if not event.is_directory:
            path = Path(event.dest_path)

            if path.parent == DOWNLOADS:
                wait_until_ready(path)


def main():
    DOWNLOADS.mkdir(parents=True, exist_ok=True)

    for folder_name in FOLDERS:
        (DOWNLOADS / folder_name).mkdir(exist_ok=True)

    # Organize files already in the test folder.
    for file_path in list(DOWNLOADS.iterdir()):
        if file_path.is_file():
            organize_file(file_path)

    observer = Observer()
    observer.schedule(OrganizerHandler(), str(DOWNLOADS), recursive=False)
    observer.start()

    print(f"Automatic organizer is running!")
    print(f"Watching: {DOWNLOADS}")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping organizer...")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
