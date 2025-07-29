# SoftwareManager - A Download Manager/Launcher

## Description
SoftwareManager is a Python-based GUI/TUI tool that simplifies downloading and managing pirated software from various sources.

## Features
- Start downloads via a predefined magnet URI.
- View detailed download information (name, speed, and status).

## Requirements
- Python 3.x
- `aria2c` (installed and available in your PATH)
- Python libraries:
  - `aria2p`
  - `keyboard`

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install Aria2:
   ```bash
   sudo apt install aria2  # For Debian/Ubuntu/Mint
   paru/yay -S aria2       # For Arch from AUR
   brew install aria2      # For macOS
   choco install aria2     # For Windows
   ```

## Example
Run the following command to launch SoftwareManager and control downloads:

```bash
python main.py
```

Press `d` to start the predefined download, `s` to pause, and `q` to quit.

## Notes
- Aria2 must be installed and accessible from your command line.
- This tool is for educational purposes only. Use it responsibly.

---

**Disclaimer:** SoftwareManager is intended for legal and ethical use only. Ensure compliance with applicable laws and regulations when using this tool.

