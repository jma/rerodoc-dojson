#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Johnny Mariethoz <Johnny.Mariethoz@rero.ch>"
__version__ = "0.0.0"
__copyright__ = "Copyright (c) 2012 Rero, Johnny Mariethoz"
__license__ = "Internal Use Only"


#---------------------------- Modules -----------------------------------------
import sys

# import of standard modules
from optparse import OptionParser

# third party modules
from pyld import jsonld
import json
import rdflib_jsonld
from rdflib import Graph


# local modules

def get_demo_record():
    from dojson.contrib.marc21.utils import create_record
    from rerodoc.dojson.book import book
    from rerodoc.testsuite.test_dojson import MIN_BASE_RECORD
    blob = create_record(MIN_BASE_RECORD)
    return book.do(blob)

#---------------------------- Main Part ---------------------------------------

if __name__ == '__main__':

    usage = "usage: %prog [options]"

    parser = OptionParser(usage)

    parser.set_description ("Get a demo record and extract RDF triples")

    parser.add_option ("-v", "--verbose", dest="verbose",
                       help="Verbose mode",
                       action="store_true", default=False)

    parser.add_option ("-f", "--format", dest="format",
                       help="Output format",
                       type="string", default="turtle")

    (options, args) = parser.parse_args ()

    if len(args) != 0:
        parser.error("Error: incorrect number of arguments, try --help")

    from rerodoc.dojson.utils import get_context
    context = get_context("book")
    doc = get_demo_record()
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
