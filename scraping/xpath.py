from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def find_element_by_aria_label(driver, label_text):
    # Construct the XPath expression to find the label element
    xpath_expression = f'//label[@aria-label="{label_text}"]'

    # Find the element using the XPath expression
    matching_element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))

    return matching_element


def find_elements_by_role(driver, role_value):
    # Construct the XPath expression to find elements with the specified role
    xpath_expression = f'//*[@role="{role_value}"]'

    # Find all elements matching the XPath expression
    matching_element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))

    return matching_element


def find_elements_by_expression(driver, expression):
    matching_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, expression)))
    return matching_elements