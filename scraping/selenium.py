from selenium import webdriver
from apps.localvars import FB_DRIVER_TYPE
from webdriver_manager.chrome import ChromeDriverManager
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def init_chrome_driver():

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                         OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(software_names=software_names,
                                   operating_systems=operating_systems,
                                   limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    print(user_agent)

    if FB_DRIVER_TYPE == 'LOCAL':
        # Set up Chrome options for headless mode
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        #chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
        #chrome_options.add_argument(f"user-agent={user_agent}")
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
        options.add_argument( user_agent )
        options.add_argument("--no-sandbox")
        # options.add_argument("start-maximized")
        # options.add_argument("disable-infobars")
        # options.add_argument("--disable-extensions")
        options.binary_location = '/usr/bin/google-chrome'
        driver = webdriver.Chrome(options=options)

    return driver
