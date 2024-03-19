from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class FlatInfo:
    name: str
    images: list[str]
    price: str
    locality: str

    def __init__(self, name: str, images: list[str], price, locality):
        self.name = name
        self.images = images
        self.price = price
        self.locality = locality


class FlatScraper:
    driver: webdriver
    flats: list[FlatInfo]

    def __init__(self):
        self.flats = []

    def open_chrome_with_url(self, url):
        user_agent = "bot:srealityscraper"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(url)
        return True

    def scrapy_func(self):

        start_urls = ["https://www.sreality.cz/hledani/prodej/byty/"]

        #   each page has 20 records and we want 500 of them
        # for i in range(1, int(500 / 20)):
        for i in range(1, 3):
            start_urls.append(
                f"https://www.sreality.cz/hledani/prodej/byty/?strana={i}"
            )

        for url in start_urls:
            print(f"============== Stránka: {url} ==============")
            if not self.open_chrome_with_url(url):
                return False

            # try:
            #     main_content = self.driver.find_element(By.CLASS_NAME, "content-cover")
            # except:
            #     print("Table with tournaments was not found.")

            try:
                main_content = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "dir-property-list"))
                )
            except:
                print("Failed to get main content.")

            # print(main_content.get_attribute("innerHTML"))
            try:
                first_item = WebDriverWait(main_content, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "property.ng-scope"))
                )
            except:
                print("Failed to wait for first item.")

            items = main_content.find_elements(By.CLASS_NAME, "property.ng-scope")

            for item in items:
                title = (
                    item.find_element(By.CLASS_NAME, "name.ng-binding")
                    .get_attribute("textContent")
                    .strip()
                )

                try:
                    price = (
                        WebDriverWait(item, 10)
                        .until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, "price.ng-scope")
                            )
                        )
                        .get_attribute("textContent")
                        .strip()
                    )
                except:
                    print("Failed to wait for price and locality.")

                try:
                    locality = (
                        WebDriverWait(item, 10)
                        .until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, "locality.ng-binding")
                            )
                        )
                        .get_attribute("textContent")
                        .strip()
                    )
                except:
                    print("Failed to wait for price and locality.")

                image_items = item.find_elements(By.TAG_NAME, "img")
                print("price and locality")
                print(title)
                print(price)
                print(locality)

                images = []
                for img in image_items:
                    images.append(img.get_attribute("src"))

                self.flats.append(FlatInfo(title, images, price, locality))
            self.driver.close()
        return self.flats


if __name__ == "__main__":
    tm = FlatScraper()
    res = tm.scrapy_func()
    for item in res:
        print(item.name)
        print(item.images)
        print("--------------------------")
