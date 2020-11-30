from enum import Enum
from abc import ABC, abstractmethod
from urllib.parse import urlparse
import re
import pyshacl
import validators
from rdflib import Graph, URIRef, RDF, Literal, Namespace, BNode
from rdflib.namespace import SDO, XSD

"""
The Classes defined here aim to represent a metadata-set, closely following the metadata ontology.
"""

##### TODO-List #####
#
# - implement on the fly input validation
# - implement overall data validation
# - don't add person/org/etc. to graph, unless they're referenced somewhere
#
#####################

ontology_url = "https://raw.githubusercontent.com/dasch-swiss/dsp-ontologies/main/dsp-repository/v1/dsp-repository.shacl.ttl"

dsp_repo = Namespace("http://ns.dasch.swiss/repository#")


class Cardinality(Enum):
    """
    A set of cardinalities that may be used for properties.
    """
    UNBOUND = 0
    ONE = 1
    ZERO_OR_ONE = 2
    ONE_TO_UNBOUND = 3
    ONE_TO_TWO = 4
    ZERO_TO_TWO = 5

    def get_optionality_string(card) -> str:
        """
        Returns wether or not a cardinality is optional.

        Args:
            card (Cardinality): the cardinality in question

        Returns:
            str: "Mandatory" or "Optional", depending on the cardinality
        """
        if card == Cardinality.ONE \
                or card == Cardinality.ONE_TO_TWO \
                or card == Cardinality.ONE_TO_UNBOUND:
            return "Mandatory"
        if card == Cardinality.UNBOUND \
                or card == Cardinality.ZERO_OR_ONE \
                or card == Cardinality.ZERO_TO_TWO:
            return "Optional"


class Datatype(Enum):
    """
    A set of cardinalities that may be used for properties.
    """
    STRING = 0
    DATE = 1
    STRING_OR_URL = 2
    PLACE = 3
    PERSON_OR_ORGANIZATION = 4
    GRANT = 5
    DATA_MANAGEMENT_PLAN = 6
    URL = 7
    CONTROLLED_VOCABULARY = 8
    PROJECT = 9
    ATTRIBUTION = 10
    IRI = 11
    ADDRESS = 12
    PERSON = 13
    ORGANIZATION = 14


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
    - dataset: # TODO: make multiple
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

    def __init__(self, index: int, name: str, path: str):
        self.index = index
        self.name = name
        self.path = path
        self.files = []
        self.project = Project(name, self)
        self.dataset = Dataset(name, self.project, self)
        self.dataset.project.value = self.project
        self.persons = [Person(self)]
        self.organizations = [Organization(self)]
        self.update_iris()

    def update_iris(self):
        """
        Updates the IRIs of all DataClass fields.

        This method should be called whenever something is added/removed
        to the lists holding DataClass instances (persons, etc.).
        """
        # TODO: this method needs to be called whenever a person/org/dataset is added/removed
        self.project.iri_suffix = "-project"
        self.dataset.iri_suffix = "-dataset"  # TODO: allow multiple
        for i, person in enumerate(self.persons):
            person.iri_suffix = f"-person-{str(i + 1).zfill(3)}"
        for i, org in enumerate(self.organizations):
            org.iri_suffix = f"-organization-{str(i + 1).zfill(3)}"

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
                self.organizations
            ]
        })

    def get_all_properties(self) -> list:
        """
        Returns a list of all properties held by fields of this class. (person, dataset, etc.)
        """
        res = self.project.get_properties()
        res.extend(self.dataset.get_properties())
        for p in self.persons:
            res.extend(p.get_properties())
        for o in self.organizations:
            res.extend(o.get_properties())
        return res

    def validate_graph(self):
        """
        Validates the graph of the entire data against the SHACL ontology.
        """
        graph = self.generate_rdf_graph()
        conforms, results_graph, results_text = pyshacl.validate(
            graph, shacl_graph=ontology_url)
        print(f"Validation result: {conforms}")
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
        self.project.add_rdf_to_graph(graph, "Project")
        # TODO: should allow multiple
        self.dataset.add_rdf_to_graph(graph, "Dataset")
        for i, person in enumerate(self.persons):
            person.add_rdf_to_graph(graph, "Person")
        for i, org in enumerate(self.organizations):
            org.add_rdf_to_graph(graph, "Organization")
        # print("\n------------------\n")
        # print(graph.serialize(format='nt').decode("utf-8"))
        print("\n------------------\n")
        print(graph.serialize(format='turtle').decode("utf-8"))
        print("\n------------------\n")
        # print(graph.serialize(format='xml').decode("utf-8"))
        # print("\n------------------\n")
        # print(graph.serialize(format='json-ld').decode("utf-8"))
        # print("\n------------------\n")
        return graph

    def get_by_iri(self, iri: str):
        if str(self.project) == iri:
            return self.project
        if str(self.dataset) == iri:  # TODO: should be multiple
            return self.dataset
        for o in self.persons:
            if str(o) == iri:
                return o
        for o in self.organizations:
            if str(o) == iri:
                return o


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
            # graph.add((iri, prop.predicate, prop.rdf_value))
            # graph.add(prop.get_triple(iri))
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


class Project(DataClass):
    """
    Project shape.

    Corresponds to `dsp-repo:Project` in our ontology.

    Args:
        name (str): The name of the project
        meta (MetaDataSet): the owning `MetaDataSet`
    """
    def __init__(self, name: str, meta: MetaDataSet):
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
                                    predicate=dsp_repo.hasDescription)

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
                                  Datatype.STRING,
                                  Cardinality.ONE,
                                  value="0000",
                                  predicate=dsp_repo.hasShortCode)

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
                                    predicate=dsp_repo.hasPublication)

        self.contactPoint = Property("Contact Point",
                                     "Contact information",
                                     "",
                                     Datatype.PERSON_OR_ORGANIZATION,
                                     Cardinality.ZERO_OR_ONE,
                                     predicate=dsp_repo.hasContactPoint)

    def get_properties(self):
        return [
            self.name,
            self.description,
            self.keywords,
            self.discipline,
            self.startDate,
            self.endDate,
            self.temporalCoverage,
            self.spatialCoverage,
            self.funder,
            self.grant,
            self.url,
            self.shortcode,
            self.alternateName,
            self.dataManagementPlan,
            self.publication,
            self.contactPoint
        ]

    def __str__(self):
        return f"dsp-repo:Project <{self.name}>"


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
                                         Cardinality.ONE,
                                         predicate=dsp_repo.hasAlternativeTitle)

        self.abstract = Property("Abstract",
                                 "Description of the dataset",
                                 "This is merely an exemplary dataset",
                                 Datatype.STRING_OR_URL,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasAbstract)

        self.sameAs = Property("Alternative URL",
                               "Alternative URL to the dataset, if applicable",
                               "https://test.dasch.swiss/",
                               Datatype.URL,
                               Cardinality.UNBOUND,
                               predicate=dsp_repo.sameAs)

        self.typeOfData = Property("Type of data",
                                   "Type of data related to the dataset: xml, text, image, movie, audio",
                                   "xml",
                                   Datatype.CONTROLLED_VOCABULARY,
                                   Cardinality.ONE_TO_UNBOUND,
                                   value_options=["xml", "text",
                                                  "image", "movie", "audio"],
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
                                  "Testprojekt (test), 2002, https://test.dasch.swiss",
                                  Datatype.STRING,
                                  Cardinality.ONE,
                                  predicate=dsp_repo.hasHowToCite)

        self.status = Property("Dataset status",
                               "Current status of a dataset (testing phase, ongoing, finished)",
                               "The dataset is work in progress",
                               Datatype.STRING,
                               Cardinality.ONE,
                               predicate=dsp_repo.hasStatus)

        self.datePublished = Property("Date published",
                                      "Date of publication",
                                      "2000-08-01",
                                      Datatype.DATE,
                                      Cardinality.ZERO_OR_ONE,
                                      predicate=dsp_repo.hasDatePublished)

        self.language = Property("Language",
                                 "Language(s) of the dataset",
                                 "Hetite",
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
                                     Datatype.URL,
                                     Cardinality.ZERO_OR_ONE,
                                     predicate=dsp_repo.hasDistribution)

    def get_properties(self):
        return [
            self.sameAs,
            self.title,
            self.alternativeTitle,
            self.abstract,
            self.typeOfData,
            self.documentation,
            self.license,
            self.accessConditions,
            self.howToCite,
            self.status,
            self.datePublished,
            self.language,
            self.project,
            self.attribution,
            self.dateCreated,
            self.dateModified,
            self.distribution
        ]

    def __str__(self):
        return f"dsp-repo:Dataset <{self.title}>"

    def get_metadataset(self):
        return self.meta


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
                                  Cardinality.ONE_TO_UNBOUND,
                                  predicate=dsp_repo.hasGivenName)

        self.familyName = Property("Family name",
                                   "Family name of the person",
                                   "Doe",
                                   Datatype.STRING,
                                   Cardinality.ONE_TO_UNBOUND,
                                   predicate=dsp_repo.hasFamilyName)

        self.email = Property("E-mail",
                              "E-mail address of the person",
                              "john.doe@dasch.swiss",
                              Datatype.IRI,
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
            self.sameAs,
            self.givenName,
            self.familyName,
            self.email,
            self.address,
            self.memberOf,
            self.jobTitle
        ]

    def __str__(self):
        return str(self.get_rdf_iri())
        # return f"dsp-repo:Person <{self.givenName} {self.familyName}>"

    def get_metadataset(self):
        return self.meta


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
                              Datatype.IRI,
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
            self.address,
            self.url
        ]

    def __str__(self):
        return str(self.get_rdf_iri())
        # return f"dsp-repo:Organization <{self.name}>"

    def get_metadataset(self):
        return self.meta


# TODO: dsp-repo:Grant (?)
# TODO: dsp-repo:DataManagementPlan
# TODO: schema:PostalAddress


class Property():
    """
    General representation of a property.

    Corresponds to `sh:property`
    """

    # name = None
    # description = None
    # datatype = None
    # cardinality = None

    def __init__(self, name: str, description: str, example: str, datatype: Datatype.STRING,
                 cardinality=Cardinality.UNBOUND, value=None, value_options=None,
                 predicate=dsp_repo.whatever):
        self.name = name
        self.description = description
        self.example = example
        self.datatype = datatype
        self.cardinality = cardinality
        self.value = value
        self.value_options = value_options
        self.predicate = predicate

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
        g = Graph()
        # Ensure the data can be looped
        vals = self.value
        if not isinstance(vals, list):
            vals = [vals]
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
            if datatype == Datatype.STRING or datatype == Datatype.CONTROLLED_VOCABULARY:
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
                # TODO: make this actual link, once this is object, not string
            elif datatype == Datatype.ORGANIZATION:
                g.add((subject, self.predicate, v.get_rdf_iri()))
                # TODO: make this actual link, once this is object, not string
            elif datatype == Datatype.PROJECT:
                g.add((subject, self.predicate, v.get_rdf_iri()))
                # TODO: make this actual link, once this is object, not string
            else:
                print(f"{datatype}: {v}\n-> don't know how to serialize this.\n")
            # TODO: Grant
            # TODO: DMP
            # TODO: Attribution
            # TODO: Address
        return g

    def __str__(self):
        if self.value:
            return str(self.value)
        return f"<Property '{self.name}' undefined>"
