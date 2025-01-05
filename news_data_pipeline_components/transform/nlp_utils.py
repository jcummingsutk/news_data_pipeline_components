from typing import Union

import pandas as pd
import spacy


class SpacySentenceCounter:
    def __init__(self, model_name: str):
        self.nlp = spacy.load(model_name)

    def __call__(self, text: Union[str, None]) -> Union[int, None]:
        if text is None:
            return None
        doc = self.nlp(text)
        num_sentences = len(list(doc.sents))
        return num_sentences


class ArticleSummarizer:
    def __init__(self, chain):
        self.chain = chain

    def __call__(self, text: Union[str, None]) -> Union[str, None]:
        summary = self.chain.invoke(text)
        if summary == "none":
            return None
        return summary


def count_number_of_sentences(
    df: pd.DataFrame, sentence_counter: SpacySentenceCounter
) -> pd.DataFrame:
    df["num_sentences_in_content"] = 0
    content_not_null_mask = ~df["content"].isna()
    df.loc[content_not_null_mask, "num_sentences_in_content"] = df.loc[
        content_not_null_mask, "content"
    ].map(sentence_counter)
    return df


def summarize_articles(
    df: pd.DataFrame, article_summarizer: ArticleSummarizer
) -> pd.DataFrame:
    content_to_summarize_mask = df["num_sentences_in_content"] > 0
    df["summary"] = "No summary available"
    df.loc[content_to_summarize_mask, "summary"] = df.loc[
        content_to_summarize_mask, "content"
    ].map(article_summarizer)
    return df
