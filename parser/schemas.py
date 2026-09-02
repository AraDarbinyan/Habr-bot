from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    id: str
    title: str
    url: str
