# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import pytest


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
    return get_demo_record("""
<record>
  <controlfield tag="001">235790</controlfield>
  <controlfield tag="005">20150331105725.0</controlfield>
  <datafield tag="020" ind1=" " ind2=" ">
    <subfield code="a">9782881980343</subfield>
  </datafield>
  <datafield tag="024" ind1="8" ind2=" ">
    <subfield code="a">oai:doc.rero.ch:20150327115158-PX</subfield>
    <subfield code="p">book</subfield>
  </datafield>
  <datafield tag="024" ind1="8" ind2=" ">
    <subfield code="p">IRDP</subfield>
  </datafield>
  <datafield tag="024" ind1="8" ind2=" ">
    <subfield code="p">cdu37</subfield>
  </datafield>
  <datafield tag="035" ind1=" " ind2=" ">
    <subfield code="a">R007896380</subfield>
  </datafield>
  <datafield tag="041" ind1=" " ind2=" ">
    <subfield code="a">fre</subfield>
  </datafield>
  <datafield tag="080" ind1=" " ind2=" ">
    <subfield code="a">37</subfield>
  </datafield>
  <datafield tag="100" ind1=" " ind2=" ">
    <subfield code="a">Nidegger, Christian (éd.)</subfield>
  </datafield>
  <datafield tag="245" ind1=" " ind2=" ">
    <subfield code="a">PISA 2012</subfield>
    <subfield code="9">fre</subfield>
    <subfield code="b">compétences des jeunes Romands : résultats de la cinquième enquête PISA auprès des élèves de fin de scolarité obligatoire</subfield>
  </datafield>
  <datafield tag="260" ind1=" " ind2=" ">
    <subfield code="a">Neuchâtel</subfield>
    <subfield code="c">2014</subfield>
    <subfield code="b">IRDP, Institut de recherche et de documentation pédagogique</subfield>
  </datafield>
  <datafield tag="300" ind1=" " ind2=" ">
    <subfield code="a">190 p.</subfield>
    <subfield code="c">24 cm</subfield>
    <subfield code="b">ill.</subfield>
  </datafield>
  <datafield tag="520" ind1=" " ind2=" ">
    <subfield code="a">Quelles sont les compétences des jeunes en mathématiques, lecture et sciences ? Quels sont les facteurs qui favorisent leur développement ou qui, au contraire, peuvent faire obstacle ? Quelle est l’évolution des résultats au cours du temps ? L’enquête internationale PISA, menée tous les trois ans depuis 2000 dans plus de soixante pays, cherche à apporter des réponses à ces interrogations. Près de 7000 élèves romands en fin de scolarité obligatoire ont participé en 2012 à cette enquête centrée, pour la deuxième fois, sur les mathématiques, tout en abordant aussi la lecture et les sciences. Cet ouvrage fournit un ensemble de résultats et les met en rapport avec l’environnement social, culturel et scolaire des élèves. On montre par exemple que les variables sociodémographiques ont un impact global marqué sur les compétences des élèves tout en révélant des spécificités locales et cantonales. Différents aspects des compétences des élèves en termes de contenus et de processus mathématiques sont également analysés. D’autres éléments tels que la motivation, l’intérêt pour les mathématiques ou l’anxiété vis-à-vis de cette discipline, ont aussi un effet déterminant sur les performances des élèves. Comment les prendre en compte à l’école pour faire progresser tous les élèves et leur permettre de mener à bien leur scolarité et leur future vie professionnelle ? Ce rapport s’adresse aux différents partenaires de l’école : responsables politiques et scolaires, enseignants, formateurs. Il vise une meilleure compréhension de l’école et de son fonctionnement. Par la mise en perspective des résultats des cantons romands avec ceux obtenus au niveau national et international, il apporte un éclairage spécifique aux débats actuels sur les acquis et les compétences des élèves de Suisse romande.</subfield>
    <subfield code="9">fre</subfield>
  </datafield>
  <datafield tag="600" ind1=" " ind2=" ">
    <subfield code="9">61027</subfield>
    <subfield code="a">PISA (Programme international pour le suivi des acquis des élèves)</subfield>
    <subfield code="2">rero</subfield>
  </datafield>
  <datafield tag="600" ind1=" " ind2=" ">
    <subfield code="9">650_7</subfield>
    <subfield code="a">Évaluation en éducation</subfield>
    <subfield code="2">rero</subfield>
  </datafield>
  <datafield tag="600" ind1=" " ind2=" ">
    <subfield code="9">650_7</subfield>
    <subfield code="a">Lecture</subfield>
    <subfield code="2">rero</subfield>
  </datafield>
  <datafield tag="600" ind1=" " ind2=" ">
    <subfield code="9">650_7</subfield>
    <subfield code="a">Sciences</subfield>
    <subfield code="2">rero</subfield>
  </datafield>
  <datafield tag="600" ind1=" " ind2=" ">
    <subfield code="9">650_7</subfield>
    <subfield code="a">Mathématiques</subfield>
    <subfield code="2">rero</subfield>
  </datafield>
  <datafield tag="600" ind1=" " ind2=" ">
    <subfield code="9">650_7</subfield>
    <subfield code="a">Scolarité obligatoire</subfield>
    <subfield code="2">rero</subfield>
  </datafield>
  <datafield tag="600" ind1=" " ind2=" ">
    <subfield code="9">650_7</subfield>
    <subfield code="a">2012</subfield>
    <subfield code="2">rero</subfield>
  </datafield>
  <datafield tag="600" ind1=" " ind2=" ">
    <subfield code="9">651_7</subfield>
    <subfield code="a">Suisse romande</subfield>
    <subfield code="2">rero</subfield>
  </datafield>
  <datafield tag="695" ind1=" " ind2=" ">
    <subfield code="a">Enquête ; Evaluation internationale ; Analyse comparative ; Compétence ; Performance ; Niveau de connaissances ; Elève ; Secondaire premier cycle ; Fin de scolarité ; Suisse ; Berne ; Fribourg ; Genève ; Jura ; Neuchâtel ; Valais ; Vaud ; Suisse romande ; Sciences ; Mathématique ; Lecture ; Influence ; Milieu familial ; Milieu social ; Milieu scolaire</subfield>
    <subfield code="9">fre</subfield>
  </datafield>
  <datafield tag="856" ind1="4" ind2=" ">
    <subfield code="f">pisa2012_rapport_romand.pdf</subfield>
    <subfield code="q">application/pdf</subfield>
    <subfield code="s">2197614</subfield>
    <subfield code="u">http://doc.rero.ch/record/235790/files/pisa2012_rapport_romand.pdf</subfield>
    <subfield code="y">order:1</subfield>
    <subfield code="z">Texte intégral</subfield>
  </datafield>
  <datafield tag="919" ind1=" " ind2=" ">
    <subfield code="a">Institut de recherche et de documentation pédagogique (IRDP)</subfield>
    <subfield code="b">Neuchâtel</subfield>
    <subfield code="d">doc.support@rero.ch</subfield>
  </datafield>
  <datafield tag="980" ind1=" " ind2=" ">
    <subfield code="a">BOOK</subfield>
    <subfield code="b">IRDP</subfield>
  </datafield>
  <datafield tag="990" ind1=" " ind2=" ">
    <subfield code="a">20150327115158-PX</subfield>
  </datafield>
</record>""")

# """
# <record>
#   <controlfield tag="001">1234</controlfield>
#   <datafield tag="020" ind1=" " ind2=" ">
#     <subfield code="a">9782600017626</subfield>
#   </datafield>
#   <datafield tag="024" ind1="8" ind2=" ">
#     <subfield code="a">oai:doc.rero.ch:20150908091223-PN</subfield>
#   </datafield>
#     <datafield tag="035" ind1=" " ind2=" ">
#     <subfield code="a">R</subfield>
#   </datafield>
#   <datafield tag="041" ind1=" " ind2=" ">
#     <subfield code="a">eng</subfield>
#   </datafield>
#   <datafield tag="245" ind1=" " ind2=" ">
#     <subfield code="a">Book Title</subfield>
#     <subfield code="9">eng</subfield>
#   </datafield>
#    <datafield tag="856" ind1="4" ind2=" ">
#     <subfield code="f">test_file.pdf</subfield>
#     <subfield code="q">application/pdf</subfield>
#     <subfield code="s">7096</subfield>
#     <subfield code="u">http://doc.test.rero.ch/record/280342/files/test_file.pdf</subfield>
#     <subfield code="y">order:1</subfield>
#     <subfield code="z">Test intégral</subfield>
#   </datafield>
#   <datafield tag="919" ind1=" " ind2=" ">
#     <subfield code="a">Université de Fribourg</subfield>
#     <subfield code="b">Fribourg</subfield>
#     <subfield code="d">doc.support@rero.ch</subfield>
#   </datafield>
#   <datafield tag="980" ind1=" " ind2=" ">
#     <subfield code="a">BOOK</subfield>
#     <subfield code="b">UNIFR</subfield>
#   </datafield>
#   <datafield tag="990" ind1=" " ind2=" ">
#     <subfield code="a">20150908091223-PN</subfield>
#   </datafield>
# </record>
# </collection>
# """)


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
