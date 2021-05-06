from rdflib import Graph
from rdflib.namespace import Namespace, RDF, SDO
import json
import jsonschema
from rdflib.term import BNode
import requests
import time
from langdetect import detect


schema_url = "https://raw.githubusercontent.com/dasch-swiss/dasch-service-platform/main/docs/services/metadata/schema-metadata.json"
dsp = Namespace("http://ns.dasch.swiss/repository#")


def convert_file(file):
    with open(file, 'r+', encoding='utf-8') as f:
        s = f.read()
    convert_string(s)


def convert_string(data):
    g = Graph()
    g.parse(data=data, format='ttl')
    res = {"$schema": schema_url}
    res['project'] = _get_project(g)
    print(json.dumps(res, indent=2))
    # validate(res)  # TODO: bring back


def _get_project(g: Graph):
    project_iri = next(g.triples((None, RDF.type, dsp.Project)))[0]
    res = {"@id": project_iri,
           "@type": "Project",
           "@created": time.time_ns(),
           "@modified": time.time_ns(),
           "howToCite": "XXX"}

    for _, p, o in g.triples((project_iri, None, None)):
        if p == dsp.hasShortcode:
            res['shortcode'] = o
        elif p == dsp.hasName:
            res['name'] = o
        elif p == dsp.hasDescription:
            res['description'] = {"XXX": o}
        elif p == dsp.hasStartDate:
            res['startDate'] = o
        elif p == dsp.hasEndDate:
            res['endDate'] = o
        elif p == dsp.hasKeywords:
            res.setdefault('keywords', [])
            res['keywords'].append(_guess_language(o))
        elif p == dsp.hasDiscipline:
            res.setdefault('disciplines', [])
            if isinstance(o, BNode):
                res['disciplines'].append(_get_url(g, o))
            else:
                res['disciplines'].append(_guess_language(o))
        elif p == dsp.hasTemporalCoverage:
            res.setdefault('temporalCoverage', [])
            if isinstance(o, BNode):
                res['temporalCoverage'].append(_get_url(g, o))
            else:
                res['temporalCoverage'].append(_guess_language(o))
        elif p == dsp.hasSpatialCoverage:
            res.setdefault('spatialCoverage', [])
            res['spatialCoverage'].append(_get_place(g, o))
        elif p == dsp.hasURL:
            res.setdefault('urls', [])
            res['urls'].append(_get_url(g, o))
        elif p == dsp.hasDataManagementPlan:
            res['dataManagementPlan'] = o
        # elif p == dsp.datasets:  # TODO: how can I get this to work? is dataset.isPartOf
        #     res['datasets'] = []
        # elif p == dsp.hasPublication:
        #     res['publications'] = o  # TODO: implement
        # elif p == dsp.hasGrant:
        #     res['grants'] = o  # TODO: implement
        # elif p == dsp.hasAlternateName:
        #     res['alternativeNames'] = o  # TODO: implement
        # elif p == dsp.hasFunder:
        #     res['funders'] = o  # TODO: implement
        # elif p == dsp.hasContactPoint:
        #     res['contactPoint'] = o  # TODO: implement
        else:
            print("Issue: Could not handle:", p, o)

    return res


def _guess_language(text):
    lang = detect(str(text))
    if lang not in ["en", "de", "fr"]:
        lang = f"XXX - {lang}"
    return {
        lang: text
    }


def _get_place(g: Graph, iri: BNode):
    # print(list(g.triples((iri, SDO.url, None))))
    url = next(g.objects(iri, SDO.url))
    return _get_url(g, url)
    # print(place)
    pass


def _get_url(g: Graph, iri: BNode):
    propID_bnode = next(g.objects(iri, SDO.propertyID))
    propID = str(next(g.objects(propID_bnode, SDO.propertyID)))
    url = str(next(g.objects(iri, SDO.url)))
    # TODO: improve text guessing
    return {
        "text": "XXX - " + propID,
        "type": _get_url_type(propID),
        "url": url
    }


def _get_url_type(propID):
    if propID.startswith("SKOS"):
        return "Skos"
    if propID.startswith("Geonames"):
        return "Geonames"
    if propID.startswith("Pleiades"):
        return "Pleiades"
    if propID.startswith("ORCID"):
        return "ORCID"  # TODO: missing in json schema?
    if propID.startswith("Periodo"):
        return "Periodo"
    if propID.startswith("ChronOntology") or propID.startswith("dainst."):
        return "Chronontology"
    if propID.startswith("GND"):
        return "GND"
    if propID.startswith("VIAF"):
        return "VIAF"
    if propID.startswith("Creative Commons"):
        return "Creative Commons"
    else:
        return "URL"


def validate(data):
    json_data = json.dumps(data)
    r = requests.get(schema_url)
    schema = r.json()
    # with open('test/test-data/example.json', 'r+', encoding='utf-8') as f:
    #     json_data = json.loads(f.read())
    try:
        print("Validating:")
        validator = jsonschema.Draft7Validator(schema)
        for e in validator.iter_errors(data):
            print(f'Validation Error: {e.message}')
        # validation = jsonschema.validate(json_data, schema)
        # print("Valid!")
    except jsonschema.ValidationError as val:
        print(val.message)


if __name__ == "__main__":
    file = 'test/test-data/maximal.ttl'
    # file = 'test/test-data/rosetta.ttl'
    convert_file(file)
