from setuptools import setup

setup(
    name="RERO DOC",
    version="0.1.dev0",
    url="http://doc.rero.ch/",
    author="Johnny Mariethoz - RERO",
    author_email="doc.support@rero.ch",
    description="RERO DOC - Digital Library",
    install_requires=[
        "dojson==0.1.1",
        "PyLD>=0.6.8",
        "rdflib-jsonld>=0.3",
        "jsonschema>=2.5.1"
    ],
    test_suite='rerodoc.testsuite',
    entry_points={
        "invenio.config": ["rerodoc = rerodoc.config"]
    }
)
