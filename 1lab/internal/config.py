"""."""
import yaml


def read_cfg(config_path: str = r"1lab/configs/local.yaml") -> dict:
    """."""
    with open(config_path, 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)
        return cfg
