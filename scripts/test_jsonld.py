#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------- Modules -----------------------------------------
import sys

# import of standard modules
from optparse import OptionParser

# third party modules
from pyld import jsonld
import json
import rdflib_jsonld
from rdflib import Graph

__author__ = "Johnny Mariethoz <Johnny.Mariethoz@rero.ch>"
__version__ = "0.0.0"
__copyright__ = "Copyright (c) 2012 Rero, Johnny Mariethoz"
__license__ = "Internal Use Only"


def get_demo_record(verbose=False):
    """Get a record in Json format from a MarcXML."""

    from dojson.contrib.marc21.utils import create_record
    from rerodoc.dojson.book import book
    from rerodoc.testsuite.test_dojson import MIN_BASE_RECORD
    blob = create_record(MIN_BASE_RECORD)
    data = book.do(blob)
    if verbose:
        print(json.dumps(blob, indent=2))
        print(json.dumps(data, indent=2))
    return data


def validate(record, schema_name="book"):
    """Record validation with a given schema."""

    from jsonschema import validate
    from rerodoc.dojson.utils import get_schema
    schema = get_schema(schema_name)
    validate(record, schema)

#---------------------------- Main Part ---------------------------------------

if __name__ == '__main__':

    usage = "usage: %prog [options]"

    parser = OptionParser(usage)

    parser.set_description("Get a demo record and extract RDF triples")

    parser.add_option("-v", "--verbose", dest="verbose", help="Verbose mode",
                      action="store_true", default=False)

    parser.add_option("-f", "--format", dest="format", help="Output format",
                      type="string", default="turtle")

    (options, args) = parser.parse_args()

    if len(args) != 0:
        parser.error("Error: incorrect number of arguments, try --help")

    doc = get_demo_record(options.verbose)
    validate(doc)
    if options.verbose:
        from rerodoc.dojson.book import book2marc
        print(json.dumps(book2marc.do(doc), indent=2))

    from rerodoc.dojson.utils import get_context
    context = get_context("book")
    doc.update(context)

    if options.verbose:
        print("Input record in json format:")
        print(json.dumps(doc, indent=2))

    compacted = jsonld.compact(doc, context)
    #expanded = jsonld.expand(compacted)
    #flattened = jsonld.flatten(doc)
    #framed = jsonld.frame(doc, context)
    #normalized = jsonld.normalize(doc, {'format': 'application/nquads'})

    graph = Graph().parse(data=json.dumps(compacted, indent=2), format="json-ld")
    print(graph.serialize(format=options.format))
