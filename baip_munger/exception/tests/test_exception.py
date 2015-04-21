import unittest2

import baip_munger.exception


class TestMungerConfigError(unittest2.TestCase):

    def test_error_code_1000(self):
        """Config file not found: code 1000.
        """
        try:
            raise baip_munger.exception.MungerConfigError(1000)
        except baip_munger.exception.MungerConfigError as received:
            expected = '1000: Config file not found'
            msg = 'TestMungerConfigError code 1000: error'
            self.assertEqual(str(received), expected, msg)

    def test_error_code_1001(self):
        """No config elements have been found: code 1001.
        """
        try:
            raise baip_munger.exception.MungerConfigError(1001)
        except baip_munger.exception.MungerConfigError as received:
            expected = '1001: No config elements have been defined'
            msg = 'TestMungerConfigError code 1001: error'
            self.assertEqual(str(received), expected, msg)
