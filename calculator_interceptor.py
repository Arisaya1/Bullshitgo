#!/usr/bin/env python3
"""
Calculator Interceptor Script

This script monitors for Windows Calculator processes and redirects to a Google search
when the calculator is launched.

Requirements:
- Windows 10/11
- Python 3.6+
- psutil library

Usage:
    python calculator_interceptor.py

Note: Run as administrator for better process management capabilities.
"""

import time
import webbrowser
import psutil
import urllib.parse
from typing import Set
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calculator_interceptor.log'),
        logging.StreamHandler()
    ]
)

# Search terms to redirect to
SEARCH_TERMS = "hung men turkey faced babies"
GOOGLE_SEARCH_URL = "https://www.google.com/search?q=" + urllib.parse.quote(SEARCH_TERMS)

# Calculator process names to monitor
CALCULATOR_PROCESSES = {
    'calc.exe',           # Classic Windows Calculator
    'calculator.exe',     # Windows 10/11 Calculator
    'Calculator.exe',     # Case variation
    'calculatorapp.exe',  # UWP Calculator
    'Microsoft.WindowsCalculator.exe'  # Windows Store Calculator
}

class CalculatorInterceptor:
    """Monitors and intercepts Windows Calculator launches."""
    
    def __init__(self):
        self.monitored_pids: Set[int] = set()
        self.running = True
        
    def is_calculator_process(self, process_name: str) -> bool:
        """Check if the process name matches any calculator variants."""
        return process_name.lower() in {name.lower() for name in CALCULATOR_PROCESSES}
    
    def kill_process_safely(self, proc: psutil.Process) -> bool:
        """Safely terminate a process."""
        try:
            proc.terminate()
            # Wait for process to terminate gracefully
            proc.wait(timeout=3)
            logging.info(f"Successfully terminated calculator process: {proc.name()} (PID: {proc.pid})")
            return True
        except psutil.TimeoutExpired:
            try:
                # Force kill if graceful termination fails
                proc.kill()
                logging.info(f"Force killed calculator process: {proc.name()} (PID: {proc.pid})")
                return True
            except Exception as e:
                logging.error(f"Failed to kill process {proc.pid}: {e}")
                return False
        except Exception as e:
            logging.error(f"Error terminating process {proc.pid}: {e}")
            return False
    
    def open_google_search(self):
        """Open the Google search in the default browser."""
        try:
            webbrowser.open(GOOGLE_SEARCH_URL)
            logging.info(f"Opened Google search: {SEARCH_TERMS}")
        except Exception as e:
            logging.error(f"Failed to open browser: {e}")
    
    def scan_for_calculators(self):
        """Scan for running calculator processes."""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Skip if we've already processed this PID
                    if proc.info['pid'] in self.monitored_pids:
                        continue
                    
                    # Check if it's a calculator process
                    if self.is_calculator_process(proc.info['name']):
                        logging.info(f"Detected calculator process: {proc.info['name']} (PID: {proc.info['pid']})")
                        
                        # Add to monitored PIDs to avoid duplicate processing
                        self.monitored_pids.add(proc.info['pid'])
                        
                        # Get the actual process object
                        calculator_proc = psutil.Process(proc.info['pid'])
                        
                        # Kill the calculator
                        if self.kill_process_safely(calculator_proc):
                            # Open Google search
                            self.open_google_search()
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process may have ended or we don't have permission
                    continue
                except Exception as e:
                    logging.debug(f"Error checking process {proc.info['pid']}: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error during process scan: {e}")
    
    def cleanup_monitored_pids(self):
        """Remove PIDs of processes that no longer exist."""
        current_pids = {proc.info['pid'] for proc in psutil.process_iter(['pid'])}
        self.monitored_pids &= current_pids
    
    def run(self, scan_interval: float = 1.0):
        """
        Main monitoring loop.
        
        Args:
            scan_interval: Time in seconds between process scans
        """
        logging.info("Calculator Interceptor started")
        logging.info(f"Monitoring for calculator processes: {', '.join(CALCULATOR_PROCESSES)}")
        logging.info(f"Will redirect to: {GOOGLE_SEARCH_URL}")
        logging.info("Press Ctrl+C to stop")
        
        try:
            while self.running:
                self.scan_for_calculators()
                
                # Cleanup monitored PIDs every 10 scans to prevent memory growth
                if len(self.monitored_pids) > 100:
                    self.cleanup_monitored_pids()
                
                time.sleep(scan_interval)
                
        except KeyboardInterrupt:
            logging.info("Stopping calculator interceptor...")
            self.running = False
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            raise


def main():
    """Main entry point."""
    interceptor = CalculatorInterceptor()
    
    try:
        interceptor.run()
    except Exception as e:
        logging.error(f"Failed to start interceptor: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())