.. BAIP Munger documentation master file

BAIP - Munger
=============

.. toctree::
    :maxdepth: 2

    contents.rst

The BAIP Munger is a fit-for-purpose HTML transposer tool.

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
