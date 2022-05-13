import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import date
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
csv_headers = ("Device ID", "Memory", "Subscription", "Available For Online Sale", "Price Without Subscription", "Final Price",
               "Color ID", "Color Code", "Article ZID", "Article ID", "Color Available For Online Sale", "Root Code", "Brand", "Model", "Package ID", "Commitment ID", "Commitment Duration", "Phone Option Price", "Phone Option Code")
datime = str(date.today())
csv_file = f"1_Letz-Compare-Scraping/post_site/post_mobiles/post_phones_{datime}.csv"
csv_data = []
data = []


def writer(header, data, filename):
    with open(filename, "w+", newline="") as csvfile:
        phones = csv.writer(csvfile)
        phones.writerow(header)
        for x in data:
            phones.writerow(x)


def post_scraper_5G():
    global csv_data, data
    driver.get(
        "https://www.post.lu/en/particuliers/mobile/5gpower-avec-telephone")
    accept_cookies = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    if accept_cookies != []:
        accept_cookies[0].click()
        time.sleep(3)

    time.sleep(5)
    plans = driver.find_elements(
        By.CLASS_NAME, "card.card-mobile-phone-plan")
    plan_names = driver.find_elements(
        By.CSS_SELECTOR, ".card-mobile-phone-plan > .card-wrapper > h4")
    mobile_phones = []

    previous_plan = driver.find_element(By.CLASS_NAME, "swiper-button-prev")
    while "swiper-button-disabled" not in previous_plan.get_attribute("class"):
        previous_plan.click()

    buttons = driver.find_elements(By.CLASS_NAME, "custom-control-input")
    time.sleep(5)

    for plan in range(len(plans)):
        plan_name = plan_names[plan].get_attribute("innerText")
        script = """XMLHttpRequest.prototype.realSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function(value) {
    this.addEventListener("progress", function(e){
        console.log(e.target.responseURL)
        if(e.target.responseURL.indexOf("https://api.post.lu/services/phones-catalog-api/devices-best-offer") == 0 && e.target.responseText.indexOf("deviceId")!==-1){
            try{
                localStorage.setItem("devicesJSON", e.target.responseText)
            }
            catch(err){
                console.log(err);
            }
        }
        else{
            console.log(e.target.responseURL);
        }
    }, false);
    this.realSend(value);
    };"""
        buttons[plan].click()
        time.sleep(5)
        page = driver.execute_script("return window.location.href")
        driver.get(page)
        driver.execute_script(script)
        time.sleep(5)
        driver.execute_script(script)
        time.sleep(35)
        arr = driver.execute_script(
            "return localStorage.getItem('devicesJSON')")
        print(arr)
        time.sleep(5)

        for key in (json.loads(arr))["offers"]:
            to_append = []
            to_append.append({"deviceID": key["device"]["deviceId"]})
            to_append.append({"memory": key["device"]["memory"]})
            to_append.append(
                {"Subscription": plan_name})
            to_append.append(
                {"availableForOnlineSale": key["device"]["availableForOnlineSale"]})
            to_append.append(
                {"priceWithoutSubscription": key["device"]["priceWithoutSubscription"]["price"]})
            to_append.append(
                {"finalPrice": key["device"]["finalPrice"]["price"]})
            to_append.append({"colorID": []})
            to_append.append({"colorCode": []})
            to_append.append({"articleZID": []})
            to_append.append({"articleID": []})
            to_append.append({"colorAvailableForOnlineSale": []})
            to_append.append(
                {"rootCode": key["device"]["rootFeatures"]["rootCode"]})
            to_append.append(
                {"brand": key["device"]["rootFeatures"]["brand"]})
            to_append.append(
                {"model": key["device"]["rootFeatures"]["model"]})
            to_append.append(
                {"packageId": key["packageCommitment"]["packageId"]})
            to_append.append(
                {"commitmentId": key["packageCommitment"]["commitmentId"]})
            to_append.append(
                {"commitmentDuration": key["packageCommitment"]["commitmentDuration"]})
            to_append.append(
                {"phoneOptionPrice": key["phoneOption"]["price"]["price"]})
            to_append.append(
                {"phoneOptionCode": key["phoneOption"]["code"]})

            for reference in key["device"]["deviceReferences"]:
                to_append[6]["colorID"].append(reference["color"]["id"])
                to_append[7]["colorCode"].append(reference["color"]["code"])
                to_append[8]["articleZID"].append(reference["articleZId"])
                to_append[9]["articleID"].append(reference["articleId"])
                to_append[10]["colorAvailableForOnlineSale"].append(
                    reference["availableForOnlineSale"])

            mobile_phones.append(to_append)
            print("-----------------------------------------------------------")

        validator = []
        for phone in mobile_phones:
            for color in range(len(phone[6]["colorID"])):
                if (phone[0]["deviceID"], phone[1]
                        ["memory"], phone[2]["Subscription"], phone[3]["availableForOnlineSale"], phone[4]["priceWithoutSubscription"], phone[5]["finalPrice"], phone[6]["colorID"][color], phone[7]["colorCode"][color], phone[8]["articleZID"][color], phone[9]["articleID"][color], phone[10]["colorAvailableForOnlineSale"][color], phone[11]["rootCode"], phone[12]["brand"], phone[13]["model"], phone[14]["packageId"], phone[15]["commitmentId"], phone[16]["commitmentDuration"], phone[17]["phoneOptionPrice"], phone[18]["phoneOptionCode"]) in data:

                    continue
                if (phone[0]["deviceID"], phone[1]
                        ["memory"], phone[2]["Subscription"], phone[3]["availableForOnlineSale"], phone[4]["priceWithoutSubscription"], phone[5]["finalPrice"], phone[6]["colorID"][color], phone[7]["colorCode"][color], phone[8]["articleZID"][color], phone[9]["articleID"][color], phone[10]["colorAvailableForOnlineSale"][color], phone[11]["rootCode"], phone[12]["brand"], phone[13]["model"], phone[14]["packageId"], phone[15]["commitmentId"], phone[16]["commitmentDuration"], phone[17]["phoneOptionPrice"], phone[18]["phoneOptionCode"]) in validator:
                    continue
                else:
                    validator.append((phone[0]["deviceID"], phone[1]
                                      ["memory"], phone[2]["Subscription"], phone[3]["availableForOnlineSale"], phone[4]["priceWithoutSubscription"], phone[5]["finalPrice"], phone[6]["colorID"][color], phone[7]["colorCode"][color], phone[8]["articleZID"][color], phone[9]["articleID"][color], phone[10]["colorAvailableForOnlineSale"][color], phone[11]["rootCode"], phone[12]["brand"], phone[13]["model"], phone[14]["packageId"], phone[15]["commitmentId"], phone[16]["commitmentDuration"], phone[17]["phoneOptionPrice"], phone[18]["phoneOptionCode"]))
                    data.append((phone[0]["deviceID"], phone[1]
                                 ["memory"], phone[2]["Subscription"], phone[3]["availableForOnlineSale"], phone[4]["priceWithoutSubscription"], phone[5]["finalPrice"], phone[6]["colorID"][color], phone[7]["colorCode"][color], phone[8]["articleZID"][color], phone[9]["articleID"][color], phone[10]["colorAvailableForOnlineSale"][color], phone[11]["rootCode"], phone[12]["brand"], phone[13]["model"], phone[14]["packageId"], phone[15]["commitmentId"], phone[16]["commitmentDuration"], phone[17]["phoneOptionPrice"], phone[18]["phoneOptionCode"]))

        driver.get(
            "https://www.post.lu/en/particuliers/mobile/5gpower-avec-telephone")
        time.sleep(5)
        buttons = driver.find_elements(By.CLASS_NAME, "custom-control-input")
        time.sleep(3)
        previous_plan = driver.find_element(
            By.CLASS_NAME, "swiper-button-prev")
        while "swiper-button-disabled" not in previous_plan.get_attribute("class"):
            previous_plan.click()
        next_button = driver.find_element(By.CLASS_NAME, "swiper-button-next")
        plan_names = driver.find_elements(
            By.CSS_SELECTOR, ".card-mobile-phone-plan > .card-wrapper > h4")

        for clicks in range(plan+1):
            if "swiper-button-disabled" not in next_button.get_attribute("class"):
                next_button.click()
        time.sleep(3)


def post_scraper():
    global csv_data, data
    driver.get(
        "https://www.post.lu/en/particuliers/mobile/scoubido-avec-telephone")
    accept_cookies = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    if accept_cookies != []:
        accept_cookies[0].click()
        time.sleep(3)

    time.sleep(5)
    plans = driver.find_elements(
        By.CLASS_NAME, "card.card-mobile-phone-plan")
    plan_names = driver.find_elements(
        By.CSS_SELECTOR, ".card-mobile-phone-plan > .card-wrapper > h4")
    mobile_phones = []

    previous_plan = driver.find_element(By.CLASS_NAME, "swiper-button-prev")
    while "swiper-button-disabled" not in previous_plan.get_attribute("class"):
        previous_plan.click()

    buttons = driver.find_elements(By.CLASS_NAME, "custom-control-input")
    time.sleep(5)

    for plan in range(len(plans)):
        plan_name = plan_names[plan].get_attribute("innerText")
        script = """XMLHttpRequest.prototype.realSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function(value) {
    this.addEventListener("progress", function(e){
        console.log(e.target.responseURL)
        if(e.target.responseURL.indexOf("https://api.post.lu/services/phones-catalog-api/devices-best-offer") == 0 && e.target.responseText.indexOf("deviceId")!==-1){
            try{
                localStorage.setItem("devicesJSON", e.target.responseText)
            }
            catch(err){
                console.log(err);
            }
        }
        else{
            console.log(e.target.responseURL);
        }
    }, false);
    this.realSend(value);
    };"""
        buttons[plan].click()
        time.sleep(5)
        page = driver.execute_script("return window.location.href")
        driver.get(page)
        driver.execute_script(script)
        time.sleep(5)
        driver.execute_script(script)
        time.sleep(35)
        arr = driver.execute_script(
            "return localStorage.getItem('devicesJSON')")
        print(arr)
        time.sleep(5)
        for key in (json.loads(arr))["offers"]:
            to_append = []
            to_append.append({"deviceID": key["device"]["deviceId"]})
            to_append.append({"memory": key["device"]["memory"]})
            to_append.append(
                {"Subscription": plan_name})
            to_append.append(
                {"availableForOnlineSale": key["device"]["availableForOnlineSale"]})
            to_append.append(
                {"priceWithoutSubscription": key["device"]["priceWithoutSubscription"]["price"]})
            to_append.append(
                {"finalPrice": key["device"]["finalPrice"]["price"]})
            to_append.append({"colorID": []})
            to_append.append({"colorCode": []})
            to_append.append({"articleZID": []})
            to_append.append({"articleID": []})
            to_append.append({"colorAvailableForOnlineSale": []})
            to_append.append(
                {"rootCode": key["device"]["rootFeatures"]["rootCode"]})
            to_append.append(
                {"brand": key["device"]["rootFeatures"]["brand"]})
            to_append.append(
                {"model": key["device"]["rootFeatures"]["model"]})
            to_append.append(
                {"packageId": key["packageCommitment"]["packageId"]})
            to_append.append(
                {"commitmentId": key["packageCommitment"]["commitmentId"]})
            to_append.append(
                {"commitmentDuration": key["packageCommitment"]["commitmentDuration"]})
            to_append.append(
                {"phoneOptionPrice": key["phoneOption"]["price"]["price"]})
            to_append.append(
                {"phoneOptionCode": key["phoneOption"]["code"]})

            for reference in key["device"]["deviceReferences"]:
                to_append[6]["colorID"].append(reference["color"]["id"])
                to_append[7]["colorCode"].append(reference["color"]["code"])
                to_append[8]["articleZID"].append(reference["articleZId"])
                to_append[9]["articleID"].append(reference["articleId"])
                to_append[10]["colorAvailableForOnlineSale"].append(
                    reference["availableForOnlineSale"])

            mobile_phones.append(to_append)
            print("-----------------------------------------------------------")

        validator = []
        for phone in mobile_phones:
            for color in range(len(phone[6]["colorID"])):
                if (phone[0]["deviceID"], phone[1]
                        ["memory"], phone[2]["Subscription"], phone[3]["availableForOnlineSale"], phone[4]["priceWithoutSubscription"], phone[5]["finalPrice"], phone[6]["colorID"][color], phone[7]["colorCode"][color], phone[8]["articleZID"][color], phone[9]["articleID"][color], phone[10]["colorAvailableForOnlineSale"][color], phone[11]["rootCode"], phone[12]["brand"], phone[13]["model"], phone[14]["packageId"], phone[15]["commitmentId"], phone[16]["commitmentDuration"], phone[17]["phoneOptionPrice"], phone[18]["phoneOptionCode"]) in data:

                    continue
                if (phone[0]["deviceID"], phone[1]
                        ["memory"], phone[2]["Subscription"], phone[3]["availableForOnlineSale"], phone[4]["priceWithoutSubscription"], phone[5]["finalPrice"], phone[6]["colorID"][color], phone[7]["colorCode"][color], phone[8]["articleZID"][color], phone[9]["articleID"][color], phone[10]["colorAvailableForOnlineSale"][color], phone[11]["rootCode"], phone[12]["brand"], phone[13]["model"], phone[14]["packageId"], phone[15]["commitmentId"], phone[16]["commitmentDuration"], phone[17]["phoneOptionPrice"], phone[18]["phoneOptionCode"]) in validator:
                    continue
                else:
                    validator.append((phone[0]["deviceID"], phone[1]
                                      ["memory"], phone[2]["Subscription"], phone[3]["availableForOnlineSale"], phone[4]["priceWithoutSubscription"], phone[5]["finalPrice"], phone[6]["colorID"][color], phone[7]["colorCode"][color], phone[8]["articleZID"][color], phone[9]["articleID"][color], phone[10]["colorAvailableForOnlineSale"][color], phone[11]["rootCode"], phone[12]["brand"], phone[13]["model"], phone[14]["packageId"], phone[15]["commitmentId"], phone[16]["commitmentDuration"], phone[17]["phoneOptionPrice"], phone[18]["phoneOptionCode"]))
                    data.append((phone[0]["deviceID"], phone[1]
                                 ["memory"], phone[2]["Subscription"], phone[3]["availableForOnlineSale"], phone[4]["priceWithoutSubscription"], phone[5]["finalPrice"], phone[6]["colorID"][color], phone[7]["colorCode"][color], phone[8]["articleZID"][color], phone[9]["articleID"][color], phone[10]["colorAvailableForOnlineSale"][color], phone[11]["rootCode"], phone[12]["brand"], phone[13]["model"], phone[14]["packageId"], phone[15]["commitmentId"], phone[16]["commitmentDuration"], phone[17]["phoneOptionPrice"], phone[18]["phoneOptionCode"]))
        driver.get(
            "https://www.post.lu/en/particuliers/mobile/scoubido-avec-telephone")
        time.sleep(5)
        buttons = driver.find_elements(By.CLASS_NAME, "custom-control-input")
        time.sleep(3)
        previous_plan = driver.find_element(
            By.CLASS_NAME, "swiper-button-prev")
        while "swiper-button-disabled" not in previous_plan.get_attribute("class"):
            previous_plan.click()
        next_button = driver.find_element(By.CLASS_NAME, "swiper-button-next")
        plan_names = driver.find_elements(
            By.CSS_SELECTOR, ".card-mobile-phone-plan > .card-wrapper > h4")

        for clicks in range(plan+1):
            if "swiper-button-disabled" not in next_button.get_attribute("class"):
                next_button.click()
        time.sleep(3)


post_scraper_5G()
post_scraper()

for i, piece in enumerate(data):
    csv_data.append(piece)
writer(csv_headers, csv_data, csv_file)
