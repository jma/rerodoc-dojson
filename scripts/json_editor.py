#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO: add a navigation sidebar (http://www.codingeverything.com/2014/02/BootstrapDocsSideBar.html)
"""

#---------------------------- Modules -----------------------------------------
# import of standard modules
import sys
import os
from optparse import OptionParser
import json
from flask import Flask, jsonify
from flask_jsonrpc import JSONRPC

# third party modules

# local modules

__author__ = "Johnny Mariethoz <Johnny.Mariethoz@rero.ch>"
__version__ = "0.0.0"
__copyright__ = "Copyright (c) 2009-2015 Rero, Johnny Mariethoz"
__license__ = "Internal Use Only"

jsonrpc = JSONRPC(service_url="/rpc")

@jsonrpc.method('api.get_udc')
def get_udc(lang):
    from rerodoc.udc.udc import get_long_names
    return get_long_names(lang).values()


app = Flask(__name__)



@app.route('/angular/<doc_type>/edit/<recid>')
def edit_angular(doc_type, recid):
    from rerodoc.dojson.utils import get_schema, get_form
    schema = get_schema(doc_type, doc_type)
    form = get_form(doc_type, doc_type)
    import json
    return """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>JSON Editor to Test Submission</title>
      <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
      <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

    <script type="text/javascript" src="/static/bower_components/angular/angular.min.js"></script>
    <script type="text/javascript" src="/static/bower_components/angular-sanitize/angular-sanitize.min.js"></script>
    <script type="text/javascript" src="/static/bower_components/tv4/tv4.js"></script>
    <script type="text/javascript" src="/static/bower_components/objectpath/lib/ObjectPath.js"></script>
    <script type="text/javascript" src="/static/bower_components/angular-schema-form/dist/schema-form.min.js"></script>
  </head>

    <style type='text/css'>
    body {
        max-width: 960px;
        padding: 100px;
        margin: auto auto;
    }
    </style>
  <body ng-app="test">
    <h1>Angular JSON Editor Example</h1>

<div ng-controller="MyFormController">
    <form sf-schema="schema" sf-form="form" sf-model="model"></form>
</div>

<script>
    app=angular.module('test', ['schemaForm'])
        .controller('MyFormController', function($scope) {
          $scope.schema =%s;
          $scope.form = %s;
          $scope.model = %s;
          $scope.autocomplete = function (modelValue, form) {
          alert(modelValue, form);
              var to_return = [
                "test1",
                "test2
              ];
              return to_return;
          };
    });
</script>
    <script type="text/javascript" src="/static/bower_components/angular-schema-form/dist/bootstrap-decorator.min.js"></script>

  </body>
</html>
    """ % (json.dumps(schema, indent=2), json.dumps(form, indent=2), json.dumps(get_record(recid)))


@app.route('/angular/<doc_type>')
def angular(doc_type):
    from rerodoc.dojson.utils import get_schema, get_form
    schema = get_schema(doc_type, doc_type)
    form = get_form(doc_type, doc_type)
    import json
    return """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>JSON Editor to Test Submission</title>
      <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
  <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

    <script type="text/javascript" src="/static/bower_components/angular/angular.min.js"></script>
    <script type="text/javascript" src="/static/bower_components/angular-sanitize/angular-sanitize.min.js"></script>
    <script type="text/javascript" src="/static/bower_components/tv4/tv4.js"></script>
    <script type="text/javascript" src="/static/bower_components/objectpath/lib/ObjectPath.js"></script>
    <script type="text/javascript" src="/static/bower_components/angular-schema-form/dist/schema-form.min.js"></script>
    <script type="text/javascript" src="/static/bower_components/angular-schema-form/dist/bootstrap-decorator.min.js"></script>
    <script type="text/javascript" src="/static/bower_components/angular-bootstrap/ui-bootstrap-tpls.js"></script>
    <script type="text/javascript" src="/static/bower_components/angular-uuid/uuid.min.js"></script>
    <script type="text/javascript" src="/static/bower_components/angular-jsonrpc/jsonrpc.js"></script>
    <script type="text/javascript" src="/static/js/app.js"></script>
    <script type="text/javascript" src="/static/js/services/data.js"></script>
    <script type="text/javascript" src="/static/js/directives/typeahead.js"></script>
    <script type="text/javascript" src="/static/js/controllers/autocomplete.js"></script>


  </head>

    <style type='text/css'>
    body {
        max-width: 960px;
        padding: 100px;
        margin: auto auto;
    }
    .autocomplete .dropdown-menu {
        max-height: 200px;
        overflow-y: scroll;
    }
    </style>
  <body ng-app="test">
    <h1>Angular JSON Editor Example</h1>

<div ng-controller="MyFormController">
    <form sf-schema="schema" sf-form="form" sf-model="model"></form>
</div>


<script>
        app.controller('MyFormController', function($scope) {
            $scope.schema =%s;
            $scope.form = %s;           
            $scope.model = {};

        });

</script>

  </body>
</html>
    """ % (json.dumps(schema, indent=2), json.dumps(form, indent=2))


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
                    {$ref: "schema/audio/audio"}
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
                    //{$ref: "/schema/book/book"},
                    {$ref: "/schema/audio/audio"}
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
    from rerodoc.dojson.processors import convert_marcxml
    from rerodoc.dojson.book import book

    remote = urllib2.urlopen("http://doc.rero.ch/record/%s/export/xm" % recid)

    data = convert_marcxml(remote)
    return data.next()
    #blob = create_record(remote.read())
    #data = book.do(blob)
    #return data


@app.route('/record/<recid>')
def rerodoc2json(recid):
    return jsonify(get_record(recid))


jsonrpc.init_app(app)

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
