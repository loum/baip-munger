import unittest2
import os
import tempfile

import baip_munger
from filer.files import (get_directory_files_list,
                         remove_files)


class TestMunger(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._test_dir = os.path.join('baip_munger', 'tests', 'files')
        results_dir = os.path.join('baip_munger', 'tests', 'results')
        cls._results_dir = os.path.join('baip_munger', 'tests', 'results')
        test_html_page = 'source.htm'
        table_removed_html_page = 'source_with_table_removed.htm'
        p_removed_html_page = 'source_with_p_removed.htm'
        baip_generated = '1123-climate.htm'
        baip_generated_dots = '1134-coal-and-hydrocarbons.htm'
        grouped_dots = 'BA-NSB-GLO-1.1-combined_clean.html'

        # Source HTML page.
        test_html_fh = open(os.path.join(cls._test_dir, test_html_page))
        cls._source_html = test_html_fh.read()
        test_html_fh.close()

        # Source BAIP generated.
        test_html_fh = open(os.path.join(cls._test_dir, baip_generated))
        cls._source_baip_generated = test_html_fh.read()
        test_html_fh.close()

        # Source BAIP generated: dots.
        test_html_fh = open(os.path.join(cls._test_dir, baip_generated_dots))
        cls._source_baip_generated_dots = test_html_fh.read()
        test_html_fh.close()

        # Source grouped dots.
        test_html_fh = open(os.path.join(cls._test_dir, grouped_dots))
        cls._source_grouped_dots = test_html_fh.read()
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

    def test_update_element_attribute_delete_missing_attr_context(self):
        """Update element attribute: delete missing attribute.
        """
        # Given a source HTML page
        html = self._source_baip_generated

        # and an xpath definition to target a HTML element
        xpath = "//table[@class='TableBAHeaderRow']/thead/tr/td/p"

        # and an undefined attribute name to remove
        attr = 'banana'

        # when I attempt to search and delete
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr)
        received = munger.dump_root()

        # the resultant HTML should unchanged
        expected = html
        msg = 'Attribute update: delete undefined attribute error'
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

        # and an old attribute value to match
        old_value = 'TableHeading'

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr, value, old_value)
        received = munger.dump_root()

        # the resultant HTML should present an updated element attribute
        result_fh = open(os.path.join(self._results_dir,
                                      '1123-climate-update-attr.htm'))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Attribute update: update attribute error'
        self.assertEqual(received, expected, msg)

    def test_update_element_attribute_recursive_update_context(self):
        """Update element attribute: recursive update.
        """
        # Given a source HTML page
        html = self._source_grouped_dots

        # and an xpath definition to target a HTML element
        xpath = ("//p[@class='%s']/span[@style='%s']" %
                 ('MsoBodyText', 'font-family:Symbol'))

        # and an attribute name to update
        attr = 'class'

        # and an attribute value to replace
        value = 'MsoListBullet'

        # and an attribute old attribute value to match and replace
        old_value = 'MsoBodyText'

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr, value, old_value)
        received = munger.dump_root()

        # the resultant HTML should present an updated element attribute
        result_file = 'BA-NSB-GLO-1.1-combined_clean_recursuve_attr_upd.html'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Attribute update: recursive update attribute error'
        self.assertEqual(received, expected, msg)

    def test_update_element_attribute_update_context_old_value_matched(self):
        """Update element attribute: update a matched old value.
        """
        # Given a source HTML page
        html = self._source_baip_generated

        # and an xpath definition to target a HTML element
        xpath = ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                 ('TableBAHeaderRow', 'TableHeading'))

        # and an attribute name to update
        attr = 'class'

        # and an old attribute value to target
        old_value = 'TableHeading'

        # and an attribute value to replace
        value = 'TableText'

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr, value, old_value)
        received = munger.dump_root()

        # the resultant HTML should present an omitted element attribute
        result_fh = open(os.path.join(self._results_dir,
                                      '1123-climate-update-attr.htm'))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Attribute matched old value update: update attribute error'
        self.assertEqual(received, expected, msg)

    def test_update_element_attribute_update_context_old_value_unmatched(self):
        """Update element attribute: update a unmatched old value.
        """
        # Given a source HTML page
        html = self._source_baip_generated

        # and an xpath definition to target a HTML element
        xpath = ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                 ('TableBAHeaderRow', 'TableHeading'))

        # and an attribute name to update
        attr = 'class'

        # and an old attribute value to target
        old_value = 'banana'

        # and an attribute value to replace
        value = 'TableText'

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr, value, old_value)
        received = munger.dump_root()

        # the resultant HTML should present an unchanged attribute
        expected = self._source_baip_generated
        msg = 'Attribute unmatched old value update: update attribute error'
        self.assertEqual(received, expected, msg)

    def test_update_element_attribute_update_context_no_add_if_missing(self):
        """Update element attribute: update no add if missing.
        """
        # Given a source HTML page
        html = self._source_baip_generated

        # and an xpath definition to target a HTML element
        xpath = ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                 ('TableBAHeaderRow', 'TableHeading'))

        # and an attribute name to update which is not defined
        attr = 'fruit'

        # and an attribute value
        value = 'banana'

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr, value)
        received = munger.dump_root()

        # the resultant HTML should not be altered
        expected = html
        msg = 'Attribute update: update attribute error add if missing'
        self.assertEqual(received, expected, msg)

    def test_update_element_attribute_add_context(self):
        """Update element attribute: add.
        """
        # Given a source HTML page
        html = self._source_baip_generated

        # and an xpath definition to target a HTML element
        xpath = ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                 ('TableBAHeaderRow', 'TableHeading'))

        # and an attribute name to add
        attr = 'style'

        # and an attribute value to replace
        value = 'margin-bottom:1.0pt'

        # when I attempt to search and add
        munger = baip_munger.Munger(html)
        munger.update_element_attribute(xpath, attr, value, add=True)
        received = munger.dump_root()

        # the resultant HTML should present an omitted element attribute
        result_fh = open(os.path.join(self._results_dir,
                                      '1123-climate-add-attr.htm'))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Attribute update: add attribute error'
        self.assertEqual(received, expected, msg)

    def test_replace_tag(self):
        """Replace element tag.
        """
        # Given a source HTML page
        html = self._source_baip_generated_dots

        # and an xpath definition to target a HTML element
        xpath = ("//p[@class='%s']" % 'MsoListBullet')

        # and an new tag name
        new_tag = 'li'

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.replace_tag(xpath, new_tag)
        received = munger.dump_root()

        # the resultant HTML should present an updated element
        result_file = '1134-coal-and-hydrocarbons-replace-tag.htm'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Element tag replace error'
        self.assertEqual(received, expected, msg)

    def test_replace_tag_and_add_new_attributes(self):
        """Replace element tag: add new attributes.
        """
        # Given a source HTML page
        html = self._source_baip_generated_dots

        # and an xpath definition to target a HTML element
        xpath = ("//p[@class='%s']" % 'MsoListBullet')

        # and an new tag name
        new_tag = 'li'

        # and the new tag's attributes
        new_tag_attributes = [('class', 'MsoListBullet')]

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.replace_tag(xpath, new_tag, new_tag_attributes)
        received = munger.dump_root()

        # the resultant HTML should present an updated element with new
        # attributes
        result_file = '1134-coal-and-hydrocarbons-replace-tag-new-attr.htm'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Element tag replace error'
        self.assertEqual(received, expected, msg)

    def test_replace_tag_and_add_new_boolean_attributes(self):
        """Replace element tag: add new boolean attributes.
        """
        # Given a source HTML page
        html = self._source_baip_generated_dots

        # and an xpath definition to target a HTML element
        xpath = ("//p[@class='%s']" % 'MsoListBullet')

        # and an new tag name
        new_tag = 'li'

        # and the new tag's boolean attributes
        new_tag_attributes = [('hidden', None)]

        # when I attempt to search and replace
        munger = baip_munger.Munger(html)
        munger.replace_tag(xpath, new_tag, new_tag_attributes)
        received = munger.dump_root()

        # the resultant HTML should present an updated element with
        # new boolean attributes
        result_file = '1134-coal-and-hydrocarbons-replace-tag-new-bool-attr.htm'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Element tag replace error'
        self.assertEqual(received, expected, msg)

    def test_insert_tag(self):
        """Insert parent element tag.
        """
        # Given a source HTML page
        html = self._source_baip_generated_dots

        # and an xpath definition to target a HTML element
        xpath = ("//p[@class='%s']" % 'MsoListBullet')

        # and a new parent tag name to insert
        new_tag = 'ul'

        # when I attempt to insert the new parent element
        munger = baip_munger.Munger(html)
        munger.insert_tag(xpath, new_tag)
        received = munger.dump_root()

        # the resultant HTML should present with the new parent element
        result_file = '1134-coal-and-hydrocarbons-insert-parent-element.htm'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Element tag insert error'
        self.assertEqual(received, expected, msg)

    def test_insert_tag_grouped_bullet_points_defect(self):
        """Insert parent element tag: grouped bullet points defect.
        """
        # Given a source HTML page
        html = self._source_grouped_dots

        # and an xpath definition to target a HTML element
        xpath = ("//p[@class='%s']" % 'MsoListBullet')

        # and a new parent tag name to insert
        new_tag = 'ul'

        # when I attempt to insert the new parent element
        munger = baip_munger.Munger(html)
        munger.insert_tag(xpath, new_tag)
        received = munger.dump_root()

        # the resultant HTML should present with the new parent element
        result_file = 'BA-NSB-GLO-1.1-combined_clean_insert_element.html'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Grouped element tag insert error'
        self.assertEqual(received, expected, msg)

    def test_strip_char(self):
        """Strip text from element tag text.
        """
        # Given a source HTML page
        html = self._source_baip_generated_dots

        # and an xpath definition to target a HTML element
        xpath = ("//p[@class='%s']" % 'MsoListBullet')

        # and a sub string to remove from the element tag
        text = u'\xb7 '

        # when I attempt to strip the text
        munger = baip_munger.Munger(html)
        munger.strip_char(xpath, text)
        received = munger.dump_root()

        # the resultant HTML should present with modified tag text
        result_file = '1134-coal-and-hydrocarbons-strip-text.htm'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Element tag text strip error'
        self.assertEqual(received, expected, msg)

    def test_munge(self):
        """Munge a file.
        """
        # Given a file to munge
        munge_infile = os.path.join(self._test_dir,
                                    'BA-NSB-GLO-1.1-combined_clean.html')

        # and a target munged file
        temp_dir = tempfile.mkdtemp()
        munge_outfile = os.path.join(temp_dir,
                                     'BA-NSB-GLO-1.1-combined_clean.html')

        # and a set of munging actions
        config_file = os.path.join(self._test_dir,
                                   'baip-munger-update-attr.xml')
        conf = baip_munger.XpathGen(config_file)
        actions = conf.parse_configuration()

        # when I perform a munge action
        munger = baip_munger.Munger()
        received = munger.munge(actions, munge_infile, munge_outfile)

        # then the munge should occur without error
        msg = 'Munger UI munge should return True'
        self.assertTrue(received, msg)

        # and the munged file deposited to the Munger target directory
        msg = 'Munged target file not created'
        self.assertTrue(os.path.exists(munge_outfile), msg)

        # Clean up
        remove_files(get_directory_files_list(temp_dir))
        os.removedirs(temp_dir)

    def test_munge_ordered_list(self):
        """Munge a file: ordered list.
        """
        # Given a file to munge
        test_file = 'BA-LEB-GAL-261-1-SWReview-v00_clean.html'
        munge_infile = os.path.join(self._test_dir, test_file)

        # and a target munged file
        temp_dir = tempfile.mkdtemp()
        munge_outfile = os.path.join(temp_dir, test_file)

        # and a set of munging actions with ordered list context
        config_file = os.path.join(self._test_dir,
                                   'baip-munger-ordered-list.xml')
        conf = baip_munger.XpathGen(config_file)
        actions = conf.parse_configuration()

        # when I perform a munge action
        munger = baip_munger.Munger()
        received = munger.munge(actions, munge_infile, munge_outfile)

        # then the munge should occur without error
        msg = 'Munger UI munge should return True'
        self.assertTrue(received, msg)

        # and the munged file deposited to the Munger target directory
        msg = 'Munged target file not created'
        self.assertTrue(os.path.exists(munge_outfile), msg)

        # Clean up
        remove_files(get_directory_files_list(temp_dir))
        os.removedirs(temp_dir)

    def test_munge_unordered_list(self):
        """Munge a file: unordered list.
        """
        # Given a file to munge
        test_file = 'unordered_source.html'
        munge_infile = os.path.join(self._test_dir, test_file)

        # and a target munged file
        temp_dir = tempfile.mkdtemp()
        munge_outfile = os.path.join(temp_dir, test_file)

        # and a set of munging actions with ordered list context
        config_file = os.path.join(self._test_dir,
                                   'baip-munger-unordered-list.xml')
        conf = baip_munger.XpathGen(config_file)
        actions = conf.parse_configuration()

        # when I perform a munge action
        munger = baip_munger.Munger()
        received = munger.munge(actions, munge_infile, munge_outfile)

        # then the munge should occur without error
        msg = 'Munger UI munge should return True'
        self.assertTrue(received, msg)

        # and the munged file deposited to the Munger target directory
        msg = 'Munged target file not created'
        self.assertTrue(os.path.exists(munge_outfile), msg)

        # the resultant HTML should present with modified tag text
        result_file = 'unordered.html'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Unordered list generation error'
        received = munger.dump_root()
        self.assertEqual(received, expected, msg)

        # Clean up
        remove_files(get_directory_files_list(temp_dir))
        os.removedirs(temp_dir)

    def test_munge_lists_combined(self):
        """Munge a file: lists combined.
        """
        # Given a file to munge
        test_file = 'list_source.html'
        munge_infile = os.path.join(self._test_dir, test_file)

        # and a target munged file
        temp_dir = tempfile.mkdtemp()
        munge_outfile = os.path.join(temp_dir, test_file)

        # and a set of munging actions with ordered list context
        config_file = os.path.join(self._test_dir,
                                   'baip-munger-lists.xml')
        conf = baip_munger.XpathGen(config_file)
        actions = conf.parse_configuration()

        # when I perform a munge action
        munger = baip_munger.Munger()
        received = munger.munge(actions, munge_infile, munge_outfile)

        # then the munge should occur without error
        msg = 'Munger UI munge should return True'
        self.assertTrue(received, msg)

        # and the munged file deposited to the Munger target directory
        msg = 'Munged target file not created'
        self.assertTrue(os.path.exists(munge_outfile), msg)

        # the resultant HTML should present with modified tag text
        result_file = 'lists.html'
        result_fh = open(os.path.join(self._results_dir, result_file))
        expected = result_fh.read().rstrip()
        result_fh.close()
        msg = 'Combined list generation error'
        received = munger.dump_root()
        self.assertEqual(received, expected, msg)

        # Clean up
        remove_files(get_directory_files_list(temp_dir))
        os.removedirs(temp_dir)

    def test_munge_missing_input_file(self):
        """Munge a file: missing input file.
        """
        # Given a file to munge
        munge_infile = 'banana'

        # and a target munged file
        temp_dir = tempfile.mkdtemp()
        munge_outfile = os.path.join(temp_dir,
                                     'BA-NSB-GLO-1.1-combined_clean.html')

        # and a set of munging actions
        config_file = os.path.join(self._test_dir,
                                   'baip-munger-update-attr.xml')
        conf = baip_munger.XpathGen(config_file)
        actions = conf.parse_configuration()

        # when I perform a munge action
        munger = baip_munger.Munger()
        received = munger.munge(actions, munge_infile, munge_outfile)

        # then the munge should occur without error
        msg = 'Munger UI munge (missing file) should return False'
        self.assertFalse(received, msg)

        # and the munged file should not be deposited to the Munger
        # target directory
        msg = 'Munged target file not created'
        self.assertFalse(os.path.exists(munge_outfile), msg)

        # Clean up
        remove_files(get_directory_files_list(temp_dir))
        os.removedirs(temp_dir)

    @classmethod
    def tearDownClass(cls):
        cls._test_dir = None
        cls._source_html = None
        cls._results_dir = None
        cls._source_with_table_removed_html = None
        cls._source_with_p_removed_html = None
        cls._source_baip_generated = None
        cls._source_baip_generated_dots = None
        cls._source_grouped_dots = None
