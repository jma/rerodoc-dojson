# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import pytest


def get_demo_record(rec):
    """Get a record in Json format from a MarcXML."""

    from dojson.contrib.marc21.utils import create_record
    from rerodoc.dojson.book import book
    from rerodoc.testsuite.test_dojson import MIN_BASE_RECORD
    blob = create_record(rec)
    data = book.do(blob)
    return data


@pytest.fixture(scope='session')
def simple_book_record():
    """A sample book record."""
    return get_demo_record("""
<record>
  <controlfield tag="001">1234</controlfield>
  <datafield tag="020" ind1=" " ind2=" ">
    <subfield code="a">9782600017626</subfield>
  </datafield>
  <datafield tag="024" ind1="8" ind2=" ">
    <subfield code="a">oai:doc.rero.ch:20150908091223-PN</subfield>
  </datafield>
  <datafield tag="041" ind1=" " ind2=" ">
    <subfield code="a">eng</subfield>
  </datafield>
  <datafield tag="245" ind1=" " ind2=" ">
    <subfield code="a">Book Title</subfield>
    <subfield code="9">eng</subfield>
  </datafield>
   <datafield tag="856" ind1="4" ind2=" ">
    <subfield code="f">test_file.pdf</subfield>
    <subfield code="q">application/pdf</subfield>
    <subfield code="s">7096</subfield>
    <subfield code="u">http://doc.test.rero.ch/record/280342/files/test_file.pdf</subfield>
    <subfield code="y">order:1</subfield>
    <subfield code="z">Test intégral</subfield>
  </datafield>
  <datafield tag="919" ind1=" " ind2=" ">
    <subfield code="a">Université de Fribourg</subfield>
    <subfield code="b">Fribourg</subfield>
    <subfield code="d">doc.support@rero.ch</subfield>
  </datafield>
  <datafield tag="980" ind1=" " ind2=" ">
    <subfield code="a">BOOK</subfield>
    <subfield code="b">UNIFR</subfield>
  </datafield>
  <datafield tag="990" ind1=" " ind2=" ">
    <subfield code="a">20150908091223-PN</subfield>
  </datafield>
</record>
</collection>
""")


@pytest.fixture(scope='session')
def book_schema():
    """Session-wide book schema."""
    from rerodoc.dojson.utils import get_schema
    return get_schema("book")


@pytest.fixture(scope='session')
def book_context():
    """Session-wide book context."""
    from rerodoc.dojson.utils import get_context
    return get_context("book")
