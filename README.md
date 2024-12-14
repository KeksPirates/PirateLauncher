# PirateLauncher - A Download Manager/Launcher

## Description
PirateLauncher is a Python-based tool that simplifies downloading content using the Aria2 RPC interface. It provides keyboard shortcuts for managing downloads, including starting, pausing, and resuming. The launcher integrates seamlessly with the Aria2 service and displays download statuses in real-time.

## Features
- Start downloads via a predefined magnet URI.
- Pause and resume all active downloads using keyboard shortcuts.
- View detailed download information (name, speed, and status).
- Automatically launches Aria2 with RPC enabled for hassle-free operation.

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
   sudo apt install aria2  # For Debian/Ubuntu
   brew install aria2      # For macOS
   choco install aria2     # For Windows
   ```
3. Install the required Python libraries:
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

## Workflow
- PirateLauncher initializes an Aria2 RPC client to connect to a local `aria2c` instance.
- It launches Aria2 as a subprocess with RPC enabled, directing downloads to the system's Downloads folder.
- Users can control downloads using predefined keyboard shortcuts.
- The launcher monitors and prints download details, including speed and status, in real time.

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
- Edit the `magnet_uri` variable to set your desired download link.
- This tool is for educational purposes only. Use it responsibly.

## License
PirateLauncher is licensed under the MIT License. Refer to the LICENSE file for more information.

---

**Disclaimer:** PirateLauncher is intended for legal and ethical use only. Ensure compliance with applicable laws and regulations when using this tool.

