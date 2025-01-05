import os
from dataclasses import dataclass
from typing import Literal

import yaml
from dotenv import load_dotenv

from ..shared_code.soup_builder import SoupBuilder


@dataclass
class LoadConfig:
    soup_builder: SoupBuilder


def get_local_config(config_dict: dict) -> LoadConfig:
    soup_builder = SoupBuilder()
    return LoadConfig(soup_builder=soup_builder)


def get_dev_config(config_dict: dict) -> LoadConfig:
    soup_builder = SoupBuilder()
    return LoadConfig(soup_builder=soup_builder)


def get_config(env_type: Literal["local", "dev"]) -> LoadConfig:
    config_file = os.path.join(
        "news_data_pipeline_components", "load", "config", f"{env_type}.yaml"
    )
    with open(config_file, "r") as fp:
        config_dict = yaml.safe_load(fp)
    if env_type == "local":
        config = get_local_config(config_dict=config_dict)
    elif env_type == "dev":
        config = get_dev_config(config_dict=config_dict)
    return config
