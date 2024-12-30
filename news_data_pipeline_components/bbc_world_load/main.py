from .config import Config
import requests
from dataclasses import dataclass
from bs4.element import Tag
from ..shared_code.soup_builder import SoupBuilder


@dataclass
class FeedEntry:
    source_name: str
    title: str
    description: str
    url: str
    date: str


def parse_bs_tag(entry: Tag) -> FeedEntry:
    url = entry.find("link").text
    title = entry.find("title").text
    date = entry.find("pubDate").text
    description = entry.find("description").text
    feed_entry_to_append = FeedEntry(
        source_name="bbc",
        url=url,
        title=title,
        description=description,
        date=date,
    )
    return feed_entry_to_append


def extract_entries(config: Config) -> list[FeedEntry]:
    response = requests.get(config.feed_url)
    rss_feed = response.text
    soup = config.soup_builder.add_markup(rss_feed).add_features("xml").build()
    entries = soup.find_all("item")
    feed_entries: list[FeedEntry] = []
    for entry in entries:
        feed_entry_to_append = parse_bs_tag(entry)
        feed_entries.append(feed_entry_to_append)
    return feed_entries


def main(config: Config):
    entries = extract_entries(config)
    print(entries)


if __name__ == "__main__":
    soup_builder = SoupBuilder()
    config = Config(
        "https://feeds.bbci.co.uk/news/world/rss.xml", soup_builder=soup_builder
    )
    main(config)
