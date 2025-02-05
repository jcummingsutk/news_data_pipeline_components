import os

from ..shared_code.base_config import BaseConfig, get_base_config
from .bbc_world_transform import main_bbc_world_transform
from .config_transform import TransformConfig, get_transform_config
from .npr_politics_transform import main_npr_politics_transform


def main_transform(base_config: BaseConfig, transform_config: TransformConfig):
    main_bbc_world_transform(base_config=base_config, transform_config=transform_config)
    main_npr_politics_transform(
        base_config=base_config, transform_config=transform_config
    )


if __name__ == "__main__":
    env_type = os.getenv("ENVIRONMENT", "local")
    tranform_config = get_transform_config(env_type)
    base_config = get_base_config(env_type)

    main_transform(base_config=base_config, transform_config=tranform_config)
