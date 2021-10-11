# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field


@dataclass
class ProjectItem:
    name: str
    description: str
    url: str
    downloads: int
    owners: list = field(default_factory=lambda: [])
    owners_urls: list = field(default_factory=lambda: [])
