import unittest2
import os

import baip_munger


class TestMunger(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        test_dir = os.path.join('baip_munger', 'tests', 'files')
        results_dir = os.path.join('baip_munger', 'tests', 'results')
        test_html_page = 'source.htm'
        table_removed_html_page = 'source_with_table_removed.htm'
        p_removed_html_page = 'source_with_p_removed.htm'

        # Source HTML page
        test_html_fh = open(os.path.join(test_dir, test_html_page))
        cls._source_html = test_html_fh.read()
        test_html_fh.close()

        # Source with table removed HTML page
        test_html_fh = open(os.path.join(results_dir,
                                         table_removed_html_page))
        cls._source_with_table_removed_html = test_html_fh.read()
        test_html_fh.close()

        # Source with nested paragraph removed HTML page
        test_html_fh = open(os.path.join(results_dir,
                                         p_removed_html_page))
        cls._source_with_p_removed_html = test_html_fh.read()
        test_html_fh.close()

    def test_init(self):
        """Initialise a baip_munger.Munger()
        """
        munger = baip_munger.Munger()
        msg = 'Object is not a baip_munger.Munger'
        self.assertIsInstance(munger, baip_munger.Munger, msg)

    def test_remove_section_table(self):
        """Remove a table section from the HTML page.
        """
        # Given a source HTML page
        html = self._source_html

        # and an xpath definition to target a table section to remove
        xpath = '//table[contains(@summary, "Log of issues and comments")]'

        # when I attempt to remove a section
        munger = baip_munger.Munger()
        received = munger.remove_section(html, xpath, 'table')

        # the resultant HTML should present an omitted table structure
        expected = self._source_with_table_removed_html
        msg = 'Section removed error: table'
        self.assertEqual(received, expected, msg)

    def test_remove_section_paragraph(self):
        """Remove a paragraph section from the HTML page.
        """
        # Given a source HTML page
        html = self._source_html

        # and an xpath definition to target a paragraph section to remove
        xpath = '//p/*[text()="History of this document"]'

        # when I attempt to remove a section
        munger = baip_munger.Munger()
        received = munger.remove_section(html, xpath, 'p')

        # the resultant HTML should present an omitted paragraph structure
        expected = self._source_with_p_removed_html
        msg = 'Section removed error: paragraph'
        self.assertEqual(received, expected, msg)

    def test_remove_section_not_found(self):
        """Remove a unmatched section from the HTML page.
        """
        # Given a source HTML page
        html = self._source_html

        # and an xpath definition to target a missing section to remove
        xpath = '//p/*[text()="Banana"]'

        # when I attempt to remove a section
        munger = baip_munger.Munger()
        received = munger.remove_section(html, xpath, 'p')

        # the resultant HTML should present an unchanged structure
        expected = self._source_html.rstrip()
        msg = 'Section removed error: unmatched section'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._source_html = None
        cls._source_with_table_removed_html = None
        cls._source_with_p_removed_html = None
