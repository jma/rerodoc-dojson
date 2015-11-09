import os
import json
import functools
import six


def legacy_export_as_marc(json, tabsize=4):
    """Create the MARCXML representation using the producer rules."""

    def encode_for_marcxml(value):
        from xml.sax.saxutils import escape
        if isinstance(value, unicode):
            value = value.encode('utf8')
        return escape(str(value))

    export = ['<record>\n']

    for key, value in sorted(six.iteritems(json)):
        if not value:
            continue
        if key.startswith('00') and len(key) == 3:
            # Controlfield
            if isinstance(value, list):
                value = value[0]
            export += ['\t<controlfield tag="%s">%s'
                       '</controlfield>\n'.expandtabs(tabsize)
                       % (key, encode_for_marcxml(value))]
        else:
            tag = key[:3]
            try:
                ind1 = key[3].replace("_", "")
            except:
                ind1 = ""
            try:
                ind2 = key[4].replace("_", "")
            except:
                ind2 = ""
            if isinstance(value, dict):
                value = [value]
            for field in value:
                export += ['\t<datafield tag="%s" ind1="%s" '
                           'ind2="%s">\n'.expandtabs(tabsize)
                           % (tag, ind1, ind2)]
                for code, subfieldvalue in six.iteritems(field):
                    if subfieldvalue:
                        if isinstance(subfieldvalue, list):
                            for val in subfieldvalue:
                                export += ['\t\t<subfield code="%s">%s'
                                           '</subfield>\n'.expandtabs(tabsize)
                                           % (code, encode_for_marcxml(val))]
                        else:
                            export += ['\t\t<subfield code="%s">%s'
                                       '</subfield>\n'.expandtabs(tabsize)
                                       % (code,
                                          encode_for_marcxml(subfieldvalue))]
                export += ['\t</datafield>\n'.expandtabs(tabsize)]
    export += ['</record>\n']
    return "".join(export)


def concatenate(data, subfields, sep=" "):
    to_concatenate = []
    for sf in subfields:
        if data.get(sf):
            to_concatenate.append(data.get(sf))
    if to_concatenate:
        return sep.join(to_concatenate)
    return None


def get_schema(name, base='common', version="0.0.1"):
    schema_file_name = os.path.join(os.path.dirname(__file__), base,
                                    "schemas", name + "-" + version + ".json")
    if not os.path.isfile(schema_file_name):
        return None

    def expand_schema(schema):
        if isinstance(schema, list):
            for s in schema:
                expand_schema(s)
        if isinstance(schema, dict):
            if schema.get('$ref'):
                name = schema.get('$ref')
                base, name = name.split('/')[2:]
                sub_schema = get_schema(name, base)
                schema.update(sub_schema)
                del(schema['$ref'])
            for k, v in schema.iteritems():
                expand_schema(v)

    schema = json.load(file(schema_file_name))
    expand_schema(schema)
    return schema


def get_context(name, version="0.0.1"):
    context_file_name = os.path.join(os.path.dirname(__file__), name,
                                     "context", name + "-" + version + ".json")
    if not os.path.isfile(context_file_name):
        return None
    return json.load(file(context_file_name))
