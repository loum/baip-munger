import unittest2
import os

import baip_munger


class TestMunger(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        test_dir = os.path.join('baip_munger', 'tests', 'files')
        results_dir = os.path.join('baip_munger', 'tests', 'results')
        cls._results_dir = os.path.join('baip_munger', 'tests', 'results')
        test_html_page = 'source.htm'
        table_removed_html_page = 'source_with_table_removed.htm'
        p_removed_html_page = 'source_with_p_removed.htm'
        baip_generated = '1123-climate.htm'

        # Source HTML page.
        test_html_fh = open(os.path.join(test_dir, test_html_page))
        cls._source_html = test_html_fh.read()
        test_html_fh.close()

        # Source BAIP generated.
        test_html_fh = open(os.path.join(test_dir, baip_generated))
        cls._source_baip_generated = test_html_fh.read()
        test_html_fh.close()

        # Source with table removed HTML page.
        test_html_fh = open(os.path.join(results_dir,
                                         table_removed_html_page))
        cls._source_with_table_removed_html = test_html_fh.read()
        test_html_fh.close()

        # Source with nested paragraph removed HTML page.
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

    def test_update_element_attribute_delete_context(self):
        """Update element attribute: delete.
        """
        # Given a source HTML page
        html = self._source_baip_generated

        # and an xpath definition to target a HTML element
        xpath = "//table[@class='TableBAHeaderRow']/thead/tr/td/p"

        # and an attribute name to remove
        attr = 'align'

        # when I attempt to search and delete
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr)
        received = munger.dump_root()

        # the resultant HTML should present an omitted element attribute
        result_fh = open(os.path.join(self._results_dir,
                                      '1123-climate-remove-attr.htm'))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Attribute update: delete attribute error'
        self.assertEqual(received, expected, msg)

    def test_update_element_attribute_update_context(self):
        """Update element attribute: update.
        """
        # Given a source HTML page
        html = self._source_baip_generated

        # and an xpath definition to target a HTML element
        xpath = ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                 ('TableBAHeaderRow', 'TableHeading'))

        # and an attribute name to update
        attr = 'class'

        # and an attribute value to replace
        value = 'TableText'

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr, value)
        received = munger.dump_root()

        # the resultant HTML should present an omitted element attribute
        result_fh = open(os.path.join(self._results_dir,
                                      '1123-climate-update-attr.htm'))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Attribute update: update attribute error'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._source_html = None
        cls._results_dir = None
        cls._source_with_table_removed_html = None
        cls._source_with_p_removed_html = None
        cls._source_baip_generated = None
