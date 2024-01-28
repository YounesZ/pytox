from selenium import webdriver
from apps.localvars import FB_DRIVER_TYPE
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from apps.lib.scraper.models.collection.web_scraper import user_agents


def init_chrome_driver():

    if FB_DRIVER_TYPE == 'LOCAL':
        # Set up Chrome options for headless mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
        chrome_options.add_argument(f"user-agent={user_agents()}")
        service= Service( ChromeDriverManager().install() )
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        # Set up Chrome options for headless mode
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        # chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument( user_agents() )

        # options.add_argument("--no-sandbox")
        # options.add_argument("start-maximized")
        # options.add_argument("disable-infobars")
        # options.add_argument("--disable-extensions")
        options.binary_location = '/usr/bin/google-chrome'
        driver = webdriver.Chrome(options=options)

    return driver



