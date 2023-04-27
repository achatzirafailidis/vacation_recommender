from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import csv
import re

options = Options()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)

about_list = []
review_list = []
best_time_list = []
with open('/home/alex/Spiced/final_project/data/term_list.csv', newline='') as f:
    reader = csv.reader(f)
    a = 1
    for row in reader: 
        print(row[0])
        elem = driver.get(f"https://www.tripadvisor.com/Search?q={str(row[0]).lower()}")

        #elements = driver.find_element(By.CSS_SELECTOR, ".ui_column.is-12.content-column.result-card.result-card-default")
        #elements.click()
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui_columns.is-mobile.result-content-columns')))
            driver.execute_script("arguments[0].click();", element)
        except:
            continue

        #element.get_attribute('innerHTML')
        time.sleep(5)
        url_list = []
        print(a)
        driver.switch_to.window(driver.window_handles[1])
        url_list.append(driver.current_url)

        url = url_list[0]
        #print(url)

        if "WebPresentation_AttractionAboutSectionGroup" in driver.page_source:
            print("yes")


            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            tag = soup.select_one('[data-automation="WebPresentation_AttractionAboutSectionGroup"]')

            text_list = [text for text in tag.find_all(string=True) if text.parent.name != "span"]
            about_list.append([row[0],text_list[1]])
            tag_reviews = soup.select_one('[id="REVIEWS"]')

            text_list_reviews = [text for text in tag_reviews.find_all(string=True) if text.parent.name == "span"]
            indices = [i for i, x in enumerate(text_list_reviews) if x == "Read more"]
            
            for i in indices:
                review_list.append([row,text_list_reviews[i-1]])

            time.sleep(5)
        else:
            print('no')

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            #print(type(html))
            try:
                #print('in')
                about = soup.select_one('[data-test-target="geo-description"]')
                city_about = [text for text in about.find_all(string=True) if text.parent.name != "span"]

                #print("in1")
                for i in city_about:
                    #print(about_list)
                    if "About" not in i:
                        about_list.append([row[0],i])
                    else:
                        pass


                #print("in2")

                ids = driver.find_element(By.XPATH,'/html/body/div[1]/main/div[7]/div[1]/div[2]/div/div')
                text = ids.get_attribute('innerHTML')
                href = re.search('href="([^#]*)', text)
                #print(href.group(1))

                elem = driver.get(f"https://www.tripadvisor.com{href.group(1)}")

                #print(driver.current_url)
                html_get_there = driver.page_source
                #print(html_get_there)
                soup_get_there = BeautifulSoup(html_get_there, 'html.parser')

                best_tim_tag = soup_get_there.find_all("p", class_="FnIWP ggYOs z")

                best = [text for text in soup_get_there.find_all(string=True) if text.parent.name != "span"]
                
                for i in best:
                    if i=='When is the best time to visit?':
                        #print(best[best.index(i)+1])
                        best_time_list.append([row[0], best[best.index(i)+1]])
                    else:
                        pass
            except:
                pass
        a += 1
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

print(review_list)
driver.quit()

with open('/home/alex/Spiced/final_project/data/reviews_trip_advisor.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(review_list)

with open('/home/alex/Spiced/final_project/data/about_trip_advisor.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(about_list)

with open('/home/alex/Spiced/final_project/data/best_time_trip_advisor.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(best_time_list)

print("Finished")
