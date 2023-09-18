from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class FieldRule:
    field: str
    rule: Optional[Callable] = None


class FileSpec:
    """
    FileSpec defines the rules for parsing raw data fetched from an API.

    Attributes:
        field_rules (List[FieldRule]): A list of FieldRule objects that specify how
          to parse each field in the raw data.
    """

    def __init__(self, field_rules: List[FieldRule]):
        self.field_rules = field_rules

    def parse_data(self, raw_data: List[Dict]) -> List[Dict]:
        """
        Parses the raw data based on the field rules.

        Parameters:
            raw_data (Dict): The raw data to be parsed.

        Returns:
            Dict: The parsed data
        """
        parsed = []
        for data in raw_data:
            if data is not None:
                parsed.append(self._parse_data(data))
        return parsed

    def _parse_data(self, raw_data: Dict) -> Dict:
        parsed_data = {}
        for fr in self.field_rules:
            parsed_data[fr.field] = (
                fr.rule(raw_data.get(fr.field, None))
                if fr.rule
                else raw_data.get(fr.field, None)
            )
        return parsed_data
