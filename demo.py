#!/usr/bin/env python3
"""
Demo script to show the Google search URL that would be opened.
This is safe to run and won't interfere with your calculator.
"""

import webbrowser
import urllib.parse
from calculator_interceptor import SEARCH_TERMS, GOOGLE_SEARCH_URL


def main():
    """Demonstrate the search functionality."""
    print("Calculator Interceptor Demo")
    print("=" * 30)
    print(f"Search terms: {SEARCH_TERMS}")
    print(f"Google URL: {GOOGLE_SEARCH_URL}")
    print()
    
    choice = input("Open the Google search URL? (y/n): ").lower().strip()
    
    if choice in ('y', 'yes'):
        print("Opening browser...")
        webbrowser.open(GOOGLE_SEARCH_URL)
        print("Done!")
    else:
        print("Demo complete without opening browser.")


if __name__ == "__main__":
    main()