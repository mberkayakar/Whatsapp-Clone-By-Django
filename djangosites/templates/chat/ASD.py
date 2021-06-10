from selenium import webdriver
import time

browser = webdriver.Chrome(executable_path=r"C:\Users\alica\PycharmProjects\pythonProject1\chromedriver.exe")
url = "https://www.mackolik.com/puan-durumu/almanya-bundesliga/2020-2021/fikstur/6by3h89i2eykc341oz7lv1ddd"
browser.get(url)
ssss = browser.find_element_by_class_name("widget-gameweek__selected-label")
sayac = 0
for harf in ssss.text:
    if harf == ".":
        break
    else:
        sayac += 1


def haftaverisi():
    print("\n", browser.find_element_by_class_name("widget-gameweek__selected-label").text, "\n")
    asd = browser.find_elements_by_class_name("p0c-competition-match-list__day")
    for item in asd:
        qwe = item.find_element_by_class_name("p0c-competition-match-list__title")
        sss = item.find_elements_by_class_name("p0c-competition-match-list__row")
        for asdddd in sss:
            asdddd.find_element_by_class_name("p0c-competition-match-list__match-content")
            print(qwe.text , asdddd.text.replace("\n"," "))


integer = int(ssss.text[:sayac]) - 1

for sasd in range(integer, 0, -1):
    buttonback = browser.find_element_by_xpath('//div[@class="widget-gameweek__arrow widget-gameweek__arrow--prev"]')
    browser.execute_script("arguments[0].click();", buttonback)
sayac = 0
for item in range(34):
    sayac += 1
    time.sleep(5)
    haftaverisi()
    if sayac == 34:
        break
    else:
        buttongo = browser.find_element_by_xpath('//div[@class="widget-gameweek__arrow widget-gameweek__arrow--next"]')
        browser.execute_script("arguments[0].click();", buttongo)