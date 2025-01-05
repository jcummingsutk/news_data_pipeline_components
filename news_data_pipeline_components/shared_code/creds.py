import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from google.cloud.secretmanager import SecretManagerServiceClient


class CredentialLoader(ABC):
    @abstractmethod
    def load_credentials(self) -> None:
        """"""


class DotEnvFileCredentialLoader(CredentialLoader):
    def __init__(self, filename: str):
        self.filename = filename

    def load_credentials(self) -> None:
        load_dotenv(self.filename)


class GCPSecretLoader(CredentialLoader):
    def __init__(
        self,
        client: SecretManagerServiceClient,
        env_var_keys: list[str],
        secret_names: list[str],
    ):
        self.env_var_keys = env_var_keys
        self.secret_names = secret_names
        self.client = client

    def load_credentials(self):
        for env_var_key, secret_name in zip(self.env_var_keys, self.secret_names):
            print(secret_name)
            response = self.client.access_secret_version(name=secret_name)
            os.environ[env_var_key] = response.payload.data.decode("UTF-8")


def get_local_credential_loader(creds_file: str) -> CredentialLoader:
    return DotEnvFileCredentialLoader(creds_file)


def get_gcp_credential_loader(config_dict: dict) -> CredentialLoader:
    client = SecretManagerServiceClient()
    env_var_keys = []
    secret_names = []
    for env_var_dict in config_dict["credentials"]["credentials-list"]:
        env_var_keys.append(env_var_dict["env_var"])
        secret_names.append(env_var_dict["secret_name"])
    return GCPSecretLoader(
        client=client, env_var_keys=env_var_keys, secret_names=secret_names
    )
