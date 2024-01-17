from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def init_chrome_driver():
    service= Service( ChromeDriverManager().install() )
    driver = webdriver.Chrome(service=service)
    return driver

