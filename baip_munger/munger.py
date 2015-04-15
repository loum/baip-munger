import lxml.html
import lxml.etree
import lxml.html.builder

from logga.log import log

__all__ = ['Munger']


class Munger(object):
    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, value):
        if value is not None:
            self.__root = lxml.html.fromstring(value)

    def __init__(self, html=None):
        self.__root = None

        if html is not None:
            self.root = html

    def dump_root(self):
        root = str()

        if self.root is not None:
            root = lxml.html.tostring(self.__root)

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

    def update_element_attribute(self,
                                 xpath,
                                 attribute,
                                 value=None,
                                 old_value=None,
                                 add=False):
        """Update element *attribute* from *xpath* expression search.

        If *value* is ``None`` then the attribute will be deleted.
        Otherwise, the existing attribute value will be replaced with
        the string contained within *value*.

        If the *attribute* is not part of the tag definition and
        *add* is set to ``True`` then the attribute will be added

        **Args:**
            *xpath*: standard XPath expression used to query against *html*

            *attribute*: element attribute name to action

            *value*: if not ``None``, string to replace *attribute* value

            *old_value*: if not ``None``, old string to match *attribute*
            value against before a replacement occurs

            *add*: boolean flag which if set, will add the attribute
            if it already not part of the tag definition

        """
        def update_attr(element, attribute, value, old_value):
            log.debug('Updating attr "%s" from tag "%s" with "%s"' %
                      (attribute, element.tag, value))

            if old_value is not None:
                if element.attrib[attribute] == old_value:
                    element.attrib[attribute] = value
            else:
                element.attrib[attribute] = value

        def recursive_update_attr(element, attribute, value, old_value):
            if element.attrib.get(attribute) is not None:
                update_attr(element, attribute, value, old_value)

            # Now, perform the check recursively for each parent.
            parent = element.getparent()
            while parent is not None:
                if parent.attrib.get(attribute) is not None:
                    update_attr(parent, attribute, value, old_value)

                parent = parent.getparent()

        log.debug('Update attribute XPath: "%s"' % xpath)

        for tag in self.root.xpath(xpath):
            if value is None:
                if add:
                    log.debug('Adding attr "%s" from tag "%s"' %
                              (attribute, tag.tag))
                    tag.attrib[attribute] = str()
                elif tag.attrib.get(attribute):
                    log.debug('Removing attr "%s" from tag "%s"' %
                              (attribute, tag.tag))
                    tag.attrib.pop(attribute)
            else:
                if add:
                    log.debug('Adding attr "%s" from tag "%s" with "%s"' %
                              (attribute, tag.tag, value))

                    tag.attrib[attribute] = value
                # else tag.attrib.get(attribute) is not None:
                else:
                    recursive_update_attr(tag,
                                          attribute,
                                          value,
                                          old_value)

    def replace_tag(self, xpath, new_tag):
        """Replace element tag from *xpath* expression search to
        *new_tag*.

        **Args:**
            *xpath*: standard XPath expression used to query against *html*

            *new_tag*: new element tag name to replace

        """
        log.info('Replace element tag XPath: "%s"' % xpath)

        for tag in self.root.xpath(xpath):
            log.debug('Replacing element tag "%s" with "%s"' %
                      (tag.tag, new_tag))
            new_element = lxml.etree.Element(new_tag)
            new_element.text = tag.text_content()
            tag.getparent().replace(tag, new_element)

    def insert_tag(self, xpath, new_tag):
        """Insert *new_tag* element tag from *xpath* expression search.

        Workflow is:

            * identify elements from XPath expression
            * group same parent/sequential elements
            * construct new HTML element based on *new_tag*
            * insert into :att:`root` :mod:`lxml.html` tree

        **Args:**
            *xpath*: standard XPath expression used to query against
            *html*

            *new_tag*: new element tag name to replace as a string.
            Method will convert to a :mod:`lxml.etree.Element`

        """
        def build_xml(new_tag, tags_to_extend):
            new_element = lxml.etree.Element(new_tag)
            new_element.extend(tags_to_extend)
            xml = lxml.etree.XML(lxml.etree.tostring(new_element))

            return xml

        def child_xml_insert(start_index, node_count, parent_element, xml):
            insert_index = start_index - node_count + 1
            log.info('Child element insert "%s ..." at index: %d' %
                     (lxml.html.tostring(xml)[:70], insert_index))
            parent_element.insert(insert_index, xml)

        log.info('Insert element tag XPath: "%s"' % xpath)

        tags = self.root.xpath(xpath)
        current_parent = None
        prev_index = None
        tags_to_extend = []
        tags_to_extend_index = []

        for tag in tags:
            parent = tag.getparent()
            index = parent.index(tag)

            if current_parent is None:
                current_parent = parent
                log.debug('Set current parent %s:"%s"' %
                          (current_parent, current_parent.tag))
                tags_to_extend.append(tag)
                tags_to_extend_index.append(index)
                continue

            if parent == current_parent:
                if prev_index is None or index == (prev_index + 1):
                    prev_index = index
                    tags_to_extend.append(tag)
                    tags_to_extend_index.append(index)
                    continue
                else:
                    log.debug('Sequential index interrupted: inserting')
            else:
                log.debug('Parent change: inserting')

            xml = build_xml(new_tag, tags_to_extend)
            if parent != current_parent:
                current_parent.insert(index, xml)
                current_parent = parent
                log.debug('Set current parent %s:"%s"' %
                          (current_parent, current_parent.tag))
            else:
                child_xml_insert(prev_index,
                                 len(tags_to_extend),
                                 current_parent,
                                 xml)

            # Reset our control variables.
            prev_index = None
            del tags_to_extend[:]
            tags_to_extend.append(tag)
            del tags_to_extend_index[:]
            tags_to_extend_index.append(index)

        # Insert the laggards (if any).
        if len(tags_to_extend_index):
            xml = build_xml(new_tag, tags_to_extend)
            child_xml_insert(prev_index,
                             len(tags_to_extend),
                             current_parent,
                             xml)

    def strip_char(self, xpath, chars):
        """Strip *chars* from *xpath* expression search.

        **Args:**
            *xpath*: standard XPath expression used to query against *html*

            *chars*: characters to strip from the element tag text

        """
        log.info('Strip chars XPath expression: "%s"' % xpath)

        for tag in self.root.xpath(xpath):
            for child_tag in tag.iter():
                if child_tag.text is not None:
                    log.debug('Stipping "%s" from tag "%s" text: "%s"' %
                              (chars, child_tag.tag, child_tag.text))
                    child_tag.text = child_tag.text.strip(chars)
                    log.debug('Resultant text: "%s"' % child_tag.text)
                    if child_tag.tail is not None:
                        log.debug('Stipping tail text: "%s" from "%s"' %
                                  (chars, child_tag.tail))
                        child_tag.tail = child_tag.tail.strip(chars)
                        log.debug('Resultant tail text: "%s"' %
                                  child_tag.tail)
