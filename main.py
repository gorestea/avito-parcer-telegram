import json
import datetime
import time
from tkinter import N
import openpyxl
# import sqlite3
from hashlib import new
from asyncio.windows_events import NULL
from this import d
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

options = webdriver.ChromeOptions()
options.add_argument("start-maximazed")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options)

stealth(                                         # модуль скрытности
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win64",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

pages = int()

def get_pages(url):
    global pages
    pages = []
    for page in range(1, 2):
        url1 = f"{url}"
        driver.get(url1)

        blocks = driver.find_element(By.CLASS_NAME, "pagination-root-Ntd_O")
        posts = blocks.find_elements(By.CLASS_NAME, "pagination-item-JJq_j")
        for i in posts:
            pages.append(i.text)
        pages = int(pages[-2]) + 1
    time.sleep(5)


def get_all_to_excel(url):
    global pages
    news_dict = {}
    news_dict['tovary'] = []
    news = {}
    print(pages)

    for page in range(1, pages):
        url1 = f"{url}"
        url2 = url1.replace("{page}", str(page))
        driver.get(url2)

        blocks = driver.find_element(By.CLASS_NAME, "items-items-kAJAg")
        posts = blocks.find_elements(By.CLASS_NAME, "iva-item-root-_lk9K")

        for post in posts:
            if not post.find_elements(By.CLASS_NAME, "iva-item-descriptionStep-C0ty1"):
                continue
            if not post.find_element(By.CLASS_NAME, "iva-item-titleStep-pdebR").find_element(By.TAG_NAME, "a").get_attribute("href"):
                break
            else:
                title_link = post.find_element(By.CLASS_NAME, "iva-item-titleStep-pdebR").find_element(By.TAG_NAME, "a").get_attribute("href")
                comment = post.find_element(By.CLASS_NAME, "iva-item-descriptionStep-C0ty1").text
                title = post.find_element(By.CLASS_NAME, "iva-item-titleStep-pdebR").find_element(By.TAG_NAME, "a").text
                price = post.find_element(By.CLASS_NAME, "iva-item-priceStep-uq2CQ").find_element(By.TAG_NAME, "span").text.replace(" ", ".")
                if price == "Цена.не.указана":
                    price = post.find_element(By.CLASS_NAME, "iva-item-priceStep-uq2CQ").find_element(By.TAG_NAME, "span").text.replace(" ", ".")
                    price = price.replace(".", " ")
                else:
                    price = post.find_element(By.CLASS_NAME, "iva-item-priceStep-uq2CQ").find_element(By.TAG_NAME, "span").text.replace(" ", ".")
                    price = price.replace(".₽", "")
                    price = int(price.replace(".", ""))
                date_time = datetime.datetime.now()
                d = str(date_time)[:19]
                date = post.find_element(By.CLASS_NAME, "date-text-KmWDf").text
                data = {
                    "title": title,
                    "url": title_link,
                    "price": price,
                    "comment": comment,
                    "date_append": d, 
                    "date": date
                }

                news_dict["tovary"].append(data)

                with open("news_dict.json", "w", encoding="utf-8") as file:
                    json.dump(news_dict, file, indent=4, ensure_ascii=False)
                
                news[title_link] = {
                    "title": title,
                    "url": title_link,
                    "price": price,
                    "comment": comment,
                    "date_append": d,
                    "date": date
                }

                with open("dict.json", "w", encoding="utf-8") as file:
                    json.dump(news, file, indent=4, ensure_ascii=False)

def check_update(url):
    with open("dict.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    fresh_news = {}
    for page in range(1, 2):
        url1 = f"{url}"
        driver.get(url1)

        blocks = driver.find_element(By.CLASS_NAME, "items-items-kAJAg")
        posts = blocks.find_elements(By.CLASS_NAME, "iva-item-root-_lk9K")
        for post in posts:
            title_link = post.find_element(By.CLASS_NAME, "iva-item-titleStep-pdebR").find_element(By.TAG_NAME, "a").get_attribute("href")
            if title_link in news_dict:
                continue
            if not post.find_elements(By.CLASS_NAME, "iva-item-descriptionStep-C0ty1"):
                continue
            else:
                comment = post.find_element(By.CLASS_NAME, "iva-item-descriptionStep-C0ty1").text
                title = post.find_element(By.CLASS_NAME, "iva-item-titleStep-pdebR").find_element(By.TAG_NAME, "a").text
                price = post.find_element(By.CLASS_NAME, "iva-item-priceStep-uq2CQ").find_element(By.TAG_NAME, "span").text.replace(" ", ".")
                date_time = datetime.datetime.now()
                d = str(date_time)[:19]
                date = post.find_element(By.CLASS_NAME, "date-text-KmWDf").text

                news_dict[title_link] = {
                    "title": title,
                    "url": title_link,
                    "price": price,
                    "comment": comment,
                    "date_append": d,
                    "date": date
                }
                
                fresh_news[title_link] = {
                    "title": title,
                    "url": title_link,
                    "price": price,
                    "comment": comment,
                    "date_append": d, 
                    "date": date
                }

                with open("dict.json", "w", encoding="utf-8") as file:
                    json.dump(news_dict, file, indent=4, ensure_ascii=False)

        return fresh_news


def main():
    get_pages()
    print(type(pages))
    # get_all_to_excel()
    # print(check_update())

if __name__ == '__main__':
    main()