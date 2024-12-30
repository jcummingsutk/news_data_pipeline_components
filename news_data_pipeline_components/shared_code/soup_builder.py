from __future__ import annotations
from bs4 import BeautifulSoup


class SoupBuilder:
    def __init__(self):
        self.markup = None
        self.features = None

    def add_markup(self, markup: str) -> SoupBuilder:
        self.markup = markup
        return self

    def add_features(self, features) -> SoupBuilder:
        self.features = features
        return self

    def build(self) -> BeautifulSoup:
        return BeautifulSoup(self.markup, features=self.features)
