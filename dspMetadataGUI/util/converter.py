"""
Module to convert RDF serialized metadata (first datamodel) into JSON metadata (new datamodel).
"""

import re
from typing import Any, Dict, List
from rdflib import Graph
from rdflib.namespace import Namespace, RDF, SDO, PROV
import json
import jsonschema
from rdflib.term import BNode
import requests
import time
from textblob import TextBlob
from bs4 import BeautifulSoup


schema_url = "https://raw.githubusercontent.com/dasch-swiss/dasch-service-platform/main/docs/services/metadata/schema-metadata.json"
dsp = Namespace("http://ns.dasch.swiss/repository#")


def convert_file(file: str) -> str:
    """Convert metadata from a file.

    Convert metadata from a local .ttl file.

    Args:
        file (str): path to a .ttl file (can be relative or absolute)

    Returns:
        str: json serialized metadata
    """
    with open(file, 'r+', encoding='utf-8') as f:
        s = f.read()
    return convert_string(s)


def convert_string(data: str) -> str:
    """Convert metadata from a string.

    Args:
        data (str): string of a turtle setrialization of metadata

    Returns:
        str: json serialized metadata.
    """
    g = Graph()
    g.parse(data=data, format='ttl')
    res = {"$schema": schema_url}
    res['project'] = _get_project(g)
    res['datasets'] = _get_datasets(g)
    for ds in res.get('datasets'):  # type: ignore
        res['project']['datasets'].append(ds.get('@id'))  # type: ignore
    persons = _get_persons(g)
    if persons:
        res['persons'] = persons
    orgs = _get_organizations(g)
    if orgs:
        res['organizations'] = orgs
    grants = _get_grants(g)
    if grants:
        res['grants'] = grants
    dmp = _get_dmp(g)
    if dmp:
        res['dataManagementPlan'] = dmp

    validate(res)
    return json.dumps(res, indent=4)


# DMP
# ---


def _get_dmp(g: Graph):
    """Get data management plan from graph"""
    try:
        dmp = next(g.subjects(RDF.type, dsp.DataManagementPlan))
    except StopIteration:
        return {}

    res = {"@id": dmp,
           "@type": "DataManagementPlan",
           "@created": str(time.time_ns()),
           "@modified": str(time.time_ns()), }

    for _, p, o in g.triples((dmp, None, None)):
        obj = str(o)
        if p == dsp.hasURL:
            res['url'] = _get_url(g, o)
        elif p == dsp.isAvailable:
            res['available'] = obj == "true"
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Grant:", p, obj)

    return res


# Grant
# -----

def _get_grants(g: Graph):
    """Get grants from graph"""
    grants = g.subjects(RDF.type, dsp.Grant)
    return [_get_grant(g, grant) for grant in grants]


def _get_grant(g: Graph, grant_iri) -> Dict[str, Any]:
    """Get grant from graph"""
    res = {"@id": grant_iri,
           "@type": "Grant",
           "@created": str(time.time_ns()),
           "@modified": str(time.time_ns()), }

    for _, p, o in g.triples((grant_iri, None, None)):
        obj = str(o)
        if p == dsp.hasFunder:
            res.setdefault('funders', [])
            res['funders'].append(obj)
        elif p == dsp.hasNumber:
            res['number'] = obj
        elif p == dsp.hasName:
            res['name'] = obj
        elif p == dsp.hasURL:
            res['url'] = _get_url(g, o)
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Grant:", p, obj)

    return res


# Organizations
# -------------

def _get_organizations(g: Graph):
    """Get organizations from graph"""
    orgs = g.subjects(RDF.type, dsp.Organization)
    return [_get_organization(g, org) for org in orgs]


def _get_organization(g: Graph, org_iri):
    """Get organization from graph"""
    res = {"@id": org_iri,
           "@type": "Organization",
           "@created": str(time.time_ns()),
           "@modified": str(time.time_ns()), }

    for _, p, o in g.triples((org_iri, None, None)):
        obj = str(o)
        if p == dsp.hasName:
            res['name'] = obj
        elif p == dsp.hasURL:
            res['url'] = _get_url(g, o)
        elif p == dsp.hasEmail:
            res['email'] = obj
        elif p == dsp.hasAddress:
            res['address'] = _get_address(g, o)
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Organization:", p, obj)

    return res


# Person
# ------

def _get_persons(g: Graph):
    """Get persons from graph"""
    persons = g.subjects(RDF.type, dsp.Person)
    return [_get_person(g, person) for person in persons]


def _get_person(g: Graph, person_iri):
    """Get person from graph"""
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
    """Get datasets from graph"""
    datasets = g.subjects(RDF.type, dsp.Dataset)
    return [_get_dataset(g, dataset) for dataset in datasets]


def _get_dataset(g: Graph, dataset_iri):
    """Get dataset from graph"""
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
            if isinstance(o, BNode):
                res['abstracts'].setdefault('urls', [])
                res['abstracts'].get('urls').append(_get_url(g, o))
            else:
                res['abstracts'].setdefault('texts', [])
                res['abstracts'].get('texts').append(_guess_language_of_text(obj))
        elif p == dsp.hasTypeOfData:
            res.setdefault("typeOfData", [])
            if obj == "Movie":
                obj = "Video"
            res['typeOfData'].append(obj)
        elif p == dsp.hasLicense:
            res.setdefault("licenses", [])
            res['licenses'].append(_get_url(g, o))
        elif p == dsp.hasLanguage:
            res.setdefault("languages", [])
            res['languages'].append(_get_language(obj))
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
            if isinstance(o, BNode):
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
    """Get project from graph"""
    project_iri = next(g.triples((None, RDF.type, dsp.Project)))[0]
    res = {"@id": project_iri,
           "@type": "Project",
           "@created": str(time.time_ns()),
           "@modified": str(time.time_ns()),
           "howToCite": "XX - new property on project level",
           "datasets": []}

    for _, p, o in g.triples((project_iri, None, None)):
        obj = str(o)
        if p == dsp.hasShortcode:
            res['shortcode'] = obj
        elif p == dsp.hasName:
            res['name'] = obj
        elif p == dsp.hasDescription:
            res['description'] = _guess_language_of_text(obj)
        elif p == dsp.hasStartDate:
            res['startDate'] = obj
        elif p == dsp.hasEndDate:
            res['endDate'] = obj
        elif p == dsp.hasKeywords:
            res.setdefault('keywords', [])
            res['keywords'].append(_guess_language_of_text(obj))
        elif p == dsp.hasDiscipline:
            res.setdefault('disciplines', [])
            if isinstance(o, BNode):
                res['disciplines'].append(_get_url(g, o))
            else:
                res['disciplines'].append(_guess_language_of_text(obj))
        elif p == dsp.hasTemporalCoverage:
            res.setdefault('temporalCoverage', [])
            if isinstance(o, BNode):
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
    """From a graph g, add an attribution defined by a blank node (i.e. all tripples that have the iri as subject), to a list."""
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


def _get_language(language):
    """Get the correct language representation according to a string describing a language (i.e. the language itself or a language shortcode)"""
    language = str(language)
    if re.match('^[a-z]{2}$', language):
        return _get_language_from_shortcode(language)
    else:
        return _guess_language_of_text(language)


def _get_language_from_shortcode(code):
    """Get language representation from a language shortcode"""
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
    default = {code: 'XX - ' + code}
    lang = langs.get(code)
    return lang if lang else default


def _guess_language_of_text(text):
    """ Guess the language of a string.

    Returns a dict of type multilanguage text, if possible with the correct language attribution to the text.
    """
    text = str(text)
    try:
        lang = TextBlob(text).detect_language()
    except Exception:
        print(f"Could not resolve language for {text}")
        lang = "XX"
    if lang not in ["en", "de", "fr"]:
        print(f"Unexpected language: {lang}  (Text: {text})")
        lang = f"XX - {lang}"
    return {
        lang: text
    }


def _get_address(g: Graph, iri: BNode):
    """Get address from graph"""
    locality = str(next(g.objects(iri, SDO.addressLocality)))
    code = str(next(g.objects(iri, SDO.postalCode)))
    street = str(next(g.objects(iri, SDO.streetAddress)))
    country = _get_country(locality)
    return {'street': street,
            'additional': "XX - new Property",
            'postalCode': code,
            'locality': locality,
            'country': country}


def _get_country(locality):
    """Get country of an address

    Checks if the place is in Switzerland.
    """
    q = f"http://api.geonames.org/searchJSON?username=blandolt&name_equals={locality}&country=ch"
    r = requests.get(q)
    js = r.json()
    gn = js.get('geonames')
    return "Switzerland" if len(gn) > 0 else "XX - Switzerland?"


def _get_place(g: Graph, iri: BNode):
    """Get a place from graph"""
    url = next(g.objects(iri, SDO.url))
    return _get_url(g, url)


def _get_url(g: Graph, iri: BNode):
    """Get URL from graph"""
    url = str(next(g.objects(iri, SDO.url)))
    try:
        propID_bnode = next(g.objects(iri, SDO.propertyID))
        propID = str(next(g.objects(propID_bnode, SDO.propertyID)))
    except StopIteration:
        propID = url
    type_ = _get_url_type(propID)
    txt = _get_url_text(url, type_)
    return {
        "text": txt,
        "type": type_,
        "url": url
    }


def _get_url_text(url, t):
    """Get a reasonable display text for a URL of a defined type."""
    if t == 'URL':
        return url
    if t == 'Skos':
        return f"XX: Skos URL: {url}"  # XXX
    if t == 'Geonames':
        return _get_geonames_name(url)
    if t == 'Pleiades':
        return f"XX: Pleiades URL: {url}"  # XXX
    if t == 'ORCID':
        return f"XX: ORCID URL: {url}"
    if t == 'Periodo':
        return f"XX: Periodo URL: {url}"  #  XXX
    if t == 'GND':
        return f"XX: GND URL: {url}"
    if t == 'VIAF':
        return f"XX: VIAF URL: {url}"
    if t == 'Creative Commons':
        return _get_cc_name(url)
    if t == 'Chronontology':
        return f"XX: Chronontology URL: {url}"  # XXX
    f"XX: Unknown Type for URL: {url}"


def _get_cc_name(url: str):
    """Get display text for a Creative Commons URL"""
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        ident = soup.select_one('span.cc-license-identifier')
        res: str = ident.get_text()
        res = res.strip().removeprefix('(').removesuffix(')')
        return res
    except Exception:
        return f'XX: CC URL: {url}'


def _get_geonames_name(url: str):
    """Get display text for a geonames URL"""
    if url.endswith(".html"):
        url = url.rsplit("/", 1)[0]
    gn_id = url.rsplit("/")[-1]
    base = f'http://api.geonames.org/getJSON'
    payload = {'geonameId': gn_id,
               'username': 'blandolt'}
    r = requests.get(base, params=payload)
    resp = r.json()
    name = resp.get('toponymName')
    return name


def _get_url_type(propID):
    """Get URL type from schema.propertyID"""
    if propID.startswith("SKOS"):
        return "Skos"
    if propID.startswith("Geonames"):
        return "Geonames"
    if propID.startswith("Pleiades"):
        return "Pleiades"
    if propID.startswith("ORCID"):
        return "ORCID"
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
    """Validates JSON

    Validates json serialized data against the schema of the API specification.  

    [Schema](https://raw.githubusercontent.com/dasch-swiss/dasch-service-platform/main/docs/services/metadata/schema-metadata.json)

    Args:
        data ([type]): [description]
    """
    r = requests.get(schema_url)
    schema = r.json()
    try:
        print("Validating...")
        validator = jsonschema.Draft7Validator(schema)
        valid = True
        for e in validator.iter_errors(data):
            print(f'Validation Error: {e.message}')
            valid = False
        if valid:
            print("JSON is valid.")
    except jsonschema.ValidationError as val:
        print(val.message)


if __name__ == "__main__":
    # file = 'test/test-data/maximal.ttl'
    file = 'test/test-data/rosetta.ttl'
    s = convert_file(file)
    print(s)
