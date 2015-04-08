import lxml.etree

from logga.log import log


__all__ = ['XpathGen']


class XpathGen(object):
    def __init__(self, conf_file=None):
        self.__conf_file = conf_file
        self.__root = None

        if conf_file is not None:
            self.root = conf_file

    @property
    def conf_file(self):
        return self.__conf_file

    @conf_file.setter
    def conf_file(self, value):
        self.__conf_file = value

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, value):
        if value is not None:
            self.__root = lxml.etree.parse(value)

    def extract_xpath(self, conf_file=None):
        """Wrapper method around the XPath generation facility.

        **Args:**
            *conf_file*:

        **Returns:**
            list of tuples representing the *remove* token
            and the corresponding xpath expression.  For example::

                [('r', '//table'), (...), ...]

            Specific to section removal is the ``r`` (*remove*) token
            that defines the action to perform on the section

        """
        if conf_file is None:
            conf_file = self.conf_file

        xpath_expressions = []
        if conf_file is None:
            log.warn('Configuration file undefined')
        else:
            # TODO: add the XPath generator worker methods
            pass

        return xpath_expressions

    @staticmethod
    def _extract_xpath_remove(tree):
        """Generate XPath expressions relating to section removal.
        *tree* is a :mod:`lxml.etree._ElementTree` object parses from
        the source XML-based configuration file

        **Args:**
            *tree*: :mod:`lxml.etree._ElementTree` structure

        **Returns:**
            list of tuples representing the *remove* token
            and the corresponding xpath expression.  For example::

                [('r', '//table'), (...), ...]

            Specific to section removal is the ``r`` (*remove*) token
            that defines the action to perform on the section

        """
        xpath_expressions = []

        for section_remover in tree.xpath('//Doc/Section/sectionRemover'):
            start_section = section_remover.xpath('../startSection')
            end_section = section_remover.xpath('../endSection')

            xpath = None
            if (len(end_section) == 0 or
               start_section[0].text == end_section[0].text):
                xpath = '//{0}'.format(start_section[0].text)

            log.debug('Generated sectionRemove xpath: "%s"' % xpath)
            xpath_expressions.append(('d', xpath))

        return xpath_expressions

    def parse_configuration(self):
        """Cycle through the configuration file defined by
        :attr:`root` and return a list of :class:`baip_munger.Munger`
        actions.

        **Returns:**
            list of :class:`baip_munger.Munger` actions of the form::

                [
                    {
                        'xpath': '<xpath_expr',
                        'attribute': 'class'
                    }
                ]

        """
        config_items = {'attributes': [],
                        'strip_chars': [],
                        'replace_tags': [],
                        'insert_tags': []}

        for section in self.root.xpath('//Doc/Section'):
            xpath = section.xpath('xpath/text()')

            if not len(xpath):
                continue

            delete_attrs = self._parse_delete_attributes(xpath[0], section)
            config_items.get('attributes').extend(delete_attrs)

            update_attrs = self._parse_update_attributes(xpath[0], section)
            config_items.get('attributes').extend(update_attrs)

            add_attrs = self._parse_add_attributes(xpath[0], section)
            config_items.get('attributes').extend(add_attrs)

            chars = self._parse_strip_chars(xpath[0], section)
            config_items.get('strip_chars').extend(chars)

            replace_tags = self._parse_replace_tag(xpath[0], section)
            config_items.get('replace_tags').extend(replace_tags)

            insert_tags = self._parse_insert_tag(xpath[0], section)
            config_items.get('insert_tags').extend(insert_tags)

        return config_items

    @staticmethod
    def _parse_delete_attributes(xpath, section):
        """Parse ``sectionDeleteAttribute`` element configuration items

        """
        config_items = []

        for action in section.xpath('sectionDeleteAttribute'):
            conf_item = {'xpath': xpath}
            attr = action.xpath('attributeName/text()')
            if len(attr):
                conf_item['attribute'] = attr[0]

                config_items.append(conf_item)

        return config_items

    @staticmethod
    def _parse_update_attributes(xpath, section):
        """Parse ``sectionUpdateAttribute`` config items.

        """
        config_items = []

        for action in section.xpath('sectionUpdateAttribute'):
            conf_item = {'xpath': xpath}
            attr = action.xpath('attributeName/text()')
            value = action.xpath('attributeValue/text()')
            if len(attr):
                conf_item['attribute'] = attr[0]
                if len(value):
                    conf_item['value'] = value[0]

                config_items.append(conf_item)

        return config_items

    @staticmethod
    def _parse_add_attributes(xpath, section):
        """Parse ``sectionAddAttribute`` config items.

        """
        config_items = []

        for action in section.xpath('sectionAddAttribute'):
            conf_item = {'xpath': xpath}
            attr = action.xpath('attributeName/text()')
            value = action.xpath('attributeValue/text()')
            log.debug('sectionAddAttribute attr|value: "%s|%s"' %
                      (attr, value))

            if len(attr):
                conf_item['attribute'] = attr[0]
                if len(value):
                    conf_item['value'] = value[0]
                conf_item['add'] = True

                config_items.append(conf_item)

        return config_items

    @staticmethod
    def _parse_strip_chars(xpath, section):
        """Parse ``sectionStripChars`` config items.

        """
        config_items = []

        for action in section.xpath('sectionStripChars'):
            conf_item = {'xpath': xpath}
            chars = action.xpath('stripChars/text()')
            log.debug('sectionStripChars value: "%s"' % chars)

            if len(chars):
                conf_item['chars'] = chars[0]

                config_items.append(conf_item)

        return config_items

    @staticmethod
    def _parse_replace_tag(xpath, section):
        """Parse ``sectionReplaceTag`` config items.

        """
        config_items = []

        for action in section.xpath('sectionReplaceTag'):
            conf_item = {'xpath': xpath}
            new_tag = action.xpath('newTag/text()')
            log.debug('sectionReplaceTag value: "%s"' % new_tag)

            if len(new_tag):
                conf_item['new_tag'] = new_tag[0]

                config_items.append(conf_item)

        return config_items

    @staticmethod
    def _parse_insert_tag(xpath, section):
        """Parse ``sectionInsertTag`` config items.

        """
        config_items = []

        for action in section.xpath('sectionInsertTag'):
            conf_item = {'xpath': xpath}
            new_tag = action.xpath('newTag/text()')
            log.debug('sectionInsertTag value: "%s"' % new_tag)

            if len(new_tag):
                conf_item['new_tag'] = new_tag[0]

                config_items.append(conf_item)

        return config_items
