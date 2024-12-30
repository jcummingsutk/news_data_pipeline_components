from dataclasses import dataclass
from ..shared_code.soup_builder import SoupBuilder


@dataclass
class Config:
    feed_url: str
    soup_builder: SoupBuilder
