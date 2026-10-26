# Python Downloads Organizer 📂

An automatic file organizer built with Python that monitors your Ubuntu Downloads folder and sorts files into categorized folders based on their file extensions.

Instead of manually organizing downloaded files, this tool detects new files and moves supported file types into the appropriate folders automatically.

## ✨ Features

- **Automatic file monitoring** — detects new files using `watchdog`.
- **File categorization** — organizes files into folders based on their extensions.
- **Supported categories:**
  - 📄 Documents: PDF, DOC, DOCX, TXT, XLSX, PPTX
  - 🖼️ Images: JPG, JPEG, PNG, GIF, WEBP
  - 🎬 Videos: MP4, MKV, MOV, AVI
  - 🎵 Music: MP3, WAV, AAC, FLAC, OGG, M4A, WMA
  - 📦 Archives: ZIP, RAR, 7Z, TAR, GZ
  - 💻 Programs: DEB, AppImage
- **Duplicate protection** — avoids overwriting files with the same name.
- **Temporary download protection** — skips common temporary download files.
- **Background operation** — can run as a systemd user service on Ubuntu.
- **Existing file organization** — organizes supported files already in the Downloads folder when it starts.

## 🛠️ Technologies Used

- Python 3
- Watchdog
- pathlib
- shutil
- systemd (for automatic startup on Ubuntu)

## 📋 Requirements

- Ubuntu Linux or another compatible Linux distribution
- Python 3
- Python virtual environment support
- pip

## 🚀 Installation

### 1. Clone the repository

```bash
git clone git@github.com:singbah/file-organizer.git
cd file-orgainzer
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

If virtual environment support is missing on Ubuntu:

```bash
sudo apt update
sudo apt install python3-venv -y
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install watchdog
```

## ▶️ Usage

Run the organizer with:

```bash
python organizer.py
```

The application monitors your Downloads folder and automatically organizes supported files as they arrive.

Press `Ctrl + C` to stop the application when running it in the terminal.

## ⚙️ Automatic Startup on Ubuntu

You can configure the organizer to start automatically when you log in using a systemd user service.

Create the service directory:

```bash
mkdir -p ~/.config/systemd/user
```

Create the service file:

```bash
nano ~/.config/systemd/user/download-organizer.service
```

Add the following configuration:

```ini
[Unit]
Description=Automatic Downloads Folder Organizer
After=default.target

[Service]
Type=simple
WorkingDirectory=%h/python-automation/download-organizer
ExecStart=%h/python-automation/download-organizer/.venv/bin/python %h/python-automation/download-organizer/organizer.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

**Important:** Update `WorkingDirectory` and `ExecStart` if your project is installed in a different location.

Enable and start the service:

```bash
systemctl --user daemon-reload
systemctl --user enable --now download-organizer.service
```

Check its status:

```bash
systemctl --user status download-organizer.service
```

View logs:

```bash
journalctl --user -u download-organizer.service -f
```

Stop the service:

```bash
systemctl --user stop download-organizer.service
```

Disable automatic startup:

```bash
systemctl --user disable --now download-organizer.service
```

## 📁 Folder Structure

```text
download-organizer/
├── organizer.py
├── README.md
└── .venv/
```

The `.venv/` directory should not be committed to GitHub. Add it to `.gitignore`.

Example `.gitignore`:

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
```

## ⚠️ Important Notes

- The organizer moves supported files from your Downloads folder into category folders.
- Unsupported file types remain in the Downloads folder.
- Files with duplicate names are skipped rather than overwritten.
- The organizer should be tested with sample files before being used on important files.
- The systemd service configuration assumes the project is installed at `~/python-automation/download-organizer`; update it for your installation path.

## 🔮 Future Improvements

- Add more file categories and extensions.
- Support custom categories through a configuration file.
- Add logging and error reporting.
- Provide a graphical user interface.
- Support configurable destination folders.
- Add a dry-run mode to preview file movements before applying them.

## 👨‍💻 Author

Created as a Python automation project to practice file handling, event monitoring, and Linux automation.

## 📄 License

This project is open source. Add a license file if you want others to reuse, modify, and distribute the code. The MIT License is one common option.
