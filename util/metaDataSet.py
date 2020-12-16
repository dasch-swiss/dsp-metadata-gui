from abc import ABC, abstractmethod
from urllib.parse import urlparse
import re
import pyshacl
import validators
from rdflib import Graph, URIRef, RDF, Literal, Namespace, BNode
from rdflib.namespace import SDO, XSD
from rdflib.collection import Collection

from util import utils
from util.utils import Cardinality, Datatype, Validity

"""
The Classes defined here aim to represent a metadata-set, closely following the metadata ontology.
"""

##### TODO-List #####
#
# - don't add person/org/etc. to graph, unless they're referenced somewhere
#
#####################

ontology_url = "https://raw.githubusercontent.com/dasch-swiss/dsp-ontologies/main/dsp-repository/v1/dsp-repository.shacl.ttl"

dsp_repo = Namespace("http://ns.dasch.swiss/repository#")
prov = Namespace("http://www.w3.org/ns/prov#")


class MetaDataSet:
    """ Representation of a data set.

    This class represents a data set of project metadata.

    It holds the following properties:
    - index: the index of the dataset in the UI (list item).
      Note: in some case, we'll need to make sure this stays correct
    - name: the repo/project name.
      Typically the name of the folder that was selected.
    - path: the full path of the folder that was selected.
    - files: a list of relevant files in the folder
    - project: a `metaDataSet.Project` representation of the actual metadata (as specified by the ontology).
    - dataset: a list of `metaDataSet.Dataset`
    - persons: a list of `metaDataSet.Person`
    - organizations: a list of `metaDataSet.Organization`

    At a later stage, this class should be able to return a representation of its data in form of an RDF graph.
    """

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, i: int):
        self.__index = i

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path: str):
        self.__path = path

    @property
    def files(self):
        return self.__files

    @files.setter
    def files(self, files: list):
        self.__files = files

    def __init__(self, index: int, name: str, path: str, shortcode: str):
        self.index = index
        self.name = name
        self.path = path
        self.files = []
        self.project = Project(name, shortcode, self)
        self.dataset = [Dataset(name, self.project, self)]
        self.persons = [Person(self)]  # FIXME: persons get wiped on every load
        self.organizations = [Organization(self)]
        self.grants = [Grant(self)]
        self.update_iris()

    def update_iris(self):
        """
        Updates the IRIs of all DataClass fields.

        This method should be called whenever something is added/removed
        to the lists holding DataClass instances (persons, etc.).
        """
        # TODO: this method needs to be called whenever a person/org/dataset is added/removed
        # TODO: ensure updating the IRIs doesn't mess up identifying objects by string
        self.project.iri_suffix = "-project"
        for i, ds in enumerate(self.dataset):
            ds.iri_suffix = f"-dataset-{str(i + 1).zfill(3)}"
        for i, person in enumerate(self.persons):
            person.iri_suffix = f"-person-{str(i + 1).zfill(3)}"
        for i, org in enumerate(self.organizations):
            org.iri_suffix = f"-organization-{str(i + 1).zfill(3)}"
        for i, g in enumerate(self.grants):
            g.iri_suffix = f"-grant-{str(i + 1).zfill(3)}"

    def __str__(self):
        return str({
            "index": self.index,
            "name": self.name,
            "path": self.path,
            "files": self.files,
            "metadata": [
                self.project,
                self.dataset,
                self.persons,
                self.organizations,
                self.grants,
            ]
        })

    def get_all_properties(self) -> list:
        """
        Returns a list of all properties held by fields of this class. (person, dataset, etc.)
        """
        res = self.project.get_properties()
        for p in self.dataset:
            res.extend(p.get_properties())
        for p in self.persons:
            res.extend(p.get_properties())
        for o in self.organizations:
            res.extend(o.get_properties())
        for o in self.grants:
            res.extend(o.get_properties())
        return res

    def validate_graph(self, graph):
        """
        Validates the graph of the entire data against the SHACL ontology.
        """
        # graph = self.generate_rdf_graph()
        conforms, results_graph, results_text = pyshacl.validate(graph, shacl_graph=ontology_url)
        print(f"Validation result: {conforms}")
        # print('\n------------\n')
        # print(results_graph)
        # print('\n------------\n')
        # print(results_text)
        return conforms

    def generate_rdf_graph(self) -> Graph:
        """
        Generates the RFD graph of the entire dataset.

        Returns:
            Graph: The RDF graph
        """
        graph = Graph(base=dsp_repo)
        graph.bind("dsp-repo", dsp_repo)
        graph.bind("schema", SDO)
        graph.bind("xsd", XSD)
        graph.bind("prov", prov)
        self.project.add_rdf_to_graph(graph, "Project")
        for i, person in enumerate(self.dataset):
            person.add_rdf_to_graph(graph, "Dataset")
        for i, person in enumerate(self.persons):
            person.add_rdf_to_graph(graph, "Person")
        for i, org in enumerate(self.organizations):
            org.add_rdf_to_graph(graph, "Organization")
        for i, org in enumerate(self.grants):
            org.add_rdf_to_graph(graph, "Grant")
        # print("\n------------------\n")
        # print(graph.serialize(format='nt').decode("utf-8"))
        # print("\n------------------\n")
        # print(graph.serialize(format='turtle').decode("utf-8"))
        # print("\n------------------\n")
        # print(graph.serialize(format='xml').decode("utf-8"))
        # print("\n------------------\n")
        # print(graph.serialize(format='json-ld').decode("utf-8"))
        # print("\n------------------\n")
        return graph

    def get_by_string(self, s: str):
        if not s or s.isspace():
            return
        if str(self.project) == s:
            return self.project
        id_str = s.split(':')[0]
        for o in self.dataset:
            if str(o).startswith(id_str):
                return o
        for o in self.persons:
            if str(o).startswith(id_str):
                return o
        for o in self.organizations:
            if str(o).startswith(id_str):
                return o
        for o in self.grants:
            if str(o).startswith(id_str):
                return o

    def add_dataset(self):
        new = Dataset(self.name, self.project, self)
        self.dataset.append(new)
        self.update_iris()

    def add_person(self):
        new = Person(self)
        self.persons.append(new)
        self.update_iris()

    def add_organization(self):
        new = Organization(self)
        self.organizations.append(new)
        self.update_iris()

    def add_grant(self):
        new = Grant(self)
        self.grants.append(new)
        self.update_iris()

    def remove(self, obj):
        if obj in self.dataset:
            self.dataset.remove(obj)
        if obj in self.persons:
            self.persons.remove(obj)
        if obj in self.organizations:
            self.organizations.remove(obj)
        if obj in self.grants:
            self.grants.remove(obj)

    def get_status(self):
        if self.validate_graph(self.generate_rdf_graph()):
            overall = 'Valid'
        else:
            overall = 'Invalid'
        invalid = 0
        missing = 0
        optional = 0
        valid = 0
        for p in self.get_all_properties():
            v, _ = p.validate()
            if v == Validity.INVALID_VALUE:
                invalid += 1
            elif v == Validity.REQUIRED_VALUE_MISSING:
                missing += 1
            elif v == Validity.OPTIONAL_VALUE_MISSING:
                optional += 1
            elif v == Validity.VALID:
                valid += 1
        return f"{overall}  --  {invalid + missing} Problems; {valid} Values"


class DataClass(ABC):
    """
    Abstract parent class of all classes holding data.
    """

    def get_metadataset(self) -> MetaDataSet:
        """
        Returns the `MetaDataSet` to which this class belongs

        Returns:
            MetaDataSet: The owner MetaDataSet
        """
        return self.meta

    def add_rdf_to_graph(self, graph: Graph, typename: str):
        """
        Adds the RDF representation of this class to a graph

        Args:
            graph (Graph): the `rdflib.Graph` to which the triples should be added
            typename (str): the type name of this class
        """
        iri = self.get_rdf_iri()
        type = dsp_repo[typename]
        # TODO: should be done in Project class
        graph.add((iri, RDF.type, type))
        for prop in self.get_properties():
            graph += prop.get_triples(iri)

    # TODO: ensure that this gets updated whenever the shortcode changes
    def get_rdf_iri(self) -> URIRef:
        """
        Return the iri of the object.

        This can be called to use the object as subject of an RDF triple.

        Returns:
            URIRef: the IRI
        """
        shortcode = self.get_metadataset().project.shortcode.value
        if not shortcode:
            shortcode = "xxxx"
        classname = shortcode + self.iri_suffix
        return URIRef(dsp_repo[classname])

    @abstractmethod
    def get_properties(self) -> list:
        """
        Return a list of all `Property` fields of this class
        """
        raise NotImplementedError

    def get_prop_by_name(self, name):
        for p in self.get_properties():
            if p.name == name:
                return p


class Project(DataClass):
    """
    Project shape.

    Corresponds to `dsp-repo:Project` in our ontology.

    Args:
        name (str): The name of the project
        meta (MetaDataSet): the owning `MetaDataSet`
    """

    def __init__(self, name: str, shortcode: str, meta: MetaDataSet):
        self.meta = meta
        self.name = Property("Name",
                             "The name of the Project",
                             "Test Project",
                             Datatype.STRING,
                             Cardinality.ONE,
                             name,
                             predicate=dsp_repo.hasName)

        self.description = Property("Description",
                                    "Description of the Project",
                                    "This is a test project. All properties have been used to test these. You will just describe your project briefly.",
                                    Datatype.STRING,
                                    Cardinality.ONE,
                                    predicate=dsp_repo.hasDescription,
                                    multiline=True)

        self.keywords = Property("Keywords",
                                 "Keywords and tags",
                                 "mathematics, science, history of science, history of mathematics. Use the plus sign to have a new field for each key word.",
                                 Datatype.STRING,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasKeywords)

        self.discipline = Property("Discipline",
                                   """Discipline and research fields from UNESCO nomenclature: https://skos.um.es/unesco6/?l=en \
                                   or from http://www.snf.ch/SiteCollectionDocuments/allg_disziplinenliste.pdf""",
                                   "http://skos.um.es/unesco6/11",
                                   Datatype.STRING_OR_URL,
                                   Cardinality.ONE_TO_UNBOUND,
                                   predicate=dsp_repo.hasDiscipline)

        self.startDate = Property("Start Date",
                                  "The date when the project started, e. g. when funding was granted.",
                                  "2000-07-26T21:32:52",
                                  Datatype.DATE,
                                  Cardinality.ONE,
                                  predicate=dsp_repo.hasStartDate)

        self.endDate = Property("End Date",
                                "The date when the project was finished, e. g. when the last changes to the project data where completed.",
                                "2000-07-26T21:32:52",
                                Datatype.DATE,
                                Cardinality.ONE,
                                predicate=dsp_repo.hasEndDate)

        self.temporalCoverage = Property("Temporal coverage",
                                         "Temporal coverage of the project from http://perio.do/en/ or https://chronontology.dainst.org/",
                                         "http://chronontology.dainst.org/period/Ef9SyESSafJ1",
                                         Datatype.STRING_OR_URL,
                                         Cardinality.ONE_TO_UNBOUND,
                                         predicate=dsp_repo.hasTemporalCoverage)

        self.spatialCoverage = Property("Spatial coverage",
                                        "Spatial coverage of the project from Geonames URL: https://www.geonames.org/ or from Pleiades URL: https://pleiades.stoa.org/places",
                                        "https://www.geonames.org/6255148/europe.html",
                                        Datatype.PLACE,
                                        Cardinality.ONE_TO_UNBOUND,
                                        predicate=dsp_repo.hasSpatialCoverage)

        self.funder = Property("Funder",
                               "Funding person or institution of the project",
                               "",
                               Datatype.PERSON_OR_ORGANIZATION,
                               Cardinality.ONE_TO_UNBOUND,
                               predicate=dsp_repo.hasFunder)

        self.grant = Property("Grant",
                              "Grant of the project",
                              "",
                              Datatype.GRANT,
                              predicate=dsp_repo.hasGrant)

        self.url = Property("URL",
                            "Landing page or Website of the project. We recommend DSP Landing Page. Optionally, a second URL can be added too.",
                            "https://test.dasch.swiss/",
                            Datatype.URL,
                            Cardinality.ONE_TO_TWO,
                            predicate=dsp_repo.hasURL)

        self.shortcode = Property("Shortcode",
                                  "Internal shortcode of the project",
                                  "0000",
                                  Datatype.SHORTCODE,
                                  Cardinality.ONE,
                                  value=shortcode,
                                  predicate=dsp_repo.hasShortcode)

        self.alternateName = Property("Alternate Name",
                                      "Alternative name of the project, e.g. in case of an overly long official name",
                                      "Another Title",
                                      Datatype.STRING,
                                      predicate=dsp_repo.hasAlternateName)

        self.dataManagementPlan = Property("Data Management Plan",
                                           "Data Management Plan of the project",
                                           "",
                                           Datatype.DATA_MANAGEMENT_PLAN,
                                           Cardinality.ZERO_OR_ONE,
                                           predicate=dsp_repo.hasDataManagementPlan)

        self.publication = Property("Publications",
                                    "Publications produced during the lifetime of the project",
                                    "Doe, J. (2000). A Publication.",
                                    Datatype.STRING,
                                    predicate=dsp_repo.hasPublication,
                                    multiline=True)

        self.contactPoint = Property("Contact Point",
                                     "Contact information",
                                     "",
                                     Datatype.PERSON_OR_ORGANIZATION,
                                     Cardinality.ZERO_OR_ONE,
                                     predicate=dsp_repo.hasContactPoint)

    def get_properties(self):
        return [
            self.name,
            self.shortcode,
            self.url,
            self.description,
            self.keywords,
            self.discipline,
            self.startDate,
            self.endDate,
            self.temporalCoverage,
            self.spatialCoverage,
            self.funder,
            self.grant,
            self.alternateName,
            self.dataManagementPlan,
            self.publication,
            self.contactPoint
        ]

    def __str__(self):
        return str(self.get_rdf_iri())


class Dataset(DataClass):
    """
    Dataset Shape.

    Corresponds to `dsp-repo:Dataset` in the ontology.
    """

    def __init__(self, name, project, meta):
        self.meta = meta
        self.title = Property("Title",
                              "Title of the dataset",
                              "Dataset-Title",
                              Datatype.STRING,
                              Cardinality.ONE,
                              value=f"Dataset of {name}",
                              predicate=dsp_repo.hasTitle)

        self.alternativeTitle = Property("Alternative title",
                                         "Alternative title of the dataset",
                                         "Another Dataset-Title",
                                         Datatype.STRING,
                                         Cardinality.ZERO_OR_ONE,
                                         predicate=dsp_repo.hasAlternativeTitle)

        self.abstract = Property("Abstract",
                                 "Description of the dataset",
                                 "This is merely an exemplary dataset",
                                 Datatype.STRING_OR_URL,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasAbstract,
                                 multiline=True)

        self.sameAs = Property("Alternative URL",
                               "Alternative URL to the dataset, if applicable",
                               "https://test.dasch.swiss/",
                               Datatype.URL,
                               Cardinality.UNBOUND,
                               predicate=dsp_repo.sameAs)

        self.typeOfData = Property("Type of data",
                                   "Type of data related to the dataset",
                                   "xml",
                                   Datatype.CONTROLLED_VOCABULARY,
                                   Cardinality.ONE_TO_UNBOUND,
                                   value_options=["XML", "Text",
                                                  "Image", "Movie", "Audio"],
                                   predicate=dsp_repo.hasTypeOfData)

        self.documentation = Property("Documentation",
                                      "Additional documentation",
                                      '"http://www.example.org/documentation.md" or "Work in Progress"',
                                      Datatype.STRING_OR_URL,
                                      Cardinality.UNBOUND,
                                      predicate=dsp_repo.hasDocumentation)

        self.license = Property("License",
                                "The license terms of the dataset",
                                "https://creativecommons.org/licenses/by/3.0",
                                Datatype.URL,
                                Cardinality.ONE_TO_UNBOUND,
                                predicate=dsp_repo.hasLicense)

        self.accessConditions = Property("Conditions of Access",
                                         "Access conditions of the data",
                                         "Open Access",
                                         Datatype.STRING,
                                         Cardinality.ONE,
                                         predicate=dsp_repo.hasConditionsOfAccess)

        self.howToCite = Property("How to cite",
                                  "How to cite the data",
                                  "Test-project (test), 2002, https://test.dasch.swiss",
                                  Datatype.STRING,
                                  Cardinality.ONE,
                                  predicate=dsp_repo.hasHowToCite)

        self.status = Property("Dataset status",
                               "Current status of a dataset",
                               "The dataset is work in progress",
                               Datatype.CONTROLLED_VOCABULARY,
                               Cardinality.ONE,
                               value_options=['In planning', 'Ongoing', 'On hold', 'Finished'],
                               predicate=dsp_repo.hasStatus)

        self.datePublished = Property("Date published",
                                      "Date of publication",
                                      "2000-08-01",
                                      Datatype.DATE,
                                      Cardinality.ZERO_OR_ONE,
                                      predicate=dsp_repo.hasDatePublished)

        self.language = Property("Language",
                                 "Language(s) of the dataset",
                                 "English",
                                 Datatype.STRING,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasLanguage)

        self.project = Property("is Part of",
                                "The project to which the data set belongs",
                                "",
                                Datatype.PROJECT,
                                Cardinality.ONE,
                                value=project,
                                predicate=dsp_repo.isPartOf)

        self.attribution = Property("Qualified Attribution",
                                    "Persons/Organization involved in the creation of the dataset",
                                    '<person> + "editor"',
                                    Datatype.ATTRIBUTION,
                                    Cardinality.ONE_TO_UNBOUND,
                                    predicate=dsp_repo.hasQualifiedAttribution)

        self.dateCreated = Property("Date created",
                                    "Creation of the dataset",
                                    "2000-08-01",
                                    Datatype.DATE,
                                    Cardinality.ZERO_OR_ONE,
                                    predicate=dsp_repo.hasDateCreated)

        self.dateModified = Property("Date modified",
                                     "Last modification of the dataset",
                                     "2000-08-01",
                                     Datatype.DATE,
                                     Cardinality.ZERO_OR_ONE,
                                     predicate=dsp_repo.hasDateModified)

        self.distribution = Property("Distribution",
                                     "A downloadable form of this dataset, at a specific location, in a specific format",
                                     "https://test.dasch.swiss",
                                     Datatype.DOWNLOAD,
                                     Cardinality.ZERO_OR_ONE,
                                     predicate=dsp_repo.hasDistribution)

    def get_properties(self):
        return [
            self.project,
            self.title,
            self.abstract,
            self.language,
            self.typeOfData,
            self.attribution,
            self.license,
            self.howToCite,
            self.accessConditions,
            self.status,
            self.sameAs,
            self.alternativeTitle,
            self.documentation,
            self.datePublished,
            self.dateCreated,
            self.dateModified,
            self.distribution,
        ]

    def __str__(self):
        classname = str(self.get_rdf_iri()).split('#')[1]
        n1 = "<title missing>"
        if self.title.value:
            n1 = self.title.value
        return f"{classname}: {n1}"


class Person(DataClass):
    """
    Person Shape.

    Corresponds to `dsp-repo:Person` in the ontology.
    """

    def __init__(self, meta):
        self.meta = meta
        self.sameAs = Property("Alternative URL",
                               "Alternative URL, pointing to an authority file (ORCID, VIAF, GND, ...)",
                               "https://orcid.org/000-000-000-000",
                               Datatype.URL,
                               Cardinality.UNBOUND,
                               predicate=dsp_repo.sameAs)

        self.givenName = Property("Given name",
                                  "Given name of the person",
                                  "John",
                                  Datatype.STRING,
                                  Cardinality.ONE_TO_UNBOUND_ORDERED,
                                  predicate=dsp_repo.hasGivenName)

        self.familyName = Property("Family name",
                                   "Family name of the person",
                                   "Doe",
                                   Datatype.STRING,
                                   Cardinality.ONE,
                                   predicate=dsp_repo.hasFamilyName)

        self.email = Property("E-mail",
                              "E-mail address of the person",
                              "john.doe@dasch.swiss",
                              Datatype.EMAIL,
                              Cardinality.ZERO_TO_TWO,
                              predicate=dsp_repo.hasEmail)

        self.address = Property("Address",
                                "Postal address of the person",
                                "",
                                Datatype.ADDRESS,
                                Cardinality.UNBOUND,
                                predicate=dsp_repo.hasAddress)

        self.memberOf = Property("Member of",
                                 "Affiliation of the person",
                                 "",
                                 Datatype.ORGANIZATION,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.isMemberOf)

        self.jobTitle = Property("Job title",
                                 "Position/Job title of the person",
                                 "Dr.",
                                 Datatype.STRING,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasJobTitle)

    def get_properties(self):
        return [
            self.familyName,
            self.givenName,
            self.memberOf,
            self.jobTitle,
            self.email,
            self.sameAs,
            self.address,
        ]

    def __str__(self):
        classname = str(self.get_rdf_iri()).split('#')[1]
        n1 = "<first name missing>"
        if self.givenName.value:
            n1 = " ".join(self.givenName.value)
        n2 = "<family name missing>"
        if self.familyName.value:
            n2 = self.familyName.value
        return f"{classname}: {n1} {n2}"


class Organization(DataClass):
    """
    Organization Shape.

    Corresponds to `dsp-repo:Organization` in the ontology.
    """

    def __init__(self, meta):
        self.meta = meta

        self.name = Property("Legal Name",
                             "Legal name of the organization",
                             "DaSCH",
                             Datatype.STRING,
                             Cardinality.ONE_TO_UNBOUND,
                             predicate=dsp_repo.hasName)

        self.email = Property("E-mail",
                              "E-mail address of the organization",
                              "info@dasch.swiss",
                              Datatype.EMAIL,
                              Cardinality.ZERO_OR_ONE,
                              predicate=dsp_repo.hasEmail)

        self.address = Property("Address",
                                "Postal address of the organization",
                                "",
                                Datatype.ADDRESS,
                                Cardinality.UNBOUND,
                                predicate=dsp_repo.hasAddress)

        self.url = Property("URL",
                            "URL of the organization",
                            "https://dasch.swiss",
                            Datatype.URL,
                            Cardinality.ZERO_OR_ONE,
                            predicate=dsp_repo.hasURL)

    def get_properties(self):
        return [
            self.name,
            self.email,
            self.url,
            self.address,
        ]

    def __str__(self):
        classname = str(self.get_rdf_iri()).split('#')[1]
        n1 = "<name missing>"
        if self.name.value:
            n1 = " / ".join(self.name.value)
        return f"{classname}: {n1}"


class Grant(DataClass):
    """
    Grant Shape.

    Corresponds to `dsp-repo:Grant` in the ontology.
    """

    def __init__(self, meta):
        self.meta = meta

        self.name = Property("Name",
                             "Name of the grant",
                             "Ambizione",
                             Datatype.STRING,
                             Cardinality.ZERO_OR_ONE,
                             predicate=dsp_repo.hasName)

        self.url = Property("URL",
                            "URL of the grant",
                            "https://www.snf.ch/grants/001",
                            Datatype.URL,
                            Cardinality.ZERO_OR_ONE,
                            predicate=dsp_repo.hasURL)

        self.number = Property("Number",
                               "The number of the grant.",
                               "00012345",
                               Datatype.STRING,
                               Cardinality.ZERO_OR_ONE,
                               predicate=dsp_repo.hasNumber)

        self.funder = Property("Funder",
                               "Funding person or institution of the project",
                               "",
                               Datatype.PERSON_OR_ORGANIZATION,
                               Cardinality.ZERO_OR_ONE,  # QUESTION: does that make sense?
                               predicate=dsp_repo.hasFunder)

    def get_properties(self):
        return [
            self.funder,
            self.name,
            self.number,
            self.url,
        ]

    def __str__(self):
        classname = str(self.get_rdf_iri()).split('#')[1]
        n1 = "<funder missing>"
        if self.funder.value:
            n1 = str(self.funder.value)
        return f"{classname}: {n1}"


class Property():
    """
    General representation of a property.

    Corresponds to `sh:property`
    """

    def __init__(self, name: str, description: str, example: str, datatype: Datatype.STRING,
                 cardinality=Cardinality.UNBOUND, value=None, value_options=None,
                 predicate=dsp_repo.whatever, multiline=False):
        self.name = name
        self.description = description
        self.example = example
        self.datatype = datatype
        self.cardinality = cardinality
        self.value = value
        self.value_options = value_options
        self.predicate = predicate
        self.multiline = multiline

    def get_url_property_id(url: str) -> str:
        """
        This method tries to guess the propetyID for a URL.

        For certain pre-defined cases, a reasonable propertyID is chosen;
        otherwise, the net location is being extracted, if possible.

        Args:
            url (str): a URL

        Returns:
            str: a propertyID
        """
        if re.search('skos\\.um\\.es', url):
            return "SKOS UNESCO Nomenclature"
        # TODO: more
        loc = urlparse(url).netloc
        if len(loc.split('.')) > 2:
            return '.'.join(loc.split('.')[1:])
        if loc:
            return loc
        return url[:12]

    def get_triples(self, subject: URIRef) -> Graph:
        """
        Returns a Graph containing the triples that represent this property, in respect to a given subject.

        Args:
            subject (URIRef): the subject to which the property is object

        Returns:
            Graph: a graph containing one or multiple triples that represent the property
        """
        g = Graph()  # TODO: ensure that names come in the right order
        # Ensure the data can be looped
        vals = self.value
        if not isinstance(vals, list):
            vals = [vals]
        if self.datatype == Datatype.STRING and \
                self.cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED:
            listnode = BNode()
            Collection(g, listnode, [Literal(v, datatype=XSD.string) for v in vals if v and not v.isspace()])
            g.add((subject, self.predicate, listnode))
            return g
        for v in vals:
            if not v:
                continue
            if isinstance(v, str) and v.isspace():
                continue
            # resolve datatype ambiguity
            datatype = self.datatype
            if datatype == Datatype.STRING_OR_URL:
                if v and validators.url(str(v)):
                    datatype = Datatype.URL
                elif v and v.startswith('www.'):
                    v = "http://" + v
                    datatype = Datatype.URL
                else:
                    datatype = Datatype.STRING
            if datatype == Datatype.PERSON_OR_ORGANIZATION:
                if isinstance(v, Person):
                    datatype = Datatype.PERSON
                else:
                    datatype = Datatype.ORGANIZATION
            # Handle datatypes
            if datatype == Datatype.STRING \
                    or datatype == Datatype.CONTROLLED_VOCABULARY \
                    or datatype == Datatype.SHORTCODE:
                g.add((subject, self.predicate, Literal(v, datatype=XSD.string)))
            elif datatype == Datatype.DATE:
                g.add((subject, self.predicate, Literal(v, datatype=XSD.date)))
            elif datatype == Datatype.URL:
                blank = BNode()
                g.add((subject, self.predicate, blank))
                g.add((blank, RDF.type, SDO.URL))
                b2 = BNode()
                g.add((blank, SDO.propertyID, b2))
                g.add((b2, RDF.type, SDO.PropertyValue))
                g.add((b2, SDO.propertyID, Literal(Property.get_url_property_id(v))))
                g.add((blank, SDO.url, Literal(v)))
            elif datatype == Datatype.PLACE:
                b0 = BNode()
                g.add((subject, self.predicate, b0))
                g.add((b0, RDF.type, SDO.Place))
                b1 = BNode()
                g.add((b0, SDO.url, b1))
                g.add((b1, RDF.type, SDO.URL))
                b2 = BNode()
                g.add((b1, SDO.propertyID, b2))
                g.add((b2, RDF.type, SDO.PropertyValue))
                g.add((b2, SDO.propertyID, Literal("Geonames")))
                g.add((b2, SDO.url, Literal(v)))
            elif datatype == Datatype.PERSON:
                g.add((subject, self.predicate, v.get_rdf_iri()))
            elif datatype == Datatype.ORGANIZATION:
                g.add((subject, self.predicate, v.get_rdf_iri()))
            elif datatype == Datatype.PROJECT:
                g.add((subject, self.predicate, v.get_rdf_iri()))
            elif datatype == Datatype.DATA_MANAGEMENT_PLAN:
                if v[0] or v[1]:
                    dmp = URIRef('DMP')
                    g.add((subject, self.predicate, dmp))
                    g.add((dmp, RDF.type, dsp_repo.DataManagementPlan))
                    if v[0]:
                        g.add((dmp, dsp_repo.isAvailable, Literal(
                            v[0], datatype=XSD.boolean)))
                    if v[1]:
                        b1 = BNode()
                        g.add((dmp, dsp_repo.hasURL, b1))
                        g.add((b1, RDF.type, SDO.URL))
                        g.add((b1, SDO.url, Literal(v[1])))
            elif datatype == Datatype.ADDRESS:
                if not v[0] and not v[1] and not v[2]:
                    return g
                b0 = BNode()
                g.add((subject, self.predicate, b0))
                g.add((b0, RDF.type, SDO.PostalAddress))
                g.add((b0, SDO.streetAddress, Literal(
                    v[0], datatype=XSD.string)))
                g.add((b0, SDO.postalCode, Literal(v[1], datatype=XSD.string)))
                g.add((b0, SDO.addressLocality, Literal(
                    v[2], datatype=XSD.string)))
            elif datatype == Datatype.GRANT:
                g.add((subject, self.predicate, v.get_rdf_iri()))
            elif datatype == Datatype.ATTRIBUTION:
                b0 = BNode()
                g.add((subject, self.predicate, b0))
                g.add((b0, RDF.type, prov.Attribution))
                g.add((b0, dsp_repo.hasRole, Literal(v[0], datatype=XSD.string)))
                g.add((b0, prov.agent, v[1].get_rdf_iri()))
            elif datatype == Datatype.DOWNLOAD:
                b0 = BNode()
                g.add((subject, self.predicate, b0))
                g.add((b0, RDF.type, SDO.DataDownload))
                g.add((b0, SDO.url, Literal(v)))
            elif datatype == Datatype.EMAIL:
                if isinstance(v, tuple):
                    if v and v[0]:
                        g.add((subject, self.predicate, Literal(v[0])))
                    if v and v[1]:
                        g.add((subject, self.predicate, Literal(v[1])))
                else:
                    if v and not v.isspace():
                        g.add((subject, self.predicate, Literal(v)))
            else:
                print(f"{datatype}: {v}\n-> don't know how to serialize this.\n")
        return g

    def validate(self) -> (Validity, str):
        datatype = self.datatype
        cardinality = self.cardinality
        value = self.value

        missing = "Required value is missing."
        valid = "The current value is valid."
        optional = "This field is optional"
        no_url = "Invalid URL"
        no_mail = "Invalid e-mail address"

        if not value:
            if Cardinality.isMandatory(cardinality):
                return Validity.REQUIRED_VALUE_MISSING, missing
            else:
                return Validity.OPTIONAL_VALUE_MISSING, valid

        if datatype == Datatype.STRING or \
                datatype == Datatype.STRING_OR_URL or \
                datatype == Datatype.DOWNLOAD:
            if cardinality == Cardinality.ONE:
                if value and not value.isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            elif cardinality == Cardinality.ONE_TO_TWO:
                if value[0] and not value[0].isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            elif cardinality == Cardinality.ZERO_OR_ONE:
                if value and not value.isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif cardinality == Cardinality.ONE_TO_UNBOUND or \
                    cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED:
                if len(value) > 0 and value[0] and not value[0].isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            elif cardinality == Cardinality.UNBOUND:
                if len(value) > 0 and value[0] and not value[0].isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional

        elif datatype == Datatype.SHORTCODE:
            if re.match('[a-zA-Z0-9]{4}$', value):
                return Validity.VALID, valid
            else:
                return Validity.INVALID_VALUE, "Shortcode must be exactly 4 alphanumeric characters."

        elif datatype == Datatype.URL or \
                datatype == Datatype.PLACE:
            if cardinality == Cardinality.UNBOUND:
                if len(value) > 0 and value[0] and not value[0].isspace():
                    if utils.areURLs(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_url
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif cardinality == Cardinality.ZERO_OR_ONE:
                if value and not value.isspace():
                    if utils.isURL(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_url
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif cardinality == Cardinality.ONE_TO_TWO or \
                    cardinality == Cardinality.ONE_TO_UNBOUND:
                if value[0] and not value[0].isspace():
                    if utils.areURLs(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_url
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing

        elif datatype == Datatype.EMAIL:
            if cardinality == Cardinality.ZERO_OR_ONE:
                if value and not value.isspace():
                    if utils.is_email(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_mail
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif cardinality == Cardinality.ZERO_TO_TWO:
                if value[0] and not value[0].isspace():
                    if utils.are_emails(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_mail
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional

        elif datatype == Datatype.GRANT or \
                datatype == Datatype.PROJECT or \
                datatype == Datatype.PERSON or \
                datatype == Datatype.ORGANIZATION or \
                datatype == Datatype.PERSON_OR_ORGANIZATION:
            if cardinality == Cardinality.UNBOUND:
                if len(value) > 0 and value[0]:
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                if len(value) > 0 and value[0]:
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            if cardinality == Cardinality.ONE:
                if value:
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            if cardinality == Cardinality.ZERO_OR_ONE:
                if value:
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional

        elif datatype == Datatype.DATE:
            if not value or value.isspace():
                if cardinality == Cardinality.ONE:
                    return Validity.REQUIRED_VALUE_MISSING, missing
                elif cardinality == Cardinality.ZERO_OR_ONE:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif value and re.match(r'\d{4}-\d{2}-\d{2}$', value):
                return Validity.VALID, valid
            else:
                return Validity.INVALID_VALUE, "Not a valid date."

        elif datatype == Datatype.ADDRESS:
            if cardinality == Cardinality.UNBOUND:
                if value[0] and not value[0].isspace() and \
                        value[1] and not value[1].isspace() and \
                        value[2] and not value[2].isspace():
                    return Validity.VALID, valid
                elif (not value[0] or value[0].isspace()) and \
                        (not value[1] or value[1].isspace()) and \
                        (not value[2] or value[2].isspace()):
                    return Validity.OPTIONAL_VALUE_MISSING, optional
                else:
                    return Validity.INVALID_VALUE, "Not a valid address."

        elif datatype == Datatype.CONTROLLED_VOCABULARY:
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                for v in value:
                    if v not in self.value_options:
                        return Validity.INVALID_VALUE, f"Value '{v}' not allowed."
                return Validity.VALID, valid
            elif cardinality == Cardinality.ONE:
                if value not in self.value_options:
                    return Validity.INVALID_VALUE, f"Value '{value}' not allowed."
                return Validity.VALID, valid

        elif datatype == Datatype.ATTRIBUTION:
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                for v in value:
                    if (not v[0] or v[0].isspace()) or \
                            (not v[1] or not isinstance(v[1], (Person, Organization))):
                        return Validity.INVALID_VALUE, "Not a valid address."
                return Validity.VALID, valid

        elif datatype == Datatype.DATA_MANAGEMENT_PLAN:
            if cardinality == Cardinality.ZERO_OR_ONE:
                if value[0] or (value[1] and not value[1].isspace()):
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional

        print(f'behavior undefined:\ncard: {cardinality}\ntype: {datatype}\n')
        return "", ""

    def __str__(self):
        if self.value:
            return str(self.value)
        return f"<Property '{self.name}' undefined>"
