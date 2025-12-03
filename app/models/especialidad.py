from dataclasses import dataclass
from typing import Optional


@dataclass(init=False, repr=True, eq=True)
class Especialidad:
    id: int
    nombre: str
    letra: str
    observacion: Optional[str]
    facultad: str
    universidad: Optional[str] = None