#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------- Modules -----------------------------------------
# import of standard modules
import sys
import os
from optparse import OptionParser
import json

# third party modules

# local modules

__author__ = "Johnny Mariethoz <Johnny.Mariethoz@rero.ch>"
__version__ = "0.0.0"
__copyright__ = "Copyright (c) 2009-2015 Rero, Johnny Mariethoz"
__license__ = "Internal Use Only"

from flask import Flask
app = Flask(__name__)

@app.route('/')
def json_editor():
    from rerodoc.dojson.utils import get_schema
    schema = get_schema("book")
    print schema
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
                    %s,
                    {
                        $ref: "static/simple-0.0.1.json",
                        title: "Title Only"
                    }
                  ]
          },
          // Disable additional properties
          no_additional_properties: true,
          // Require all properties by default
          required_by_default: true
      });
    </script>
  </body>
</html>
""" % json.dumps(schema, indent=2)


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

    app.run()
