"""main файл."""
from internal.config import read_cfg


def main():
    """."""
    cfg = read_cfg()

    print(cfg)

    # TODO: инициализировать сервер

    # назначить обработчик запросов
    pass


if __name__ == "__main__":
    main()
