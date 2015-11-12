#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------- Modules -----------------------------------------
# import of standard modules
import sys
import os
from optparse import OptionParser
import json
from flask import Flask, jsonify

# third party modules

# local modules

__author__ = "Johnny Mariethoz <Johnny.Mariethoz@rero.ch>"
__version__ = "0.0.0"
__copyright__ = "Copyright (c) 2009-2015 Rero, Johnny Mariethoz"
__license__ = "Internal Use Only"

app = Flask(__name__)


@app.route('/')
def json_editor():
    from rerodoc.dojson.utils import get_schema
    schema = get_schema("book")
    return """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>JSON Editor to Test Submission</title>
  <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
    <script src="/static/bower_components/json-editor/dist/jsoneditor.js"></script>
  </head>

    <style type='text/css'>
    body {
        width: 960px;
        margin: auto auto;
    }
    </style>
  <body>
    <h1>Basic JSON Editor Example</h1>

    <div id='editor_holder'></div>
    <button id='submit'>Submit (console.log)</button>

    <script>
      // Initialize the editor with a JSON schema

      var editor = new JSONEditor(document.getElementById('editor_holder'),{
          ajax: true,
          theme: 'bootstrap3',
          iconlib: 'fontawesome4',
          //disable_collapse: true,
          disable_edit_json: true,
          disable_properties: true,
          schema: {
                  "title": "Choose",
                  "oneOf": [
                    {$ref: "schema/book/book"},
                    {
                        $ref: "static/simple-0.0.1.json",
                        "title": "schema/title"
                    }
                  ]
          },
          // Disable additional properties
          no_additional_properties: true,
          // Require all properties by default
          required_by_default: true
      });

      document.getElementById('submit').addEventListener('click',function() {
        // Get the value from the editor
        console.log(editor.getValue());
      });
    </script>
  </body>
</html>
"""


@app.route('/edit/<recid>')
def edit(recid):
    from rerodoc.dojson.utils import get_schema
    schema = get_schema("book")
    return """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>JSON Editor to Test Submission</title>
  <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
    <script src="/static/bower_components/json-editor/dist/jsoneditor.js"></script>
  </head>

    <style type='text/css'>
    body {
        width: 960px;
        margin: auto auto;
    }
    </style>
  <body>
    <h1>Basic JSON Editor Example</h1>

    <div id='editor_holder'></div>
    <button id='submit'>Submit (console.log)</button>

    <script>
      // Initialize the editor with a JSON schema

      var editor = new JSONEditor(document.getElementById('editor_holder'),{
          ajax: true,
          theme: 'bootstrap3',
          iconlib: 'fontawesome4',
          //disable_collapse: true,
          disable_edit_json: true,
          disable_properties: true,
          startval: %s,
          schema: {
                  "title": "Choose",
                  "oneOf": [
                    {$ref: "/schema/book/book"},
                    {
                        $ref: "/static/simple-0.0.1.json",
                        "title": "schema/title"
                    }
                  ]
          },
          // Disable additional properties
          no_additional_properties: true,
          // Require all properties by default
          required_by_default: true
      });

      document.getElementById('submit').addEventListener('click',function() {
        // Get the value from the editor
        console.log(editor.getValue());
      });
    </script>
  </body>
</html>
""" % (json.dumps(get_record(recid)))


@app.route('/schema/<base>/<name>')
def get_schema(base, name):
    from rerodoc.dojson.utils import get_schema
    schema = get_schema(name, base)
    return jsonify(schema)


def get_record(recid, verbose=False):
    """Get a record in Json format from a MarcXML."""
    import urllib2
    from dojson.contrib.marc21.utils import create_record
    from rerodoc.dojson.book import book

    remote = urllib2.urlopen("http://doc.rero.ch/record/%s/export/xm" % recid)
    blob = create_record(remote.read())
    data = book.do(blob)
    return data


@app.route('/record/<recid>')
def rerodoc2json(recid):
    return jsonify(get_record(recid))

#---------------------------- Main Part ---------------------------------------

if __name__ == '__main__':

    usage = "usage: %prog [options]"

    parser = OptionParser(usage)

    parser.set_description("Change It")

    parser.add_option("-v", "--verbose", dest="verbose", help="Verbose mode",
                      action="store_true", default=False)

    (options, args) = parser.parse_args()

    if len(args) != 0:
        parser.error("Error: incorrect number of arguments, try --help")

    app.debug = True
    app.run("0.0.0.0")
