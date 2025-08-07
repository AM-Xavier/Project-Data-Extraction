from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_experimental_option(name="detach", value=True)
options.add_argument('--headless')

website = "https://store.steampowered.com/"
path = r"C:\Users\aless\Downloads\chromedriver-win64\chromedriver.exe"

service = Service(executable_path=path)
driver = webdriver.Chrome(options=options, service=service)
driver.get(website)

wait = WebDriverWait(driver, 10)

offers_table = wait.until(EC.element_to_be_clickable((By.ID, "tab_specials_content_trigger")))
offers_table.click()

wait.until(EC.presence_of_element_located((By.ID, "tab_specials_content")))

time.sleep(1)

containers = driver.find_elements(By.CSS_SELECTOR, "#tab_specials_content .tab_item")

game_titles = []
game_prices = []
game_discounts = []
game_links = []

for container in containers:
    try:
        title = container.find_element(By.CLASS_NAME, "tab_item_name").text
        link = container.get_attribute("href")
        
        try:
            discount = container.find_element(By.CLASS_NAME, "discount_pct").text
        except:
            discount = "N/A"
        
        try:
            price = container.find_element(By.CLASS_NAME, "discount_prices").text
        except:
            price = "N/A"
    
        game_titles.append(title)
        game_links.append(link)
        game_discounts.append(discount)
        game_prices.append(price)
        
        print(f"Obtained: {title} | {discount} | {price}")
        
    except Exception as e:
        print(f"Game {container +1} ignored: {e}")

steam_dict = {'Game Title': game_titles,
            'Game Discount': game_discounts,
            'Game Price': game_prices,
            'Game Link': game_links}

df_steam = pd.DataFrame(steam_dict)
df_steam.to_csv('offers.csv', index=False)

driver.quit()