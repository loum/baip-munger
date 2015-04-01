import unittest2
import os
import lxml.etree

import baip_munger


class TestXpathGen(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
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

    def test_parse_configuration(self):
        """Parse configuration.
        """
        # Given a Munger configuration file with target xpath expression
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-update-attr.xml')
        xpathgen = baip_munger.XpathGen(conf_file)

        # when I parse a sectionDeleteAttribute configuration element
        received = xpathgen.parse_configuration()

        # then I should receive a list of dictionary structures of the
        # form
        # [{'xpath': '<xpath_expr>',
        #   'attribute': '<attr_name>'},
        #  {...}]
        expected = {
            'attributes': [
                {
                    'xpath':
                        "//table[@class='TableBAHeaderRow']/thead/tr/td/p",
                    'attribute': 'class',
                },
                {
                    'xpath':
                        ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                         ('TableBAHeaderRow', 'TableHeading')),
                    'attribute': 'class',
                    'value': 'TableText',
                },
                {
                    'xpath':
                        ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                         ('TableBAHeaderRow', 'TableHeading')),
                    'attribute': 'style',
                    'value': 'margin-bottom:1.0pt',
                    'add': True,
                },
                {
                    'xpath':
                        "//table[@class='TableBAHeaderRow']/thead/tr/td",
                    'attribute': 'width',
                    'value': '68',
                    'add': True,
                },
                {
                    'xpath':
                        "//table[@class='TableBAHeaderRow']/thead/tr/td",
                    'attribute': 'nowrap',
                    'add': True,
                },
            ],
            'strip_chars': [
                {
                    'xpath': "//p[@class='MsoListBullet']",
                    'chars': u'\xb7 '
                }
            ],
            'replace_tags': [
                {
                    'xpath': "//p[@class='MsoListBullet']",
                    'new_tag': 'li'
                }
            ],
            'insert_tags': [
                {
                    'xpath': "//div/li",
                    'new_tag': 'ul'
                }
            ],
        }
        msg = 'Config item error'
        self.assertDictEqual(received, expected, msg)

    def test_parse_delete_attributes(self):
        """Parse delete attributes config items.
        """
        # Given a Munger configuration file with target xpath expression
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-update-attr.xml')
        xpathgen = baip_munger.XpathGen(conf_file)
        xpath = "//table[@class='TableBAHeaderRow']/thead/tr/td/p"
        section = xpathgen.root.xpath('//Doc/Section')

        # when I parse a sectionDeleteAttribute configuration element
        # section[0] is the "sectionDeleteAttribute" element
        received = xpathgen._parse_delete_attributes(xpath, section[0])

        # then I should receive a list of dictionary structures of the
        # form
        # [{'xpath': '<xpath_expr>',
        #   'attribute': '<attr_name>'}]
        expected = [
            {
                'xpath': "//table[@class='TableBAHeaderRow']/thead/tr/td/p",
                'attribute': 'class',
            },
        ]
        msg = 'Delete attribute config items error'
        self.assertListEqual(received, expected, msg)

    def test_parse_update_attributes(self):
        """Parse update attributes config items.
        """
        # Given a Munger configuration file with target xpath expression
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-update-attr.xml')
        xpathgen = baip_munger.XpathGen(conf_file)
        xpath = ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                 ('TableBAHeaderRow', 'TableHeading'))
        section = xpathgen.root.xpath('//Doc/Section')

        # when I parse a sectionDeleteAttribute configuration element
        # section[1] is the "sectionUpdateAttribute" element
        received = xpathgen._parse_update_attributes(xpath, section[1])

        # then I should receive a list of dictionary structures of the
        # form
        # [{'xpath': '<xpath_expr>',
        #   'attribute': '<attr_name>'}]
        expected = [
            {
                'xpath':
                    ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                     ('TableBAHeaderRow', 'TableHeading')),
                'attribute': 'class',
                'value': 'TableText',
            }
        ]
        msg = 'Update attribute config items error'
        self.assertListEqual(received, expected, msg)

    def test_parse_add_attributes(self):
        """Parse add attributes config items.
        """
        # Given a Munger configuration file with target xpath expression
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-update-attr.xml')
        xpathgen = baip_munger.XpathGen(conf_file)
        xpath = ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                 ('TableBAHeaderRow', 'TableHeading'))
        section = xpathgen.root.xpath('//Doc/Section')

        # when I parse a sectionDeleteAttribute configuration element
        # section[2] is the "sectionAddAttribute" element
        received = xpathgen._parse_add_attributes(xpath, section[2])

        # then I should receive a list of dictionary structures of the
        # form
        # [{'xpath': '<xpath_expr>',
        #   'attribute': '<attr_name>'}]
        expected = [
            {
                'xpath':
                    ("//table[@class='%s']/thead/tr/td/p[@class='%s']" %
                     ('TableBAHeaderRow', 'TableHeading')),
                'attribute': 'style',
                'value': 'margin-bottom:1.0pt',
                'add': True,
            }
        ]
        msg = 'Add attribute config items error'
        self.assertListEqual(received, expected, msg)

    def test_parse_strip_chars(self):
        """Parse strip characters config items.
        """
        # Given a Munger configuration file with target xpath expression
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-update-attr.xml')
        xpathgen = baip_munger.XpathGen(conf_file)
        xpath = "//p[@class='MsoListBullet']"
        section = xpathgen.root.xpath('//Doc/Section')

        # when I parse a sectionStripChars configuration element
        # section[4] is the "sectionStripChars" element
        received = xpathgen._parse_strip_chars(xpath, section[4])

        # then I should receive a list of dictionary structures of the
        # form
        # [{'xpath': '<xpath_expr>',
        #   'chars': '<chars>'}]
        expected = [
            {
                'xpath': "//p[@class='MsoListBullet']",
                'chars': u'\xb7 ',
            }
        ]
        msg = 'Strip chars config items error'
        self.assertListEqual(received, expected, msg)

    def test_parse_replace_tag(self):
        """Parse replace tag config items.
        """
        # Given a Munger configuration file with target xpath expression
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-update-attr.xml')
        xpathgen = baip_munger.XpathGen(conf_file)
        xpath = "//p[@class='MsoListBullet']"
        section = xpathgen.root.xpath('//Doc/Section')

        # when I parse a sectionReplaceTag configuration element
        # section[5] is the "sectionReplaceTag" element
        received = xpathgen._parse_replace_tag(xpath, section[5])

        # then I should receive a list of dictionary structures of the
        # form
        # [{'xpath': '<xpath_expr>',
        #   'new_tag': '<new_tag>'}]
        expected = [
            {
                'xpath': "//p[@class='MsoListBullet']",
                'new_tag': 'li',
            }
        ]
        msg = 'Replace tag config items error'
        self.assertListEqual(received, expected, msg)

    def test_parse_insert_tag(self):
        """Parse insert tag config items.
        """
        # Given a Munger configuration file with target xpath expression
        conf_file = os.path.join(self._conf_dir,
                                 'baip-munger-update-attr.xml')
        xpathgen = baip_munger.XpathGen(conf_file)
        xpath = "//p[@class='MsoListBullet']"
        section = xpathgen.root.xpath('//Doc/Section')

        # when I parse a sectionInsertTag configuration element
        # section[6] is the "sectionInsertTag" element
        received = xpathgen._parse_insert_tag(xpath, section[6])

        # then I should receive a list of dictionary structures of the
        # form
        # [{'xpath': '<xpath_expr>',
        #   'new_tag': '<new_tag>'}]
        expected = [
            {
                'xpath': "//p[@class='MsoListBullet']",
                'new_tag': 'ul',
            }
        ]
        msg = 'Insert tag config items error'
        self.assertListEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._conf_dir = None
        cls._conf_path = None
        cls._element_tree = None
