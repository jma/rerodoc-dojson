from rdflib import Graph, RDF, Namespace
import os


CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
RDF_UDC_FILE = os.path.join(CONFIG_DIR, "udcsummary-skos.rdf")


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
        dictionary[code.title()] = {"uri": concept.title()}
        dictionary[code.title()].update(labels_in_lang)
    return dictionary
