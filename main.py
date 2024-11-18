from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")


timeout = time.time() + 5
five_min = time.time() + 60 * 5

cookie_button = driver.find_element(By.ID, value="cookie")

items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

while True:
    cookie_button.click()

    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text:
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        cookie_upgrades = {}
        for i in range(len(item_prices)):
            cookie_upgrades[item_prices[i]] = item_ids[i]


        money_elem = driver.find_element(By.ID, "money").text
        if "," in money_elem:
            money_elem = money_elem.replace(",", "")
        cookie_count = int(money_elem)


        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count >= cost:
                affordable_upgrades[cost] = id


        highest_affordable_upgrade_price = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_affordable_upgrade_price]

        driver.find_element(By.ID, to_purchase_id).click()

        timeout = time.time() + 5

    if time.time() > five_min:
        per_second = driver.find_element(By.ID, "cps").text
        print(f"Cookies/second: {per_second}")
        break

