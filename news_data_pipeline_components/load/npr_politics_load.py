from .config_load import LoadConfig
import requests
from bs4.element import Tag
from ..shared_code.soup_builder import SoupBuilder
from ..shared_code.base_config import BaseConfig
from ..shared_code.database_models import LoadedFeedEntry
from datetime import datetime


def parse_bs_tag(
    entry: Tag,
    source_name: str,
    datetime_format: str,
) -> LoadedFeedEntry:
    url = entry.find("link").text
    title = entry.find("title").text
    date = entry.find("pubDate").text
    date_dt = datetime.strptime(date, datetime_format)
    description = entry.find("description").text
    loaded_feed_entry = LoadedFeedEntry(
        source_name=source_name,
        title=title,
        date=date_dt,
        description=description,
        url=url,
    )
    return loaded_feed_entry


def extract_entries(
    feed_url: str,
    source_name: str,
    soup_builder: SoupBuilder,
    datetime_format: str,
) -> list[LoadedFeedEntry]:

    response = requests.get(feed_url)
    rss_feed = response.text
    soup = soup_builder.add_markup(rss_feed).add_features("xml").build()
    entries = soup.find_all("item")
    feed_entries: list[LoadedFeedEntry] = []
    for entry in entries:
        feed_entry_to_append = parse_bs_tag(
            entry=entry,
            source_name=source_name,
            datetime_format=datetime_format,
        )
        feed_entries.append(feed_entry_to_append)
    return feed_entries


def main_npr_politics(load_config: LoadConfig, base_config: BaseConfig):
    feed_url = base_config.feeds_info["npr_politics"]["feed_url"]
    source_name = base_config.feeds_info["npr_politics"]["source_name"]
    datetime_format = base_config.feeds_info["npr_politics"]["datetime_format"]
    soup_builder = load_config.soup_builder
    extracted_entries = extract_entries(
        feed_url=feed_url,
        source_name=source_name,
        soup_builder=soup_builder,
        datetime_format=datetime_format,
    )
    for extracted_entry in extracted_entries:
        extracted_entry.save()
