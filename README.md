# RERO DOC dojson

This project will try to validate the data workflow for RERO DOC.

## Workflow

This is the actual workflow:

	1. convert the record in MarcXML into a MarcJson
	2. convert the MarcJson into our own Json definition
	3. (optionnal) validate the generated Json with the defined schema
	4. Triplets RDF generation given the json and a specific context

## Installation

	mkvirtualenv dojson
	cdvirtualenv dojson
	mkdir src; cd src
	git clone git@gitlab.rero.ch:maj/rerodoc-dojson.git
	cd rerodoc-dojson
	#will be require until the next official version
	pip install git+ssh://git@github.com/inveniosoftware/dojson.git
	pip install -e .

## Tests

You can run the tests from the root project by running:

	py.test

`tests` directory contains all the test that run the workflow.

Alternatively it is possible to run the workflow with:

	./scripts/test_jsonld.py tests/book_record.xml

 In order to validate the schema an json schema editor can be run using a local web server with:
    
    ./scripts/json_editor.py
