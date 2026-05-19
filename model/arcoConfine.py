from dataclasses import dataclass

from model.country import Country


@dataclass
class ArcoConfine:
    nazione1: int
    nazione2: int
    anno: int

    def __hash__(self):
        return hash((self.nazione1, self.nazione2))


