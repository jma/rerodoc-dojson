# RERO DOC dojson

Un premier essai concernant le workflow des données RERO DOC en json.

## Installation

	mkvirtualenv dojson
	cdvirtualenv dojson
	mkdir src
	git clone git@gitlab.rero.ch:maj/rerodoc-dojson.git
	cd rerodoc-dojson
	pip install -e .

## Tester

Il est possible d'exécuter les tests unitaires avec:

	python rerodoc/testsuite/test_dojson.py

ou de tester avec un script convertissant du MarcXML en triplets:
	
	python ./scripts/test_jsonld.py	

## Workflow

L'idée principale est la suivante:

	1. convertir le MarcXML en MarcJson
	2. convertir le MarcJson en Json comme définit dans notre overlay
	3. (optionnel) validation du Json généré avec jsonschema
	4. Génération des triplets RDF avec json-ld et le contexte définit dans notre overlay

