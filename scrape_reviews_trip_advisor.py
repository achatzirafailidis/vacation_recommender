from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import csv

options = Options()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)

review_list = []

review_nr = [i for i in range(10,201) if i%10==0]

with open('/home/alex/Spiced/final_project/data/term_list.csv', newline='') as f:
    reader = csv.reader(f)
    a = 1
    for row in reader: 
        print(row[0])
        url = f"https://www.tripadvisor.com/Search?q={str(row[0]).lower()}"
        elem = driver.get(url)
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui_columns.is-mobile.result-content-columns')))
            driver.execute_script("arguments[0].click();", element)
        except:
            continue
        time.sleep(5)
        url_list = []
        driver.switch_to.window(driver.window_handles[1])
        url_list.append(driver.current_url)

        url = url_list[0]

        if "WebPresentation_AttractionAboutSectionGroup" in driver.page_source:
            print("yes")
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            tag_reviews = soup.select_one('[id="REVIEWS"]')

            text_list_reviews = [text for text in tag_reviews.find_all(string=True) if text.parent.name == "span"]
            #range = [x]
            indices = [i for i, x in enumerate(text_list_reviews) if x == "Read more"]
            
            for i in indices:
                review_list.append([row[0],text_list_reviews[i-1]])

            attraction_url = driver.current_url
            for x in review_nr:
                new_url = (attraction_url).replace("Reviews",f"Reviews-or{x}")
                #print(new_url)
                time.sleep(3)
                elem = driver.get(new_url)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                tag_reviews = soup.select_one('[id="REVIEWS"]')

                text_list_reviews = [text for text in tag_reviews.find_all(string=True) if text.parent.name == "span"]
                #range = [x]
                indices = [i for i, x in enumerate(text_list_reviews) if x == "Read more"]
                
                for i in indices:
                    review_list.append([row[0],text_list_reviews[i-1]])
                
                print(len(review_list))
                with open('/home/alex/Spiced/final_project/data/extended_reviews_trip_advisor.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(review_list)
        else:
            pass
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(a)
        a += 1

driver.quit()

