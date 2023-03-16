from dataclasses import dataclass, field
from enum import StrEnum
import re


class UrlType(StrEnum):
    URL = "url"
    GEONAMES = "Geonames"
    PLEIADES = "Pleiades"
    UNESCO = "unesco6"
    PERIODO = "Periodo"
    CHRONONTOLOGY = "Chronontology"
    GND = "GND"
    VIAF = "VIAF"
    GRID = "Grid"


@dataclass
class Url:
    url: str
    text: str
    type: UrlType = UrlType.URL


@dataclass
class LangString:
    langStrings: dict[str, str]

    def __post_init__(self) -> None:
        for k, v in self.langStrings.items():
            assert re.match('^[a-z]{2}$', k)
            assert v


@dataclass
class Address:
    street: str
    postal_code: str
    locality: str
    country: str
    additional: str | None = None
    canton: str | None = None


@dataclass
class Organization:
    name: str
    url: Url | None = None
    address: Address | None = None
    email: str | None = None
    alternative_names: list[LangString] = field(default_factory=list)
    authority_refs: list[Url] = field(default_factory=list)


@dataclass
class Project:
    shortcode: str
    name: str
    description: str
