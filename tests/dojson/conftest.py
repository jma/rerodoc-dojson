# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import pytest
import os


def marc2record(marc):
    from rerodoc.dojson.book import book
    return book.do(marc)


def marc2marc(marc):
    from rerodoc.dojson.book import book, book2marc
    record = book.do(marc)
    return book2marc.do(record)


def record2jsonld(record, context):
    from pyld import jsonld
    import json
    import rdflib_jsonld
    from rdflib import Graph
    import copy
    rec = copy.deepcopy(record)
    rec.update(context)
    compacted = jsonld.compact(rec, context)
    return jsonld.expand(compacted)


def get_demo_record(rec):
    """Get a record in Json format from a MarcXML."""

    from dojson.contrib.marc21.utils import create_record
    from rerodoc.dojson.book import book
    blob = create_record(rec)
    data = book.do(blob)
    return data


@pytest.fixture(scope='session')
def simple_book_record():
    """A sample book record."""
    return get_demo_record(file(os.path.join(os.path.dirname(__file__),
                                             "book_record.xml")).read())


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
