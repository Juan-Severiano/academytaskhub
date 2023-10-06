import os
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.edge.service import Service


ROOT_PATH = Path(__file__).parent.parent
EDGEDRIVER_NAME = 'msedgedriver'
EDGEDRIVER_PATH = ROOT_PATH / 'bin' / EDGEDRIVER_NAME


def make_edge_browser(*options):
    edge_options = webdriver.EdgeOptions()

    if options is not None:
        for option in options:
            edge_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        edge_options.add_argument('--headless')

    edge_service = Service(executable_path=EDGEDRIVER_PATH)
    browser = webdriver.Edge(service=edge_service, options=edge_options)
    return browser


if __name__ == '__main__':
    browser = make_edge_browser()
    browser.get('https://google.com/')
    sleep(5)
    browser.quit()
