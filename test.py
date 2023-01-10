"""Tests the PhemexBoy Module"""

from phemexboy.tests import api_tests

if __name__ == "__main__":
    if not api_tests.test_all():
        print("API Tests failed")
    else:
        print("All tests passed")
