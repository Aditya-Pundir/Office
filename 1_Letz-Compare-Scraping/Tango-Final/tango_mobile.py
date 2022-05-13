import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import os
import csv
from datetime import date
from copy import deepcopy

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'browser': 'ALL'}
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service, options=options, desired_capabilities=caps)

config_file_path = "C:/Users/adity/Documents/Code-Playground/Freelance/1_Letz-Compare-Scraping/Tango-Final/config.ini"
JSON_folder_path = "C:/Users/adity/Documents/Code-Playground/Freelance/1_Letz-Compare-Scraping/Tango-Final/JSON-Files/"

if not os.path.exists(config_file_path):
    print("Config File does not exist on the given path!")
if not os.path.exists(JSON_folder_path):
    print("JSON Folder does not exist on the given path!")

output = []
headers = ["device id",
           "title",
           "price range",
           "storage",
           "storage id",
           "storage unit",
           "min price",
           "max price",
           "before promo price",
           "base min price",
           "variation id",
           "Color Title",
           "color variation id",
           "has stock",
           "sku",
           "has device variation stock",
           "subscription"]
headers = [i.title() for i in headers]


def writer(header, data, filename):
    with open(filename, "w+", newline="") as csvfile:
        phones = csv.writer(csvfile)
        phones.writerow(header)
        for x in data:
            phones.writerow(x)


def scrape_smart():
    # Declaring CSV file attributes:
    global csv_data, csv_headers, csv_file, data, config_file_path, JSON_folder_path

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
        time.sleep(5)
        with open(f"{JSON_folder_path}{sub_name.replace(' ', '')}.json", "w+") as file:
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


def scrape_infinity():
    # Declaring CSV file attributes:
    global csv_data, csv_headers, csv_file, data, config_file_path, JSON_folder_path

    driver.get(
        "https://www.tango.lu/en/residential/offers/mobiles/subscriptions/tango-infinity?tab=without")
    time.sleep(5)

    # Accepting the cookies:
    accept_cookies = driver.find_elements(By.CLASS_NAME, "actions__enable_all")
    if len(accept_cookies) != 0:
        accept_cookies[0].click()
        time.sleep(5)

    imgs = driver.find_elements(By.CLASS_NAME, "infinity-image")
    sub_length = len(imgs)
    order_button = driver.find_elements(By.CLASS_NAME, "subscription__select")
    print(order_button)
    subscriptions = []

    for img in imgs:
        if img.get_attribute("src").replace(
                "https://www.tango.lu/sites/tango/modules/custom/tango_commerce_subscriptions/img/", "").replace("_title.png", "") in subscriptions:
            continue

        subscriptions.append(img.get_attribute("src").replace(
            "https://www.tango.lu/sites/tango/modules/custom/tango_commerce_subscriptions/img/", "").replace("_title.png", ""))
    # Clicking the with smartphone selector:
    with_smartphone = driver.find_element(By.CLASS_NAME, "slider.round")
    with_smartphone.click()
    time.sleep(3)

    order_button = driver.find_elements(By.CLASS_NAME, "subscription__select")

    print(subscriptions[0])
    print(subscriptions[1])

    for subscription in range(sub_length):
        print(subscription)
        order_button[subscription].get_attribute("innerText")
        if order_button[subscription].get_attribute("innerText") != "Order\nand choose your mobile":
            continue
        time.sleep(2)
        sub_name = subscriptions[subscription]

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
        time.sleep(5)
        with open(f"{JSON_folder_path}{sub_name.replace(' ', '')}.json", "w+") as file:
            file.write(json.dumps(devices))

        driver.get(
            "https://www.tango.lu/en/residential/offers/mobiles/subscriptions/tango-infinity?tab=without")
        time.sleep(5)

        order_button = driver.find_elements(
            By.CLASS_NAME, "subscription__select")
        with_smartphone = driver.find_element(By.CLASS_NAME, "slider.round")
        with_smartphone.click()
        time.sleep(3)


scrape_infinity()
scrape_smart()


def get_paths():
    global config_file_path, JSON_folder_path

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as f:
            paths = f.readlines()

        source_path = paths[0].strip().split('=')[-1].strip().strip('\"')
        output_path = paths[1].strip().split('=')[-1].strip().strip('\"')
        if os.path.exists(source_path) and os.path.exists(output_path):
            return source_path, output_path
        elif os.path.exists(source_path) and not os.path.exists(output_path):
            print("Output path does not exists! Stopping conversion...")
            return None, None
        elif not os.path.exists(source_path) and os.path.exists(output_path):
            print("Source path does not exists! Stopping conversion...")
            return None, None
        else:
            print("Source and Output path does not exists! Stopping conversion...")
            return None, None
    else:
        print("config.ini file does not exist. Please create one!")
        return None, None


def readFile(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
    data = json.loads(data)
    if isinstance(data, str):
        data = json.loads(data)
    return data


def makeCSV(devices, files):
    for device in devices:
        row = dict.fromkeys(headers)
        row['Device Id'] = device['device_id']
        row['Title'] = device['title']
        row['Price Range'] = device['price_range']
        row['Has Device Variation Stock'] = device['has_device_variation_stock']
        row['Subscription'] = files.replace(".json", "")
        variations = device['variations']
        colors = device['colors']

        for k, variation in variations.items():
            try:
                row['Storage'] = variation['storage']
                row['Storage Id'] = variation['storage_id']
                row['Storage Unit'] = variation['storage_unit']
                row['Min Price'] = variation['min_price']
                row['Max Price'] = variation['max_price']
                row['Before Promo Price'] = variation['before_promo_price']
                row['Base Min Price'] = variation['base_min_price']
                row['Variation Id'] = variation['variation_id']

                for color in colors[variation['storage_id']].values():
                    row['Color Title'] = color['title']
                    row['Color Variation Id'] = color['variation_id']
                    row['Has Stock'] = color['has_stock']
                    row['Sku'] = color['sku']
                    output.append(deepcopy(row))
            except e:
                print()
                print('There was an error in product: ' + row['Device Id'])
                print()


try:
    input_path, output_folder_path = get_paths()
    if input_path and output_folder_path:
        output_file_path = os.path.join(
            output_folder_path, f'Tango-Mobiles_{str(date.today())}.csv')
        print('Reading source files for conversion...')
        print('Converting to CSV...')
        for files in os.listdir(input_path):
            try:
                data = readFile(os.path.join(input_path, files))
                makeCSV(data, files)
            except Exception as e:
                print(e)
                print("There was an error in file", files)

        with open(output_file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(output)
            print('Files converted successfully!')
            print(str(len(output)) +
                  " products along with variants converted to csv.")


except Exception as e:
    print(e)
    print('Could not convert files due to above error. Please run the script again.')
