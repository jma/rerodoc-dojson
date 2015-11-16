from rdflib import Graph, RDF, Namespace
import os
import json
import codecs


CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
RDF_UDC_FILE = os.path.join(CONFIG_DIR, "udcsummary-skos.rdf")
RERO_UDC_FILE = os.path.join(CONFIG_DIR, "rerodoc_udc.json")
UDC_FILE = os.path.join(CONFIG_DIR, "udc.json")
UDC = json.load(file(UDC_FILE))


def extract_rdf(file_name=RDF_UDC_FILE, lang=["en", "fr", "it", "de"]):

    skos = Namespace("http://www.w3.org/2004/02/skos/core#")
    graph = Graph()
    graph.parse(file_name)
    dictionary = {}
    for concept in graph.subjects(RDF.type, skos.Concept):
        # determine the code
        code = graph.value(concept, skos.notation)
        if not code:
            continue
        # get the preferred language label, there could be more than one
        labels = list(graph.objects(concept, skos.prefLabel))
        labels_in_lang = {}
        if len(labels) > 1:
            for label in labels:
                if label.language in lang:
                    labels_in_lang[label.language] = label.title()
        else:
            label = {labels[0].language: labels[0].title()}
        dictionary[code.title()] = {"uri": concept.title().lower()}
        dictionary[code.title()].update(labels_in_lang)
    return dictionary


def update_udc():
    rero_udc = json.load(file(RERO_UDC_FILE))
    udc_from_rdf = extract_rdf()

    def get_uri(code, udc):
        res = None
        while not res:
            res = udc.get(code)
            if not res:
                code = code[:-1]
            else:
                return udc.get(code, {}).get('uri')
        return None

    for k, v in rero_udc.iteritems():
        # range
        if k.find('/') != -1:
            _from, to = k.split('/')
            for code in range(int(_from), int(to) + 1):
                uri = get_uri(str(code), udc_from_rdf)
                print code, uri
                if uri:
                    v.setdefault('uri', []).append(uri)

        # exact match or parent
        else:
            uri = get_uri(k, udc_from_rdf)
            if uri:
                v['uri'] = [uri]

    json.dump(rero_udc, codecs.open(UDC_FILE, 'w', 'utf-8'), indent=2, ensure_ascii=False)
    UDC = json.load(file(UDC_FILE))
    return True


def get_udc(code):
    return UDC.get(code)