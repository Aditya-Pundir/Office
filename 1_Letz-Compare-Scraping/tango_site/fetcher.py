import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import date
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'browser': 'ALL'}
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service, options=options, desired_capabilities=caps)

csv_headers = ("Device ID", "Model", "Subscription", "Price Range", "Storage", "Storage ID",
               "Storage Unit", "Min Price", "Max Price", "Before Promo Price", "Base Min Price", "Variation ID", "Color Title", "Color Variation ID", "Has Stock", "Sku", "Has Device Variation Stock")
datime = str(date.today())
csv_file = f"1_Letz-Compare-Scraping/tango_site/tango_mobiles/tango_phone_{datime}.csv"
csv_data = []
data = []


def writer(header, data, filename):
    with open(filename, "w+", newline="") as csvfile:
        phones = csv.writer(csvfile)
        phones.writerow(header)
        for x in data:
            phones.writerow(x)


def scrape_tango():
    # Declaring CSV file attributes:
    global csv_data, csv_headers, csv_file, data

    driver.get(
        "https://www.tango.lu/en/residential/offers/mobiles/subscriptions/tango-smart?tab=without")
    time.sleep(5)

    # Accepting the cookies:
    accept_cookies = driver.find_elements(By.CLASS_NAME, "actions__enable_all")
    if len(accept_cookies) != 0:
        accept_cookies[0].click()
        time.sleep(5)

    # CLicking the with smartphone selector:
    with_smartphone = driver.find_element(By.CLASS_NAME, "slider.round")
    with_smartphone.click()
    time.sleep(3)

    subscriptions = driver.find_elements(
        By.CLASS_NAME, "aw-subscription_element_title")
    sub_length = len(subscriptions)
    order_button = driver.find_elements(By.CLASS_NAME, "subscription__select")
    monthly_prices = driver.find_elements(By.CLASS_NAME, "subscription__price")
    phones = []

    for subscription in range(sub_length):
        if order_button[subscription].get_attribute("innerText") != "Order\nand choose your mobile":
            continue
        if "\n" in subscriptions[subscription].get_attribute("innerText"):
            sub_name = subscriptions[subscription].get_attribute(
                "innerText").split("\n\n", 1)[1]

        else:
            sub_name = subscriptions[subscription].get_attribute(
                "innerText")

        # mobile_phones = []
        # monthly_price = monthly_prices[subscription].text

        print("--------------------------------------------------------")
        script = """XMLHttpRequest.prototype.realSend = XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.send = function(value) {
    this.addEventListener("progress", function(e){
        if(e.target.responseURL == "https://www.tango.lu/en/system/ajax"){
            try{
                array = [];
                array.push(JSON.parse(e.target.response));
            }
            catch(err){
                console.log("")
            }
        }
        else{
            console.log(e.target.responseURL)
        }
    }, false);
    this.realSend(value);
};"""
        driver.execute_script(script)
        time.sleep(5)

        order_button[subscription].click()
        time.sleep(20)
        arr = driver.execute_script("return array")
        driver.execute_script("console.log(array)")
        devices = json.loads(arr[0][0]["settings"]
                             ["device_list"]["devices_as_json"])["devices"]
        with open(f"1_Letz-Compare-Scraping/tango_site/json_files/{sub_name.replace(' ', '')}.json", "w+") as file:
            file.write(json.dumps(devices))

        driver.get(
            "https://www.tango.lu/en/residential/offers/mobiles/subscriptions/tango-smart?tab=without")
        time.sleep(5)

        order_button = driver.find_elements(
            By.CLASS_NAME, "subscription__select")
        subscriptions = driver.find_elements(
            By.CLASS_NAME, "aw-subscription_element_title")
        sub_length = len(subscriptions)
        with_smartphone = driver.find_element(By.CLASS_NAME, "slider.round")
        with_smartphone.click()
        time.sleep(3)


# tango_smart()
scrape_tango()

for piece in data:
    csv_data.append(piece)
writer(csv_headers, csv_data, csv_file)
