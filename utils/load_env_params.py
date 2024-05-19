import os


def load_env_params(params: dict[str, object]):
    for param in params:
        os.environ[param.upper()] = str(params[param])


def is_driver_headless() -> bool:
    headless = eval(os.environ.get("HEADLESS"))
    print(headless)
    return headless


def get_driver_path() -> str:
    driver_path = eval(os.environ.get("PATH_TO_CHROMEDRIVER"))
    return driver_path
