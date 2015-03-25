import unittest2

import baip_munger


class TestXpathGen(unittest2.TestCase):

    def test_init(self):
        """Initialise a baip_munger.XpathGen()
        """
        munger = baip_munger.XpathGen()
        msg = 'Object is not a baip_munger.XpathGen'
        self.assertIsInstance(munger, baip_munger.XpathGen, msg)
