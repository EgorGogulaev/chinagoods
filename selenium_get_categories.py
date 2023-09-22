import time

import undetected_chromedriver as uc
from selenium.webdriver import ChromeOptions, Chrome, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def get_categories_links():
    dict_with_links = {}
    options = ChromeOptions()
    options.add_argument("--headless")
    with Chrome(options=options) as browser:
        action = ActionChains(driver=browser)
        wait = WebDriverWait(driver=browser, timeout=10)
        browser.get("https://en.chinagoods.com/screen/product?parent_product_type_id=271&parent_product_type_name=Global%20Goods&time=1694783202416")
        len_main_categories = len(browser.find_elements(By.CSS_SELECTOR, 'div[class="condition__con"]')[0].find_elements(By.CSS_SELECTOR, 'ul[data-v-01c0d224] li')[1:])

        for num_category in range(22, len_main_categories + 1):
            main_category_element = browser.find_elements(By.CSS_SELECTOR, 'div[class="condition__con"]')[0].find_elements(By.CSS_SELECTOR, 'ul[data-v-01c0d224] li')[num_category]
            main_category_name = main_category_element.text
            action.move_to_element(main_category_element).click().perform()
            dict_with_links[main_category_name] = {}
            len_sub_categories = len(browser.find_elements(By.CSS_SELECTOR, 'div[class="condition__con"]')[1].find_elements(By.CSS_SELECTOR, 'ul[data-v-01c0d224] li')[1:])
            for num_sub_category in range(1, len_sub_categories + 1):
                sub_categoty_element = browser.find_elements(By.CSS_SELECTOR, 'div[class="condition__con"]')[1].find_elements(By.CSS_SELECTOR, 'ul[data-v-01c0d224] li')[num_sub_category]
                sub_category_name = sub_categoty_element.text
                action.move_to_element(sub_categoty_element).click().perform()
                sub_categoty_URL = browser.current_url
                dict_with_links[main_category_name][sub_category_name] = sub_categoty_URL
                print(dict_with_links)

    return dict_with_links






if __name__ == '__main__':
    result_dict = get_categories_links()
    print(result_dict)