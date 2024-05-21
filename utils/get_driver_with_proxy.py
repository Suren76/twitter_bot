import json
import os
import random
from pathlib import Path

# from selenium.webdriver import Chrome, ChromeOptions, ChromeService, Remote
# from undetected_chromedriver import Chrome, ChromeOptions
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
import seleniumwire.undetected_chromedriver as uc
from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions


from webdriver_manager.chrome import ChromeDriverManager

from utils.ProxyDataItem import ProxyDataItem
from utils.load_env_params import is_driver_headless


def load_proxy_data_on_env(path_to_proxys_file: Path):
    path_to_proxys_file = Path(path_to_proxys_file)
    proxys_data_list_raw = open(path_to_proxys_file).read().split("\n")
    proxys_data_list = list(filter(None, proxys_data_list_raw))

    proxy_data_items_list = ProxyDataItem.get_proxys_list_from_raw_proxys_list(proxys_data_list)
    proxy_data_items_list = ProxyDataItem.get_proxys_list_on_json_format(proxy_data_items_list)
    print(proxy_data_items_list)
    print(type(json.dumps(proxy_data_items_list)))

    os.environ["PROXYS_DATA"] = json.dumps(proxy_data_items_list)
    os.environ["PATH_TO_PROXYS_FILE"] = str(path_to_proxys_file)


def get_random_proxy_data() -> ProxyDataItem:
    proxys_data_list = json.loads(os.environ["PROXYS_DATA"])

    login_data = ProxyDataItem.from_dict(random.choice(proxys_data_list))
    return login_data


def _get_driver_with_proxy(
        url_to_driver,
        proxy: ProxyDataItem,
        headless: bool
):
    options = ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')

    if headless:
        options.add_argument("--headless")

    # login:password@ip:port
    # proxy_helper = SeleniumAuthenticatedProxy(
    #     proxy_url=f"http://{proxy.login}:{proxy.password}@{proxy.ip}:{proxy.port}"
    # )

    # proxy_helper.enrich_chrome_options(options)
    # options.proxy = f"http://{proxy.login}:{proxy.password}@{proxy.ip}:{proxy.port}"
    # options.add_argument("--proxy-server="+f"http://{proxy.login}:{proxy.password}@{proxy.ip}:{proxy.port}")

    # options = uc.ChromeOptions()
    proxy_options = {
        'proxy': {
            'https': f"http://{proxy.login}:{proxy.password}@{proxy.ip}:{proxy.port}",
        }
    }

    # driver = uc.Chrome(options=options, version_main=114, seleniumwire_options=proxy_options)

    if url_to_driver:
        pass
        # driver = Remote(url_to_driver, options=options)
    else:
        # driver = Chrome(options=options, driver_executable_path=ChromeDriverManager().install())
        driver = Chrome(options=options, driver_executable_path=ChromeDriverManager("123").install(), seleniumwire_options=proxy_options)
        driver.set_page_load_timeout(60)

    return driver


def get_driver_with_proxy(url_to_driver: str = None):
    proxy = get_random_proxy_data()
    headless = is_driver_headless()
    return _get_driver_with_proxy(url_to_driver, proxy, headless)
