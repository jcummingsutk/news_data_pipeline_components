from .config_load import LoadConfig, get_config

from .npr_politics_load import main_npr_politics
import os
from ..shared_code.database_models import LoadedFeedEntry
from ..shared_code.base_config import get_base_config, BaseConfig


def clear_load_collection():
    LoadedFeedEntry.objects.delete()


def main(load_config: LoadConfig, base_config: BaseConfig):
    LoadedFeedEntry.objects.delete()
    main_npr_politics(load_config=load_config, base_config=base_config)


if __name__ == "__main__":
    env_type = os.getenv("ENVIRONMENT", "local")
    load_config = get_config(env_type)
    base_config = get_base_config(env_type)

    main(load_config=load_config, base_config=base_config)
    first = LoadedFeedEntry.objects.first()
    print(first)
