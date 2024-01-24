from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def is_parent(el1, el2):
    xpath_expression = './/*'
    try:
        el1_children = find_elements_by_expression(el1, xpath_expression)
        el1_parent_el2 = el2 in el1_children
    except:
        el1_parent_el2 = False
    return el1_parent_el2


def are_siblings(driver, el1, el2):
    are_same_level_siblings = driver.execute_script(
        'return arguments[0].parentNode === arguments[1].parentNode;',
        el1, el2
    )
    return are_same_level_siblings


def same_level_siblings(element):
    # Get the parent element of D1
    parent_element = element.find_element_by_xpath('..')

    # Find all same-level siblings of element
    element_id = element.get_attribute('id')
    same_level_siblings = parent_element.find_elements_by_xpath(f'*[not(@id="{element_id}")]')
    return same_level_siblings


def previous_parent_wsiblings(element):

    cur_depth = 0
    max_depth = 15
    siblings = None
    xpath_expression = '..'
    while cur_depth<max_depth:

        # Rewind 1 step back
        parent = find_elements_by_expression(element, xpath_expression)

        # Check wether it has a sibling
        siblings = same_level_siblings(parent)

        if len(siblings)>0:
            break
        else:
            cur_depth += 1
    return siblings


def previous_parent(element):
    xpath_expression = '..'
    # Rewind 1 step back
    parent = find_elements_by_expression(element, xpath_expression)
    return parent


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


def find_elements_by_expression(driver, expression, delay=10):
    matching_elements = WebDriverWait(driver, delay).until(
        EC.presence_of_all_elements_located((By.XPATH, expression)))
    return matching_elements


def find_characteristics_from_description(current_element):
    # - GET ABOUT THIS VEHICLE
    n_back = 12
    curr_n = 0

    # Find next sibling
    next_sibling = None
    current_parent = current_element
    while curr_n < n_back:
        # Find its 10th parent
        xpath_expression = '..'
        current_parent = find_elements_by_expression(current_parent, xpath_expression)[0]

        # Check if it has span with background image
        try:
            xpath_expression = ".//div[@class and @style]"
            span_img_element = find_elements_by_expression(current_parent, xpath_expression, 1)
            has_background = any(['background-image' in i_.get_attribute('style') for i_ in span_img_element])
            if has_background:
                curr_n = n_back
        except:
            pass

        # Get class
        i_class = current_parent.get_attribute('class')
        if i_class != '':
            # Find next sibling
            try:
                xpath_expression = f"preceding-sibling::div"
                next_sibling = find_elements_by_expression(current_parent, xpath_expression, 1)[0]
                next_sbl_cls = next_sibling.get_attribute('class')
                # Ensure sibling has at least a span
                next_sbl_spn = find_elements_by_expression(next_sbl_cls, "//span", 1)
                print(next_sbl_spn)
                if next_sbl_cls == i_class:
                    # Found next sibling
                    curr_n = n_back
            except:
                curr_n += 1
        else:
            curr_n += 1

    return current_parent, next_sibling


def find_description_from_characteristics(current_element):
    # - GET ABOUT THIS VEHICLE
    n_back = 12
    curr_n = 0

    # Find next sibling
    next_sibling = None
    current_parent = current_element
    while curr_n < n_back:
        # Find its 10th parent
        xpath_expression = '..'
        current_parent = find_elements_by_expression(current_parent, xpath_expression)[0]

        # Get class
        i_class = current_parent.get_attribute('class')
        if i_class != '':
            # Find next sibling
            try:
                xpath_expression = f"following-sibling::div"
                next_sibling = find_elements_by_expression(current_parent, xpath_expression, 1)[0]
                next_sbl_cls = next_sibling.get_attribute('class')
                # Ensure sibling has at least a span
                next_sbl_spn = find_elements_by_expression(next_sbl_cls, "//span", 1)

                # Check if sibling has span with background image
                xpath_expression = ".//div[@class and @style]"
                span_img_element = find_elements_by_expression(next_sbl_cls, xpath_expression, 1)
                has_background = any(['background-image' in i_.get_attribute('style') for i_ in span_img_element])
                assert has_background

                if next_sbl_cls == i_class:
                    # Found next sibling
                    curr_n = n_back
            except:
                curr_n += 1
        else:
            curr_n += 1

    return current_parent, next_sibling


def find_common_parents(driver, element1, element2):

    # Algo
        # 1 - rewind parent 1 until parent of element 2
            # Keep elemen 1[N-1]
        # 2 - rewind element 2 until sibling of element 1[N-1]

    try:
        assert not is_parent(element1, element2)
        assert not is_parent(element2, element1)
    except:
        raise TypeError('Elemets are parents of each other')

    # 1 - rewind element 1 until parent of element 2
    i_step = 0
    max_steps = 12
    while i_step < max_steps:

        # Go back one step
        element1_parent = previous_parent(element1)[0]

        # Check if parent of element 2
        if is_parent(element1_parent, element2):
            break
        else:
            i_step += 1
            element1 = element1_parent

    # 2 - rewind element 2 until sibling of element 1
    i_step = 0
    max_steps = 12
    while i_step < max_steps:

        # Check if they are siblings
        if are_siblings(driver, element1, element2):
            break
        else:
            # rewind element2
            element2 = previous_parent(element2)[0]

    try:
        assert( are_siblings(driver, element1, element2) )
    except:
        raise TypeError('Cannot find sibling classes for elements')

    return element1, element2
