from typing import List
from rdflib import Graph
from rdflib.namespace import Namespace, RDF, SDO, PROV
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
    res['datasets'] = _get_datasets(g)
    for ds in res.get('datasets'):
        res['project']['datasets'].append(ds.get('@id'))
    res['persons'] = _get_persons(g)

    # print(json.dumps(res['person'], indent=2))
    print(json.dumps(res, indent=4))
    validate(res)  # TODO: bring back


# Person
# ------


def _get_persons(g: Graph):
    persons = g.subjects(RDF.type, dsp.Person)
    return [_get_person(g, person) for person in persons]


def _get_person(g: Graph, person_iri):
    res = {"@id": person_iri,
           "@type": "Person",
           "@created": str(time.time_ns()),
           "@modified": str(time.time_ns()), }

    for _, p, o in g.triples((person_iri, None, None)):
        obj = str(o)
        if p == dsp.hasJobTitle:
            res.setdefault('jobTitles', [])
            res['jobTitles'].append(obj)
        elif p == dsp.hasGivenName:
            res['givenNames'] = obj.split(';')
        elif p == dsp.hasFamilyName:
            res['familyNames'] = obj.split(';')
        elif p == dsp.isMemberOf:
            res.setdefault('affiliation', [])
            res['affiliation'].append(obj)
        elif p == dsp.hasAddress:
            res['address'] = _get_address(g, o)
        elif p == dsp.hasEmail:
            res.setdefault('emails', [])
            res['emails'].append(obj)
        elif p == dsp.sameAs:
            res.setdefault('authorityRefs', [])
            res['authorityRefs'].append(_get_url(g, o))
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Person:", p, obj)

    return res


# Dataset
# -------


def _get_datasets(g: Graph):
    datasets = g.subjects(RDF.type, dsp.Dataset)
    return [_get_dataset(g, dataset) for dataset in datasets]


def _get_dataset(g: Graph, dataset_iri):
    res = {"@id": dataset_iri,
           "@type": "Dataset",
           "@created": str(time.time_ns()),
           "@modified": str(time.time_ns()), }

    for _, p, o in g.triples((dataset_iri, None, None)):
        obj = str(o)
        if p == dsp.hasTitle:
            res['title'] = obj
        elif p == dsp.hasConditionsOfAccess:
            res['accessConditions'] = obj
        elif p == dsp.hasHowToCite:
            res['howToCite'] = obj
        elif p == dsp.hasStatus:
            res['status'] = obj
        elif p == dsp.hasAbstract:
            res.setdefault("abstracts", {})
            if isinstance(obj, BNode):
                res['abstracts'].setdefault('urls', [])
                res['abstracts'].get('urls').append(_get_url(g, o))
            else:
                res['abstracts'].setdefault('texts', [])
                res['abstracts'].get('texts').append(_guess_language_of_text(obj))
        elif p == dsp.hasTypeOfData:
            res.setdefault("typeOfData", [])
            res['typeOfData'].append(obj)
        elif p == dsp.hasLicense:
            res.setdefault("licenses", [])
            res['licenses'].append(_get_url(g, o))
        elif p == dsp.hasLanguage:
            res.setdefault("languages", [])
            res['languages'].append(_get_language_from_shortcode(obj))
        elif p == dsp.hasQualifiedAttribution:
            res.setdefault("attributions", [])
            res['attributions'] = (_add_attribution(g, o, res['attributions']))
        elif p == dsp.hasAlternativeTitle:
            res.setdefault("alternativeTitles", [])
            res['alternativeTitles'].append(_guess_language_of_text(obj))
        elif p == dsp.hasDateCreated:
            res['dateCreated'] = obj
        elif p == dsp.hasDatePublished:
            res['datePublished'] = obj
        elif p == dsp.hasDateModified:
            res['dateModified'] = obj
        elif p == dsp.hasDistribution:
            res['distribution'] = _get_url(g, o)
        elif p == dsp.sameAs:
            res.setdefault('urls', [])
            res['urls'].append(_get_url(g, o))
        elif p == dsp.hasDocumentation:
            res.setdefault("documentations", {})
            if isinstance(obj, BNode):
                res['documentations'].setdefault('urls', [])
                res['documentations'].get('urls').append(_get_url(g, o))
            else:
                res['documentations'].setdefault('texts', [])
                res['documentations'].get('texts').append(_guess_language_of_text(obj))
        elif p == dsp.isPartOf:
            pass
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Dataset:", p, obj)

    return res


# Project
# -------


def _get_project(g: Graph):
    project_iri = next(g.triples((None, RDF.type, dsp.Project)))[0]
    res = {"@id": project_iri,
           "@type": "Project",
           "@created": str(time.time_ns()),
           "@modified": str(time.time_ns()),
           "howToCite": "XXX",
           "datasets": []}

    for _, p, o in g.triples((project_iri, None, None)):
        obj = str(o)
        if p == dsp.hasShortcode:
            res['shortcode'] = obj
        elif p == dsp.hasName:
            res['name'] = obj
        elif p == dsp.hasDescription:
            res['description'] = {"XXX": obj}
        elif p == dsp.hasStartDate:
            res['startDate'] = obj
        elif p == dsp.hasEndDate:
            res['endDate'] = obj
        elif p == dsp.hasKeywords:
            res.setdefault('keywords', [])
            res['keywords'].append(_guess_language_of_text(obj))
        elif p == dsp.hasDiscipline:
            res.setdefault('disciplines', [])
            if isinstance(obj, BNode):
                res['disciplines'].append(_get_url(g, o))
            else:
                res['disciplines'].append(_guess_language_of_text(obj))
        elif p == dsp.hasTemporalCoverage:
            res.setdefault('temporalCoverage', [])
            if isinstance(obj, BNode):
                res['temporalCoverage'].append(_get_url(g, o))
            else:
                res['temporalCoverage'].append(_guess_language_of_text(obj))
        elif p == dsp.hasSpatialCoverage:
            res.setdefault('spatialCoverage', [])
            res['spatialCoverage'].append(_get_place(g, o))
        elif p == dsp.hasURL:
            res.setdefault('urls', [])
            res['urls'].append(_get_url(g, o))
        elif p == dsp.hasDataManagementPlan:
            res['dataManagementPlan'] = obj
        elif p == dsp.hasPublication:
            res.setdefault('publications', [])
            res['publications'].append(obj)
        elif p == dsp.hasGrant:
            res.setdefault('grants', [])
            res['grants'].append(obj)
        elif p == dsp.hasAlternateName:
            res.setdefault('alternativeNames', [])
            res['alternativeNames'].append(_guess_language_of_text(obj))
        elif p == dsp.hasFunder:
            res.setdefault('funders', [])
            res['funders'].append(obj)
        elif p == dsp.hasContactPoint:
            res['contactPoint'] = obj
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Project:", p, obj)

    return res


# Utils
# -----


def _add_attribution(g: Graph, iri: BNode, attributions: List):
    role = str(next(g.objects(iri, dsp.hasRole)))
    agent = str(next(g.objects(iri, PROV.agent)))
    for att in attributions:
        p = att.get('person')
        r = att.get('roles')
        if r and p and p == agent:
            r.append(role)
            return attributions
    attributions.append({"person": agent,
                         "roles": [role]})
    return attributions


def _get_language_from_shortcode(code):
    code = str(code)
    langs = {'en': {'en': 'English',
                    'de': 'Englisch',
                    'fr': 'anglais'},
             'de': {'en': 'German',
                    'de': 'Deutsch',
                    'fr': 'allemand'},
             'fr': {'en': 'French',
                    'de': 'Französisch',
                    'fr': 'français'}}
    default = {code: 'XXX - ' + code}
    lang = langs.get(code)
    return lang if lang else default


def _guess_language_of_text(text):
    lang = detect(str(text))
    if lang not in ["en", "de", "fr"]:
        lang = f"XXX - {lang}"
    return {
        lang: text
    }


def _get_address(g: Graph, iri: BNode):
    locality = str(next(g.objects(iri, SDO.addressLocality)))
    code = str(next(g.objects(iri, SDO.postalCode)))
    street = str(next(g.objects(iri, SDO.streetAddress)))
    return {'street': street,
            'additional': "XXX",
            'postalCode': code,
            'locality': locality,
            'country': "XXX - Switzerland"}  # TODO: ask geonames?


def _get_place(g: Graph, iri: BNode):
    url = next(g.objects(iri, SDO.url))
    return _get_url(g, url)


def _get_url(g: Graph, iri: BNode):
    url = str(next(g.objects(iri, SDO.url)))
    try:
        propID_bnode = next(g.objects(iri, SDO.propertyID))
        propID = str(next(g.objects(propID_bnode, SDO.propertyID)))
    except StopIteration:
        propID = url
    # LATER: improve text guessing
    return {
        "text": "XXX - " + propID,  # LATER: improve display text deduction
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
        return "ORCID"  # QUESTION: missing in json schema?
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
