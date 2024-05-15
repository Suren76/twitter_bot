import json
import os
import random
from pathlib import Path

from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from webdriver_manager.chrome import ChromeDriverManager

from utils.ProxyDataItem import ProxyDataItem


def load_proxy_data_on_env(path_to_proxys_file: Path):
    path_to_proxys_file = Path(path_to_proxys_file)
    proxys_data_list_raw = open(path_to_proxys_file).read().split("\n")
    proxys_data_list = list(filter(None, proxys_data_list_raw))

    proxy_data_items_list = ProxyDataItem.get_proxys_list_from_raw_proxys_list(proxys_data_list)
    proxy_data_items_list = ProxyDataItem.get_proxys_list_on_json_format(proxy_data_items_list)
    # print(proxy_data_items_list)
    # print(type(json.dumps(proxy_data_items_list)))

    os.environ["PROXYS_DATA"] = json.dumps(proxy_data_items_list)
    os.environ["PATH_TO_PROXYS_FILE"] = str(path_to_proxys_file)


def get_random_proxy_data() -> ProxyDataItem:
    proxys_data_list = json.loads(os.environ["PROXYS_DATA"])

    login_data = ProxyDataItem.from_dict(random.choice(proxys_data_list))
    return login_data


def _get_driver_with_proxy(
        url_to_driver,
        proxy: ProxyDataItem = ProxyDataItem('65.108.12.231', 10130, "eBooyiTfVd",'KyjoJZP7tb')
):
    options = ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # login:password@ip:port
    proxy_helper = SeleniumAuthenticatedProxy(
        proxy_url=f"http://{proxy.login}:{proxy.password}@{proxy.ip}:{proxy.port}"
    )

    proxy_helper.enrich_chrome_options(options)
    if url_to_driver:
        pass
        # driver = Remote(url_to_driver, options=options)
    else:
        # driver = Chrome(options=options, driver_executable_path=ChromeDriverManager().install())
        driver = Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

    return driver


def get_driver_with_proxy(url_to_driver: str=None):
    proxy = get_random_proxy_data()
    return _get_driver_with_proxy(url_to_driver, proxy)
