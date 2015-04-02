.. BAIP Munger documentation master file

BAIP - Munger
=============

Contents
--------
.. toctree::
    :maxdepth: 1

    contents.rst

--------------

The BAIP Munger is a fit-for-purpose HTML transposer tool.

BAIP Munger takes static HTML files as input and matches sections
with the HTML according to the :ref:`configuration`.  BAIP Munger
configuration also defines the actions that can be performed on the
HTML.

Currently supported actions include:

* Section removal

* Element attribute control - add, edit and delete element attrbutes)

* Element tag rename

* Element tag insertion

* Element text character removal

Usage
-----

Command Line
^^^^^^^^^^^^

Assuming you are using the global configuration file (which is in
``/etc/baip/conf/munger.xml``) ::

    $ baip-munger --help
    usage: baip-munger [-h] [-c CONFIG_FILE] infile outfile
    
    BAIP Munger Tool
    
    positional arguments:
      infile                Source HTML file to munge
      outfile               Munged HTML file

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_FILE, --config-file CONFIG_FILE

However, you can override the global configuration file with your own
version.  Simply present your file (in the case below, ``munger.xml``)
via the ``--config-file`` switch::

    $ baip-munger --config-file munger.xml <infile> <outfile>

.. _configuration:

Configuration
-------------
BAIP Munger configuration is XML-based and defines one or more
document **Sections**.  Each section contains an optional
``sectionDescription`` element that details the intention behind the
section definition.  For example::

    <?xml version="1.0" encoding="UTF-8"?>
    <Doc xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <Section>
        <sectionDescription>My really cool section!!!</sectionDescription>
      </Section>
    </Doc>

.. section_removal_configuration:

Section Removal
^^^^^^^^^^^^^^^
BAIP Munger configuration provides a ``sectionRemover`` element that
defines HTML tags to remove from your document.

The simplest type of section removal is to define a HTML element tag name
to target within the ``startSection`` element.  For example::

    <?xml version="1.0" encoding="UTF-8"?>
    <Doc xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <Section>
        <sectionDescription>Remove all tables</sectionDescription>
        <startSection>table</startSection>
        <sectionRemover></sectionRemover>
      </Section>
    </Doc>

This definition will remove all ``table`` sections from your document.

.. strip_character_configuration:

Strip Character
^^^^^^^^^^^^^^^
Character removal targets specific characters within an element tag's
text.  For example::

    <?xml version="1.0" encoding="UTF-8"?>
    <Section>
        <sectionDescription>Strip characters</sectionDescription>
        <xpath>//p[@class='MsoListBullet']</xpath>
        <sectionStripChars>
            <stripChars>&#183; </stripChars>
        </sectionStripChars>
    </Section>

Here, we define a section with the HTML document within the ``xpath``
definition to target our character removal::

    <xpath>//p[@class='MsoListBullet']</xpath>

This is standard XPath.

The characters to remove are defined under the ``stripChars``.  In the
example above, there are two characters defined:

* HTML-code ``&#183;`` (or unicode number ``U+00B7`` -- the Middle Dot)
* an ordinary space

Typical of the Python :func:`string.strip` method, the characters (if
matched) will be removed from the start and/or end of the text string.

Tag Rename
^^^^^^^^^^
Target and rename an element tag.  For example::

    <?xml version="1.0" encoding="UTF-8"?>
    <Section>
        <sectionDescription>Rename tag</sectionDescription>
        <xpath>//p[@class='MsoListBullet']</xpath>
        <sectionReplaceTag>
            <newTag>li</newTag>
        </sectionReplaceTag>
    </Section>

In this case, the ``<p>`` element (targetted by the ``xpath`` definition)
will be replaced with a ``<li>`` element.

.. warning::

    Any child elements from the subsequent XPath expression will be lost.
    Only the text (or element tail) will be retained.  For example, the
    above definition will produce the following converstion:

    *Before:*

    ::

        <p class="MsoListBullet"><span>&#183;</span>The Dewrang Group .. </p>

    *After:*

    ::

        <li>&#183;The Dewrang Group .. </li>

Tag Insert
^^^^^^^^^^
Insert a new parent element.  In the following example, we will
create an unordered list::

    <Section>
        <sectionDescription>Replace tag</sectionDescription>
        <xpath>//div/li</xpath>
        <sectionInsertTag>
            <newTag>ul</newTag>
        </sectionInsertTag>
    </Section>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
