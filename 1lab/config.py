"""Модуль для работы с конфигом."""
import yaml


def read_cfg(config_path: str = r"configs/local.yaml") -> dict:
    """Функция для парсинга yaml файла."""
    with open(config_path, 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)
        return cfg
