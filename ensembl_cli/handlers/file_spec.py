from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class FieldRule:
    field: str
    rule: Optional[Callable] = None


class FileSpec:
    def __init__(self, field_rules: List[FieldRule]):
        self.field_rules = field_rules

    def parse_data(self, raw_data: List[Dict]) -> List[Dict]:
        parsed = []
        for data in raw_data:
            parsed.append(self._parse_data(data))
        return parsed

    def _parse_data(self, raw_data: Dict) -> Dict:
        parsed_data = {}
        for fr in self.field_rules:
            if fr.rule:
                parsed_data[fr.field] = fr.rule(raw_data.get(fr.field, None))
            else:
                parsed_data[fr.field] = raw_data.get(fr.field, None)
        return parsed_data
