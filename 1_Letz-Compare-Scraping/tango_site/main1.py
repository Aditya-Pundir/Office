from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def writer(header, data, filename):
    with open(filename, "w+", newline="") as csvfile:
        phones = csv.writer(csvfile)
        phones.writerow(header)
        for x in data:
            phones.writerow(x)


def scrape_tango():
    csv_headers = ("Brand", "Model", "Color", "Storage", "Subscription",
                   "Commitment Periods", "Offers", "Smartphone Prices", "Original Smartphone Prices")

    csv_file = "1_Letz-Compare-Scraping\\tango_site\\tango_phone.csv"
    csv_data = []

    driver.get(
        "https://www.tango.lu/en/residential/offers/mobiles/devices-smartphones-and-tablets")
    accept_cookies = driver.find_element(By.CLASS_NAME, "actions__enable_all")
    accept_cookies.click()
    time.sleep(20)
    see_more = driver.find_element(By.ID, "devices-pager")
    while "display: none;" not in see_more.get_attribute("style"):
        see_more.click()
    colors = []
    a_tags = driver.find_elements(
        By.CSS_SELECTOR, ".device-item-variation > .button-pink")
    mobile_phones = []
    to_append = []

    with open("1_Letz-Compare-Scraping\\tango_site\\items_links.txt", "w+") as link_file:
        for link in a_tags:
            link_file.write(link.get_attribute("href") + "\n")

    with open("1_Letz-Compare-Scraping\\tango_site\\items_links.txt", "r") as link_file:
        links = link_file.readlines()

    previous_phone = ""

    for link in links:
        new_phone = link.replace("\n", "").split("?sku=")[0]

        if new_phone == previous_phone:
            continue
        else:
            previous_phone = new_phone
        time.sleep(5)
        driver.get(new_phone)
        brand = driver.find_element(By.CLASS_NAME, "brand")
        model = driver.find_element(By.CLASS_NAME, "range")
        color_container = driver.find_element(
            By.CLASS_NAME, "device-item-variation-colors")

        to_append = []
        to_append.append(brand.text)
        to_append.append(model.text)
        to_append.append({"colors": []})
        to_append.append({"storage_options": []})
        to_append.append({"subscriptions": []})
        # to_append.append({"subscription_value_container": []})
        # to_append.append({"subscription_details": []})
        # to_append.append({"monthly_prices": []})
        # to_append.append({"original_monthly_prices": []})
        to_append.append({"commitment_periods": []})
        to_append.append({"offers": []})
        to_append.append({"smartphone_prices": []})
        to_append.append({"original_smartphone_prices": []})

        colors = color_container.get_attribute("innerText").replace(
            "\n", "").split(" ")
        to_append[2]["colors"].append(colors)

        storage_options = driver.find_element(
            By.XPATH, """//*[@id="block-system-main"]/div/div[1]/article/div/div[2]/div/div/div[2]/div[2]/div""")
        for option in storage_options.get_attribute("innerText").split("\n"):
            option = option.replace("GO", "GB").replace(
                "TO", "TB").replace("MO", "MB").replace("KO", "KB")
            to_append[3]["storage_options"].append(option)

        subscriptions = driver.find_elements(
            By.CLASS_NAME, "device-variation-subscription-item_title")
        # subscription_value_container = driver.find_elements(
        #     By.CLASS_NAME, "subscription-details__first")

        for subscription in subscriptions:
            to_append[4]["subscriptions"].append(
                subscription.get_attribute("innerText").split("\n")[0])

        # for subscription_value in subscription_value_container:
        #     value = subscription_value.get_attribute(
        #         "innerText").replace("\n\n", " ").replace("\n", " ")
        #     print(value)
        #     to_append[5]["subscription_value_container"].append(value)

        # monthly_prices = driver.find_elements(
        #     By.CLASS_NAME, "device-variation-subscription-item_promoPrice")

        # original_monthly_prices = driver.find_elements(
        #     By.CLASS_NAME, "device-variation-subscription-item_price")

        # if len(monthly_prices) == 0:
        #     monthly_prices = driver.find_elements(
        #         By.CLASS_NAME, "device-variation-subscription-item_price")

        # if len(original_monthly_prices) == 0:
        #     to_append[6]["original_monthly_prices"].append(
        #         "No original monthly price")

        # for original_monthly_price in original_monthly_prices:
        #     price = original_monthly_price.get_attribute("data-price").replace(
        #         "€", "")
        #     to_append[6]["original_monthly_prices"].append(price)

        # for monthly_price in monthly_prices:
        #     price = monthly_price.get_attribute("innerText").replace(
        #         " € ", "").replace("/mois", "")
        #     to_append[5]["monthly_prices"].append(price)

        commitment_periods = driver.find_elements(
            By.XPATH, """//*[@id="block-system-main"]/div/div[1]/article/div/div[7]/div/div/p[2]""")

        if len(commitment_periods) == 0:
            to_append[5]["commitment_periods"].append(
                "No commitment period given")

        for period in commitment_periods:
            if len(commitment_periods) == 0:
                break
            else:
                to_append[5]["commitment_periods"].append(
                    period.get_attribute("innerText").replace("The My New Mobile option allows you to reduce the price of your device and spread the payment over ", ""))

        offers = driver.find_elements(
            By.CLASS_NAME, "device-variation-subscription-item_headline")
        if len(offers) == 0:
            to_append[6]["offers"].append("No offer")
        for offer in offers:
            if len(offers) == 0:
                break
            else:
                to_append[6]["offers"].append(
                    offer.get_attribute("innerText"))

        smartphone_price_btn = driver.find_elements(
            By.CLASS_NAME, "js-step2-trigger")
        original_smartphone_price = driver.find_element(
            By.CLASS_NAME, "device-item-price-base").get_attribute("innerText").replace(" €", "")
        to_append[8]["original_smartphone_prices"].append(
            original_smartphone_price)
        print(original_smartphone_price)
        smartphone_prices = []

        # subscription_details = driver.find_elements(
        #     By.CLASS_NAME, "device-variation-subscription-item_details")
        # for detail in subscription_details:
        #     d = detail.get_attribute(
        #         "innerText").replace("  ", "").split("\n")
        #     det = []
        #     for element in d:
        #         if element != "":
        #             det.append(element)
        #     to_append[5]["subscription_details"].append(det)

        for subscription in range(len(subscriptions)):
            smartphone_price_btn[subscription].click()
            time.sleep(5)
            sub_container = driver.find_elements(
                By.CSS_SELECTOR, ".subscription-step-2_options.subscription-step-2_options--active > div")
            val = driver.find_elements(By.CLASS_NAME, "subscription-details__first")[subscription].get_attribute(
                "innerText").replace("\n\n", " ").replace("\n", " ")
            for sub in sub_container:
                if sub.get_attribute("innerText").split("\n")[0] != "Without option":
                    print(subscriptions[subscription].get_attribute("innerText").split("\n")[0] + " - " +
                          sub.get_attribute("innerText").split("\n")[0])

                    subscrip = subscriptions[subscription].get_attribute("innerText").split(
                        "\n")[0] + " - " + sub.get_attribute("innerText").split("\n")[0]

                    fixed_price = driver.find_element(
                        By.CLASS_NAME, "js-subscription-step-2_price")
                    phone_price = driver.find_element(
                        By.CLASS_NAME, "js-subscription-mobile-step-2_price")

                    to_append[4]["subscriptions"].append(subscrip)
                    # to_append[5]["subscription_value_container"].append(val)
                    # to_append[5]["subscription_details"].append(
                    # #     ["No details given"])
                    # to_append[5]["monthly_prices"].append(
                    #     fixed_price.get_attribute("innerText").replace("€", ""))
                    # to_append[6]["original_monthly_prices"].append(
                    # "No original monthly price")
                    to_append[6]["offers"].append("No offer")
                    to_append[7]["smartphone_prices"].append(
                        phone_price.get_attribute("innerText").replace("€", ""))

            print(driver.find_element(
                By.CLASS_NAME, "js-subscription-mobile-step-2_price").get_attribute("innerText").replace("€", ""))
            smartphone_prices.append(driver.find_element(
                By.CLASS_NAME, "js-subscription-mobile-step-2_price").get_attribute("innerText").replace("€", ""))
            to_append[7]["smartphone_prices"].append(driver.find_element(
                By.CLASS_NAME, "js-subscription-mobile-step-2_price").get_attribute("innerText").replace("€", ""))
        print(smartphone_prices)

        mobile_phones.append(to_append)
        print(to_append)
        print("----------------------------------------------")

    for phone in mobile_phones:
        for storage_option in range(len(phone[3]["storage_options"])):
            for color in range(len(phone[2]["colors"][0])):
                for plan in range(len(phone[4]["subscriptions"])):
                    # for monthly_plan in range(len(phone[5]["monthly_prices"])):
                    # for detail in range(len(phone[5]["subscription_details"][plan])):
                    for period in range(len(phone[5]["commitment_periods"])):
                        for original_price in range(len(phone[8]["original_smartphone_prices"])):
                            csv_data.append((phone[0], phone[1], phone[2]["colors"][0]
                                            [color], phone[3]["storage_options"][storage_option], phone[4]["subscriptions"][plan], phone[5]["commitment_periods"][period], phone[6]["offers"][plan], phone[7]["smartphone_prices"][plan], phone[8]["original_smartphone_prices"][original_price]))

    writer(csv_headers, csv_data, csv_file)


scrape_tango()
