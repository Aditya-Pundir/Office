from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--window-size=1200,900")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def writer(header, data, filename):
    with open(filename, "w+", newline="") as csvfile:
        phones = csv.writer(csvfile)
        phones.writerow(header)
        for x in data:
            phones.writerow(x)


def scrape_orange():
    csv_headers = ("Brand", "Model", "Color", "Storage", "Plan",
                   "Plan Value", "Monthly Price", "Commitment Period", "Today Price")

    csv_file = "1_Letz-Compare-Scraping\\orange_site\\orange_phone.csv"
    csv_data = []

    driver.get("https://www.orange.lu/en/smartphones/")
    accept_cookies = driver.find_element(By.ID, "didomi-notice-agree-button")
    accept_cookies.click()
    vendors = driver.find_elements(By.CLASS_NAME, "c-product-card__vendor")
    model_names = driver.find_elements(By.CLASS_NAME, "c-product-card__name")
    a_tags = driver.find_elements(
        By.CLASS_NAME, "u-expand.btn.btn-primary.btn-lg.u-full-width.u-block.u-center")
    with open("1_Letz-Compare-Scraping\\orange_site\\items_links.txt", "w+") as link_file:
        for i in range(len(a_tags)):
            link_file.write(a_tags[i].get_attribute("href") + "\n")

    with open("1_Letz-Compare-Scraping\\orange_site\\items_links.txt", "r") as link_file:
        links = link_file.readlines()

    with open("1_Letz-Compare-Scraping\\orange_site\\vendors.txt", "w+") as vendors_file:
        for i in range(len(vendors)):
            vendors_file.write(vendors[i].text + "\n")

    with open("1_Letz-Compare-Scraping\\orange_site\\vendors.txt", "r") as vendors_file:
        vendors = vendors_file.readlines()

    with open("1_Letz-Compare-Scraping\\orange_site\\models.txt", "w+") as models_file:
        for i in range(len(model_names)):
            models_file.write(model_names[i].text + "\n")

    with open("1_Letz-Compare-Scraping\\orange_site\\models.txt", "r") as models_file:
        model_names = models_file.readlines()

    colors = []
    storage_options = []
    plans = []
    commitment_periods = []
    monthly_prices = []
    mobile_phones = []

    for vendor in range(len(vendors)):
        print(vendors[vendor])

    for model in range(len(model_names)):
        print(model_names[model])

    print("--------------------------------------------------------------------------------")

    for link in range(len(links)):
        link = links[link]

        driver.get(link)
        time.sleep(5)
        colors = driver.find_elements(
            By.CLASS_NAME, "gtm-section-product-color")
        storage_options = driver.find_elements(
            By.CLASS_NAME, "gtm-section-product-capacity")
        phone = driver.find_element(By.CLASS_NAME, "t-h1")
        brand = phone.text.split("\n")[0]
        phone = phone.text.split("\n")[1]
        plans = driver.find_elements(
            By.CSS_SELECTOR, ".gtm-section-offer > .c-plan-card__top > .u-marg-b-xxs > .t-h2")
        commitment_periods = driver.find_elements(
            By.CSS_SELECTOR, ".gtm-section-offer > .c-plan-card__top > .c-pricing > .c-pricing__muted-text")
        monthly_prices = driver.find_elements(
            By.CSS_SELECTOR, ".gtm-section-offer > .c-plan-card__top > .c-pricing > .c-pricing__price")
        today_prices = driver.find_elements(
            By.CLASS_NAME, "c-pricing.u-marg-t-xxxs")

        to_append = []
        to_append.append(brand)
        to_append.append(phone)
        to_append.append({"colors": []})
        to_append.append({"storage_options": []})
        to_append.append({"plans": []})
        to_append.append({"plan_values": []})
        to_append.append({"monthly_plans": []})
        to_append.append({"periods": []})
        to_append.append({"today_prices": []})
        for color in range(len(colors)):
            to_append[2]["colors"].append(
                colors[color].get_attribute("data-label"))

        for option in range(len(storage_options)):
            to_append[3]["storage_options"].append(
                storage_options[option].text)

        for plan in range(len(plans)):
            if plan == 0 or plan % 2 == 0:
                to_append[4]["plans"].append(
                    plans[plan].get_attribute("innerHTML"))
            else:
                to_append[5]["plan_values"].append(
                    plans[plan].get_attribute("innerHTML"))

        for period in range(len(commitment_periods)):
            complete_per = commitment_periods[period].get_attribute(
                "innerHTML").replace("<br>", " ").split(" ", 1)
            complete_pri = monthly_prices[period].get_attribute(
                "innerHTML").replace("€", "") + " " + complete_per[0]
            per = complete_per[1]

            to_append[7]["periods"].append(per)

            to_append[6]["monthly_plans"].append(complete_pri)

        for today_price in today_prices:
            to_append[8]["today_prices"].append(today_price.get_attribute("innerText").split(
                "€", 1)[1].replace("€", " and ").replace("\n", " "))

        mobile_phones.append(to_append)

    for phone in mobile_phones:
        for storage_option in range(len(phone[3]["storage_options"])):
            for color in range(len(phone[2]["colors"])):
                for plan in range(len(phone[4]["plans"])):
                    for monthly_plan in range(len(phone[6]["monthly_plans"])):
                        csv_data.append((phone[0], phone[1], phone[2]["colors"]
                                        [color], phone[3]["storage_options"][storage_option], phone[4]["plans"][plan], phone[5]["plan_values"][plan], phone[6]["monthly_plans"][monthly_plan], phone[7]["periods"][monthly_plan], phone[8]["today_prices"][monthly_plan]))

    print(
        "--------------------------------------------------------------------------------")

    writer(csv_headers, csv_data, csv_file)


scrape_orange()
