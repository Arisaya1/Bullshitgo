# Bullshitgo

A Python script that intercepts Windows Calculator launches and redirects to Google search.

## What it does

This script monitors your system for Windows Calculator processes. When you try to open the calculator, it will:
1. Detect the calculator process starting
2. Terminate the calculator 
3. Open your default browser to a Google search instead

## Requirements

- Windows 10/11
- Python 3.6 or higher
- Administrative privileges (recommended)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Arisaya1/Bullshitgo.git
   cd Bullshitgo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script (preferably as Administrator):
   ```bash
   python calculator_interceptor.py
   ```

2. The script will start monitoring for calculator processes
3. Try to open Windows Calculator - it will be intercepted and redirected
4. Press `Ctrl+C` to stop the interceptor

## Features

- Monitors multiple calculator process variants (calc.exe, calculator.exe, etc.)
- Graceful process termination with fallback to force kill
- Logging to both console and file (`calculator_interceptor.log`)
- Memory-efficient PID tracking with cleanup
- Error handling and recovery

## How it works

The script uses the `psutil` library to monitor running processes in real-time. When it detects a calculator process:

1. It terminates the calculator process safely
2. Opens the configured Google search URL in your default browser
3. Continues monitoring for future calculator launches

## Disclaimer

This is a prank/joke script. Use responsibly and only on systems you own or have permission to modify.