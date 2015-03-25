import lxml.html
import lxml.etree

from logga.log import log

__all__ = ['Munger']


class Munger(object):

    def __init__(self):
        pass

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
