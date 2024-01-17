import time
from os import getenv
from dotenv import load_dotenv
from apps.localvars import FB_CARS_URL, PATH_TO_CODE, FB_MIN_PRICE, FB_SCROLL_DELAY, FB_SCROLL_COUNT, FB_CARD_HREF_STRING
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from submodules.pytox.scraping.xpath import find_element_by_aria_label, find_elements_by_role, find_elements_by_expression


load_dotenv(PATH_TO_CODE)


def fb_enter_user_password(driver):
    # Load facebook credentials
    username = getenv('FB_USERNAME')
    password = getenv('FB_PASSWORD')

    # Find email and password elements using Selenium
    email_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )

    pass_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'pass'))
    )

    # Now, you have the email and password elements, and you can send keys to them
    # For example, sending keys to the email and password fields
    email_element.send_keys(username)
    pass_element.send_keys(password)
    return


def fb_click_login(driver):
    # Click on login button
    button_name = 'login'
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, button_name))
    )

    # Click the button
    button.click()
    return


def fb_navigate_to_cars(driver):
    # Setup full url
    full_url = f'{FB_CARS_URL}/?minPrice={FB_MIN_PRICE}'

    # Visit url
    driver.get(full_url)
    return


def fb_set_location(driver):
    # --- CLIK ON LOCATION
    # Specify the target URL in the background-image
    target_txt = "Roberval"
    xpath_expression = f"//div[contains(@role, 'button')]//span[contains(text(), '{target_txt}')]"
    matching_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath_expression))
    )
    # Click on matching element
    matching_elements[0].click()

    # --- CLICK ON RADIUS DROPDOWN
    # Specify the label text you are looking for
    label_text = 'Rayon'
    # Find the element with the specified 'aria-label'
    matching_element = find_element_by_aria_label(driver, label_text)
    matching_element[0].click()

    # --- SELECT LAST OPTION
    # Specify the role value you are looking for (e.g., "option")
    role_value = 'option'

    # Find all elements with the specified role
    matching_element = find_elements_by_role(driver, role_value)[-1]
    matching_element.click()

    # --- HIT APPLY
    # Specify the role value you are looking for (e.g., "button")
    role_value = 'button'
    # Find all elements with the specified role
    matching_elements = find_elements_by_role(driver, role_value)
    # Find all elements with desired text
    matching_element = [i_ for i_ in matching_elements if i_.text.lower() in ['appliquer', 'apply']][0]
    matching_element.click()


def fb_scroll_down_page(driver):
    # Scroll down to load more results
    for i_ in range(FB_SCROLL_COUNT):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(FB_SCROLL_DELAY)
    return


def fb_list_cards(driver):
    # --- LIST THE CARDS
    # Specify the target URL in the background-image
    xpath_expression = f'//div[a[@role="link" and contains(@href, "{FB_CARD_HREF_STRING}")]/descendant::img[@src]]'
    matching_elements = find_elements_by_expression(driver, xpath_expression)
    card_urls = [find_elements_by_expression(i_, './a')[0].get_attribute('href') for i_ in matching_elements]
    return card_urls


def fb_get_product_images(driver):
    xpath_expression = f"//div[@aria-label and @role='button']//img[@src]"
    imgs = find_elements_by_expression(driver, xpath_expression)
    imgs = [i_.get_attribute('src') for i_ in imgs]
    return imgs


def fb_get_ptoduct_title(driver):
    # GET TITLE
    xpath_expression = f"//h1[@class]//span[@class]"
    ttl_elem = driver.find_element("xpath", xpath_expression)
    title = ttl_elem.get_attribute('innerText')
    return ttl_elem, title


def fb_get_product_price_from_title(title_element):
    # GET PRICE
    # find parent
    xpath_expression = "../.."
    parent_div = find_elements_by_expression(title_element, xpath_expression)[0]
    # find price
    price_div_xpath = "following-sibling::div"
    price_div = find_elements_by_expression(parent_div, price_div_xpath)[0]
    price = price_div.get_attribute('innerText')
    return price_div, price


def fb_get_product_date_from_price(driver, price_element):
    # - GET DATE POSTED
    price_div_xpath = "following-sibling::div"
    about_div = find_elements_by_expression(price_element, price_div_xpath)[0]
    date_posted = about_div.get_attribute('innerText')
    return about_div, date_posted


def fb_get_product_characteristics_from_about(driver, about_div):
    # - GET ABOUT THIS VEHICLE
    # Find the span
    target_txt = 'À propos de ce véhicule'
    xpath_expression = f"//h2//span[contains(text(), '{target_txt}')]"
    matching_elements = find_elements_by_expression(driver, xpath_expression)[0]
    # Find its 10th parent
    xpath_expression = '/'.join(['..'] * 10)
    parent_div = find_elements_by_expression(matching_elements, xpath_expression)[0]
    # Get next div
    price_div_xpath = "following-sibling::div"
    next_div = find_elements_by_expression(parent_div, price_div_xpath)[0]
    # -Get children
    # mileage
    next_children = find_elements_by_expression(next_div, "./*")
    mileage = find_elements_by_expression(next_children[0], ".//span")
    mileage = mileage[0].text
    # transmission
    transmission = find_elements_by_expression(next_children[1], ".//span")
    transmission = transmission[0].text
    # color
    color = find_elements_by_expression(next_children[2], ".//span")
    color = color[0].text
    return parent_div, mileage, transmission, color


def fb_get_production_description_from_parent(driver, parent_div):
    # - GET DESCRIPTION
    # Get holder section
    pparent_div = find_elements_by_expression(parent_div, '..')[0]
    next_pparent_div = find_elements_by_expression(pparent_div, 'following-sibling::div')[0]
    # Get desc subsection
    next_pparent_children = find_elements_by_expression(next_pparent_div, "./*")[-1]
    # click on 'voir plus'
    all_children_desc = find_elements_by_expression(next_pparent_children, ".//div[@role='button']")
    voir_button = find_elements_by_expression(all_children_desc[0], ".//span")[0]
    voir_button.click()
    # Get description
    description = next_pparent_children.get_attribute('innerText')
    return description



if __name__ == '__main__':
    pass