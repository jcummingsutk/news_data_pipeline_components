import os
from dataclasses import dataclass
from typing import Literal
from urllib.parse import quote_plus

import mongoengine
import yaml
from dotenv import load_dotenv

from .creds import get_gcp_credential_loader


def configure_mongoengine(
    config_dict: dict,
) -> None:
    mongodb_conn_string: str = config_dict["mongodb"]["conn_str"]
    db_name: str = config_dict["mongodb"]["db_name"]
    pwd = quote_plus(os.environ["MONGODB_PASS"])
    mongodb_conn_string = mongodb_conn_string.replace("PASSWORD_ENV_VAR", pwd)
    mongodb_conn_string = mongodb_conn_string.replace("DB_NAME", db_name)
    mongoengine.connect(db_name, host=mongodb_conn_string)


@dataclass
class BaseConfig:
    feeds_info: dict


def get_dev_config(config_dict: dict) -> BaseConfig:
    credential_loader = get_gcp_credential_loader(config_dict=config_dict)
    credential_loader.load_credentials()
    configure_mongoengine(config_dict=config_dict)
    feeds_info = config_dict["feeds_info"]
    return BaseConfig(feeds_info)


def get_local_config(config_dict: dict) -> BaseConfig:
    credential_loader = get_gcp_credential_loader(config_dict=config_dict)
    credential_loader.load_credentials()
    configure_mongoengine(config_dict=config_dict)
    feeds_info = config_dict["feeds_info"]
    return BaseConfig(feeds_info)


def get_base_config(env_type: Literal["local", "dev"]) -> BaseConfig:
    config_file = os.path.join(
        "news_data_pipeline_components", "shared_code", "config", f"{env_type}.yaml"
    )
    with open(config_file, "r") as fp:
        base_config_dict = yaml.safe_load(fp)
    if env_type == "local":
        base_config = get_local_config(base_config_dict)
        return base_config
    elif env_type == "dev":
        base_config = get_dev_config(base_config_dict)
        return base_config

    raise NotImplementedError(f"Unexpected environment type {env_type}")
