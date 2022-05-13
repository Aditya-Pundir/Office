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


def writer(header, data, filename):
    with open(filename, "w+", newline="") as csvfile:
        phones = csv.writer(csvfile)
        phones.writerow(header)
        for x in data:
            phones.writerow(x)


def scrape_tango():
    # Declaring CSV file attributes:
    csv_data = []
    csv_headers = ("Device ID", "Model", "Subscription", "Price Range", "Storage", "Storage ID",
                   "Storage Unit", "Min Price", "Max Price", "Before Promo Price", "Base Min Price", "Variation ID", "Color Title", "Color Variation ID", "Has Stock", "Sku", "Has Device Variation Stock")

    datime = str(date.today())
    csv_file = f"1_Letz-Compare-Scraping/tango_site/tango_mobiles/tango_phone_{datime}.csv"

    driver.get(
        "https://www.tango.lu/en/residential/offers/mobiles/subscriptions/tango-smart?tab=without")
    time.sleep(5)

    # Accepting the cookies:
    accept_cookies = driver.find_element(By.CLASS_NAME, "actions__enable_all")
    accept_cookies.click()
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
    data = []

    for subscription in range(sub_length):
        if order_button[subscription].get_attribute("innerText") != "Order\nand choose your mobile":
            continue
        if "\n" in subscriptions[subscription].get_attribute("innerText"):
            sub_name = subscriptions[subscription].get_attribute(
                "innerText").split("\n\n", 1)[1]

        else:
            sub_name = subscriptions[subscription].get_attribute(
                "innerText")

        mobile_phones = []
        monthly_price = monthly_prices[subscription].text

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
        time.sleep(15)
        arr = driver.execute_script("return array")
        driver.execute_script("console.log(array)")
        devices = json.loads(arr[0][0]["settings"]
                             ["device_list"]["devices_as_json"])["devices"]
        for device in devices:
            phones.append([sub_name, monthly_price, device])

        time.sleep(5)
        driver.get(
            "https://www.tango.lu/en/residential/offers/mobiles/subscriptions/tango-smart?tab=without")
        time.sleep(5)

        # Clicking the with smartphone selector:
        with_smartphone = driver.find_element(By.CLASS_NAME, "slider.round")
        with_smartphone.click()
        time.sleep(3)

        subscriptions = driver.find_elements(
            By.CLASS_NAME, "aw-subscription_element_title")
        sub_length = len(subscriptions)
        order_button = driver.find_elements(
            By.CLASS_NAME, "subscription__select")
        monthly_prices = driver.find_elements(
            By.CLASS_NAME, "subscription__price")
        print("============================================================================================================")

        for phone in phones:
            to_append = []
            to_append.append({"Device ID": ""})
            to_append.append({"Model": ""})
            to_append.append({"Price Range": ""})
            to_append.append({"Storage": []})
            to_append.append({"Storage ID": []})
            to_append.append({"Storage Unit": []})
            to_append.append({"Min Price": []})
            to_append.append({"Max Price": []})
            to_append.append({"Before Promo Price": []})
            to_append.append({"Base Min Price": []})
            to_append.append({"Variation ID": []})
            to_append.append({"Color Title": []})
            to_append.append({"Color Variation ID": []})
            to_append.append({"Has Stock": []})
            to_append.append({"Sku": []})
            to_append.append({"Has Device Variation Stock": ""})
            to_append.append({"Subscription": sub_name})

            to_append[0]["Device ID"] = phone[2]["device_id"]
            to_append[1]["Model"] = phone[2]["title"]
            to_append[2]["Price Range"] = phone[2]["price_range"]
            to_append[15]["Has Device Variation Stock"] = phone[2]["has_device_variation_stock"]

            for parent_key in list(phone[2]["colors"].keys()):
                colors = []
                for key in list(phone[2]["colors"][parent_key].keys()):
                    colors.append(phone[2]["colors"][parent_key][key])

            for storage in list(phone[2]["variations"].keys()):
                to_append[3]["Storage"].append(
                    phone[2]["variations"][storage]["storage"])
                to_append[4]["Storage ID"].append(
                    phone[2]["variations"][storage]["storage_id"])
                to_append[5]["Storage Unit"].append(
                    phone[2]["variations"][storage]["storage_unit"])
                to_append[6]["Min Price"].append(
                    phone[2]["variations"][storage]["min_price"])
                to_append[7]["Max Price"].append(
                    phone[2]["variations"][storage]["max_price"])
                to_append[8]["Before Promo Price"].append(
                    phone[2]["variations"][storage]["before_promo_price"])
                to_append[9]["Base Min Price"].append(
                    phone[2]["variations"][storage]["base_min_price"])
                to_append[10]["Variation ID"].append(
                    phone[2]["variations"][storage]["variation_id"])
            for color in colors:
                to_append[11]["Color Title"].append(color["title"])
                to_append[12]["Color Variation ID"].append(
                    color["variation_id"])
                to_append[13]["Has Stock"].append(color["has_stock"])
                to_append[14]["Sku"].append(color["sku"])

            mobile_phones.append(to_append)
            print("============================================================================================================")

        validator = []
        for i, phone in enumerate(mobile_phones):
            for storage_option in range(len(phone[3]["Storage"])):
                for color in range(len(phone[11]["Color Title"])):
                    if (phone[0]["Device ID"], phone[1]
                            ["Model"], phone[16]["Subscription"], phone[2]["Price Range"], phone[3]["Storage"][storage_option], phone[4]["Storage ID"][storage_option], phone[5]["Storage Unit"][storage_option], phone[6]["Min Price"][storage_option], phone[7]["Max Price"][0], phone[8]["Before Promo Price"][storage_option], phone[9]["Base Min Price"][storage_option], phone[10]["Variation ID"][storage_option], phone[11]["Color Title"][color], phone[12]["Color Variation ID"][color], phone[13]["Has Stock"][color], phone[14]["Sku"][color], phone[15]["Has Device Variation Stock"]) in data:

                        continue
                    if (phone[0]["Device ID"], phone[1]
                            ["Model"], phone[16]["Subscription"], phone[2]["Price Range"], phone[3]["Storage"][storage_option], phone[4]["Storage ID"][storage_option], phone[5]["Storage Unit"][storage_option], phone[7]["Max Price"][0], phone[8]["Before Promo Price"][storage_option], phone[9]["Base Min Price"][storage_option], phone[10]["Variation ID"][storage_option], phone[11]["Color Title"][color], phone[12]["Color Variation ID"][color], phone[13]["Has Stock"][color], phone[14]["Sku"][color], phone[15]["Has Device Variation Stock"]) in validator:
                        continue
                    else:
                        validator.append((phone[0]["Device ID"], phone[1]
                                          ["Model"], phone[16]["Subscription"], phone[2]["Price Range"], phone[3]["Storage"][storage_option], phone[4]["Storage ID"][storage_option], phone[5]["Storage Unit"][storage_option], phone[7]["Max Price"][0], phone[8]["Before Promo Price"][storage_option], phone[9]["Base Min Price"][storage_option], phone[10]["Variation ID"][storage_option], phone[11]["Color Title"][color], phone[12]["Color Variation ID"][color], phone[13]["Has Stock"][color], phone[14]["Sku"][color], phone[15]["Has Device Variation Stock"]))
                        data.append((phone[0]["Device ID"], phone[1]
                                     ["Model"], phone[16]["Subscription"], phone[2]["Price Range"], phone[3]["Storage"][storage_option], phone[4]["Storage ID"][storage_option], phone[5]["Storage Unit"][storage_option], phone[6]["Min Price"][storage_option], phone[7]["Max Price"][0], phone[8]["Before Promo Price"][storage_option], phone[9]["Base Min Price"][storage_option], phone[10]["Variation ID"][storage_option], phone[11]["Color Title"][color], phone[12]["Color Variation ID"][color], phone[13]["Has Stock"][color], phone[14]["Sku"][color], phone[15]["Has Device Variation Stock"]))

    for piece in data:
        csv_data.append(piece)
    writer(csv_headers, csv_data, csv_file)


scrape_tango()
