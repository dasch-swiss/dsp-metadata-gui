from enum import Enum


class Validity(Enum):
    VALID = 0
    INVALID_VALUE = 1
    REQUIRED_VALUE_MISSING = 2
    OPTIONAL_VALUE_MISSING = 3


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
        if Cardinality.isMandatory(card):
            return "Mandatory"
        else:
            return "Optional"

    def isMandatory(card) -> bool:
        if card == Cardinality.ONE \
                or card == Cardinality.ONE_TO_TWO \
                or card == Cardinality.ONE_TO_UNBOUND:
            return True
        if card == Cardinality.UNBOUND \
                or card == Cardinality.ZERO_OR_ONE \
                or card == Cardinality.ZERO_TO_TWO:
            return False


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
