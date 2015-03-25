import lxml.html
import lxml.etree
import cStringIO

from logga.log import log

__all__ = ['Munger']


class Munger(object):

    def __init__(self):
        pass

    @staticmethod
    def remove_section(html, xpath):
        """Remove a section
        """
        root = lxml.html.fromstring(html)

        for element in root.xpath(xpath):
            element.getparent().remove(element)

            for ancestor in element.iterancestors():
                ancestor.getparent().remove(ancestor)
                if ancestor.tag == 'table':
                    break

        return lxml.html.tostring(root)
