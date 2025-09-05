#!/usr/bin/env python3
"""
Simple test script for calculator_interceptor.py
"""

import unittest
from unittest.mock import patch, MagicMock
import urllib.parse
import calculator_interceptor


class TestCalculatorInterceptor(unittest.TestCase):
    """Test cases for CalculatorInterceptor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.interceptor = calculator_interceptor.CalculatorInterceptor()
    
    def test_search_url_construction(self):
        """Test that the Google search URL is properly constructed."""
        expected_search_terms = "hung men turkey faced babies"
        expected_url = "https://www.google.com/search?q=" + urllib.parse.quote(expected_search_terms)
        
        self.assertEqual(calculator_interceptor.GOOGLE_SEARCH_URL, expected_url)
        self.assertEqual(calculator_interceptor.SEARCH_TERMS, expected_search_terms)
    
    def test_calculator_process_detection(self):
        """Test that calculator processes are correctly identified."""
        test_cases = [
            ("calc.exe", True),
            ("calculator.exe", True),
            ("Calculator.exe", True),
            ("calculatorapp.exe", True),
            ("Microsoft.WindowsCalculator.exe", True),
            ("notepad.exe", False),
            ("chrome.exe", False),
            ("CALC.EXE", True),  # Case insensitive
            ("", False),
        ]
        
        for process_name, expected in test_cases:
            with self.subTest(process_name=process_name):
                result = self.interceptor.is_calculator_process(process_name)
                self.assertEqual(result, expected, 
                               f"Process '{process_name}' should be {expected}")
    
    def test_monitored_pids_tracking(self):
        """Test that PID tracking works correctly."""
        # Initially empty
        self.assertEqual(len(self.interceptor.monitored_pids), 0)
        
        # Add some PIDs
        test_pids = [1234, 5678, 9999]
        for pid in test_pids:
            self.interceptor.monitored_pids.add(pid)
        
        self.assertEqual(len(self.interceptor.monitored_pids), 3)
        
        # Check PIDs are tracked
        for pid in test_pids:
            self.assertIn(pid, self.interceptor.monitored_pids)
    
    @patch('webbrowser.open')
    def test_open_google_search(self, mock_webbrowser):
        """Test that Google search opens correctly."""
        self.interceptor.open_google_search()
        
        mock_webbrowser.assert_called_once_with(calculator_interceptor.GOOGLE_SEARCH_URL)
    
    @patch('webbrowser.open', side_effect=Exception("Browser error"))
    @patch('calculator_interceptor.logging')
    def test_open_google_search_error_handling(self, mock_logging, mock_webbrowser):
        """Test error handling in open_google_search."""
        self.interceptor.open_google_search()
        
        # Should log an error
        mock_logging.error.assert_called()


def main():
    """Run the tests."""
    unittest.main()


if __name__ == "__main__":
    main()