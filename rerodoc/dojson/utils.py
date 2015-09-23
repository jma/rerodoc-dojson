import os
import json


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
