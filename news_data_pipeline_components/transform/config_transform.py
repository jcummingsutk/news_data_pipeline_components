import os
from dataclasses import dataclass
from typing import Literal

import yaml
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .nlp_utils import ArticleSummarizer, SpacySentenceCounter


@dataclass
class TransformConfig:
    sentence_counter: SpacySentenceCounter
    article_summarizer: ArticleSummarizer


def get_summarizer():
    summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """The following is a news article. Summarize it in two sentences or less. If there is no text, simply reply in all lowercase the word 'none'.""",
            ),
            ("user", "{article}"),
        ]
    )
    output_parser = StrOutputParser()
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = summary_prompt | llm | output_parser
    article_summarizer = ArticleSummarizer(chain)
    return article_summarizer


def get_local_config(config_dict) -> TransformConfig:
    creds_file = os.path.join(
        "news_data_pipeline_components",
        "transform",
        "creds",
        ".env",
    )
    load_dotenv(creds_file)
    spacy_model_name = config_dict["sentence_counter"]["spacy_model_name"]
    sentence_counter = SpacySentenceCounter(model_name=spacy_model_name)
    article_summarizer = get_summarizer()
    return TransformConfig(
        sentence_counter=sentence_counter,
        article_summarizer=article_summarizer,
    )


def get_transform_config(env_type: Literal["local", "dev"]):
    config_file = os.path.join(
        "news_data_pipeline_components",
        "transform",
        "config",
        f"{env_type}.yaml",
    )
    with open(config_file, "r") as fp:
        config_dict = yaml.safe_load(fp)
    if env_type == "local":
        config = get_local_config(config_dict)
        return config
