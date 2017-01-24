"""
Test code for file_signal_handler module.
"""
from __future__ import absolute_import, division
import os
import unittest
import file_signal_handler

class FileSignalHandlerTestCase(unittest.TestCase):
    "Test case class for FileSignalHandler class"
    def setUp(self):
        self.signal_file = './foo.txt'

    def tearDown(self):
        try:
            os.remove(self.signal_file)
        except OSError:
            pass

    def test_file_signal_handler(self):
        self.assertRaises(ValueError, file_signal_handler.FileSignalHandler,
                          '/foo/bar/foobar.txt')
        with open(self.signal_file, 'a'):
            os.utime(self.signal_file, None)
        self.assertRaises(RuntimeError, file_signal_handler.FileSignalHandler,
                          self.signal_file)

    def test_wait(self):
        handler = file_signal_handler.FileSignalHandler(self.signal_file)
        wait_interval = 1.
        poll_interval = 2.053
        self.assertRaises(ValueError, handler.wait, wait_interval,
                          poll_interval)

        wait_interval = 3.1
        elapsed_time = handler.wait(wait_interval, poll_interval)
        self.assertAlmostEqual(elapsed_time, wait_interval)

if __name__ == '__main__':
    unittest.main()
