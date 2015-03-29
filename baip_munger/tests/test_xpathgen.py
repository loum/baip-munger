import unittest2
import os
import lxml.etree

import baip_munger


class TestXpathGen(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._conf_dir = os.path.join('baip_munger', 'tests', 'files')
        conf_file = 'baip-munger.xml'
        cls._conf_path = os.path.join(cls._conf_dir, conf_file)

        cls._conf_element_tree = lxml.etree.parse(cls._conf_path)

    def test_init(self):
        """Initialise a baip_munger.XpathGen()
        """
        munger = baip_munger.XpathGen()
        msg = 'Object is not a baip_munger.XpathGen'
        self.assertIsInstance(munger, baip_munger.XpathGen, msg)

    def test_extract_xpath_no_conf_file(self):
        """Extract XPath expressions: no configuration file.
        """
        # Given an undefined Munger configuration file.
        conf_file = None

        # when I attempt to extract the XPath expressions
        xpathgen = baip_munger.XpathGen(conf_file)
        received = xpathgen.extract_xpath()

        # then I should received an empty list
        expected = []
        msg = 'XPath expression extraction should produce empty list'
        self.assertListEqual(received, expected, msg)

    def test_extract_xpath_remove(self):
        """Extract XPath sections to remove from configuration.
        """
        # Given a Munger configuration file with a single tag name of
        # "table" under the "startSection" element
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-table-only.xml')
        conf_element_tree = lxml.etree.parse(conf_file)

        # when I parse a sectionRemover configuration element
        xpathgen = baip_munger.XpathGen()
        received = xpathgen._extract_xpath_remove(conf_element_tree)

        # then I should receive a list of tuple structures of the form
        # [('d', '//table')]
        expected = [('d', '//table')]
        msg = 'Section remove XPath expressions list error'
        self.assertListEqual(received, expected, msg)

    def test_extract_xpath_remove_no_end_element(self):
        """Extract XPath sections to remove from configuration: no end.
        """
        # Given a Munger configuration file with a single tag name of
        # "table" under the "startSection" element
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-table-only-no-end.xml')
        conf_element_tree = lxml.etree.parse(conf_file)

        # when I parse a sectionRemover configuration element
        xpathgen = baip_munger.XpathGen()
        received = xpathgen._extract_xpath_remove(conf_element_tree)

        # then I should receive a list of tuple structures of the form
        # [('d', '//table')]
        expected = [('d', '//table')]
        msg = 'Section remove XPath expressions list error'
        self.assertListEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._conf_dir = None
        cls._conf_path = None
        cls._element_tree = None
