import os
import json
import functools


def concatenate(data, subfields):
    to_concatenate = []
    for sf in subfields:
        if data.get(sf):
            to_concatenate.append(data.get(sf))
    if to_concatenate:
        return ' '.join(to_concatenate)
    return None


def get_schema(name, version="0.0.1"):
    schema_file_name = os.path.join(os.path.dirname(__file__), name,
                                    "schemas", name + "-" + version + ".json")
    if not os.path.isfile(schema_file_name):
        return None
    return json.load(file(schema_file_name))


def get_context(name, version="0.0.1"):
    context_file_name = os.path.join(os.path.dirname(__file__), name,
                                     "context", name + "-" + version + ".json")
    if not os.path.isfile(context_file_name):
        return None
    return json.load(file(context_file_name))
