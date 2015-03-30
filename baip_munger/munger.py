import lxml.html
import lxml.etree

from logga.log import log

__all__ = ['Munger']


class Munger(object):
    _root = None

    def __init__(self, html=None):
        if html is not None:
            self.root = html

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        log.debug('type html: %s' % type(value))
        self._root = lxml.html.fromstring(value)

    def dump_root(self):
        root = str()

        if self.root is not None:
            root = lxml.html.tostring(self._root)

        return root

    @staticmethod
    def remove_section(html, xpath, root_tag):
        """Remove a section from *html* based on the *xpath* expression.

        If *root_tag* is a nested ancestor of the *xpath* expression match
        then the section removal will stem from this level.

        **Args:**
            *html*: HTML document as a string

            *xpath*: standard XPath expression used to query against *html*

            *root_tag*: tag name of the ancestor element to remove if
            a match/matches are produced by *xpath*

        **Returns:**
            the resultant HTML document as a string

        """
        root = lxml.html.fromstring(html)

        log.debug('Section removal XPath: "%s"' % xpath)

        for element in root.xpath(xpath):
            log.debug('Removing element tag: "%s"' % element.tag)
            if element.tag == root_tag:
                element.getparent().remove(element)

            for ancestor in element.iterancestors():
                log.debug('Removing ancestor tag: "%s"' % ancestor.tag)
                ancestor.getparent().remove(ancestor)
                if ancestor.tag == root_tag:
                    break

        return lxml.html.tostring(root)

    def update_element_attribute(self, xpath, attribute, value=None):
        """Update element *attribute* from *xpath* expression search.

        If *value* is ``None`` then the attribute will be deleted.
        Otherwise, the existing attribute value will be replaced with
        the string contained within *value*.

        **Args:**
            *xpath*: standard XPath expression used to query against *html*

            *attribute*: element attribute name to remove

            *value*: if not ``None``, string to replace *attribute* value

        **Returns:**
            the resultant HTML document as a string

        """
        log.debug('Search/replace XPath: "%s"' % xpath)

        for tag in self.root.xpath(xpath):
            if value is None:
                log.debug('Removing attr "%s" from tag "%s"' % (attribute,
                                                                tag.tag))
                tag.attrib.pop(attribute)
            else:
                log.debug('Updating attr "%s" from tag "%s" with "%s"' %
                          (attribute, tag.tag, value))

                tag.attrib[attribute] = value
