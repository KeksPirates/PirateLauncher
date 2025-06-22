# PirateLauncher - A Download Manager/Launcher

## Description
PirateLauncher is a Python-based GUI/TUI tool that simplifies downloading and managing pirated software from various sources.

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
4. Install the required Python libraries:
   ```bash
   pip install aria2p keyboard
   ```

## Usage
1. Clone or download PirateLauncher to your local machine.
2. Run the launcher:
   ```bash
   python pirate_launcher.py
   ```
3. Use the following keyboard controls:
   - Press **`d`** to start/resume a download.
   - Press **`s`** to pause all downloads.
   - Press **`q`** to quit the launcher.


## Configuration
- To use a different magnet URI, update the `magnet_uri` variable in the script.
- Ensure the RPC port (default: 6800) is open and accessible.

## Example
Run the following command to launch PirateLauncher and control downloads:

```bash
python pirate_launcher.py
```

Press `d` to start the predefined download, `s` to pause, and `q` to quit.

## Notes
- Aria2 must be installed and accessible from your command line.
- This tool is for educational purposes only. Use it responsibly.

---

**Disclaimer:** PirateLauncher is intended for legal and ethical use only. Ensure compliance with applicable laws and regulations when using this tool.

