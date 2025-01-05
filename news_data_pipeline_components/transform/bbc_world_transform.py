from typing import Union

import pandas as pd
import requests
from bs4 import BeautifulSoup
from mongoengine.queryset.queryset import QuerySet

from news_data_pipeline_components.shared_code.database_utils import (
    get_entries_above_date,
    get_max_date_by_source_name,
)

from ..shared_code.base_config import BaseConfig
from ..shared_code.database_models import LoadedFeedEntry, TransformedFeedEntry
from .config_transform import TransformConfig
from .nlp_utils import count_number_of_sentences, summarize_articles


def get_text_from_div(story_text_div) -> str:
    if story_text_div is None:
        return ""
    ps = [p.text for p in story_text_div.find_all("p", recursive=False)]
    ps_str = "\n".join(ps)
    return ps_str


def retrieve_bbc_world_content(url: str) -> Union[str, None]:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        html_content = response.text
        soup = BeautifulSoup(html_content, features="html.parser")
        story_text_divs = soup.find_all("div", attrs={"data-component": "text-block"})
        ps_strs = ""
        for story_text_div in story_text_divs:
            text = get_text_from_div(story_text_div)
            ps_strs = ps_strs + text
        return ps_strs
    except Exception as e:
        print(e)
        return None


def main_bbc_world_transform(
    base_config: BaseConfig, transform_config: TransformConfig
):
    source_name = base_config.feeds_info["bbc_world"]["source_name"]
    max_date = get_max_date_by_source_name(
        doc_class=TransformedFeedEntry,
        source_name=source_name,
    )
    entries: QuerySet = get_entries_above_date(
        LoadedFeedEntry, source_name="bbc world", date_dt=max_date
    )

    entries_dict = [entry.to_mongo().to_dict() for entry in entries]
    if len(entries_dict) == 0:
        print("No new entries")
        return
    entries_df = pd.DataFrame(entries_dict)
    entries_df["content"] = (
        entries_df["url"].astype(str).map(retrieve_bbc_world_content)
    )
    entries_df = count_number_of_sentences(
        entries_df, transform_config.sentence_counter
    )
    entries_df = summarize_articles(entries_df, transform_config.article_summarizer)

    entries_df.drop(columns={"_id"}, inplace=True)

    transformed_entries_dict = entries_df.to_dict(orient="records")
    print(transformed_entries_dict)
    for transformed_entry_dict in transformed_entries_dict:
        transformed_entry = TransformedFeedEntry(**transformed_entry_dict)
        TransformedFeedEntry.objects(title=transformed_entry.title).delete()
        transformed_entry.save()

    print(entries_df.head())

    print(source_name)
    return
