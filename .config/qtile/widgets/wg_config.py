import toml
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Configuration:
    active_cmd: str
    rx_cmd: str
    tx_cmd: str
    up_cmd: str
    down_cmd: str


current_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(current_path, "wg_config.toml")
config_dict = toml.load(config_path)

wg_config = Configuration(**config_dict)
