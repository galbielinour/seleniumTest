#!/usr/bin/env python
# coding: utf-8

# In[125]:


import os  
import shutil  
import tempfile
import importlib
import pandas as pd
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
from datetime import datetime
import time
  
os.environ["HOME"] = "/workspace"  
  
# Function to kill all Chrome processes  
def kill_all_chrome_sessions():  
    os.system("pkill chrome") 


def delete_user_data(user_data_dir):  
    if os.path.exists(user_data_dir):  
        shutil.rmtree(user_data_dir)  

kill_all_chrome_sessions()  
  
user_data_dir = tempfile.mkdtemp()  
print(f"Using user data directory: {user_data_dir}")  
  
delete_user_data(user_data_dir)  
  
options = Options()  
options.add_argument("--headless")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  
options.add_argument(f"--user-data-dir={user_data_dir}")  

service = Service(executable_path='/workspace/chromedriver-linux64/chromedriver')


# In[126]:


df = pd.read_csv('fastsearch.csv', delimiter=';')
df


# In[129]:


##2

def set_zoom_level(driver, zoom_level):
    driver.execute_script(f"document.body.style.zoom='{zoom_level}';")

zoom_level = "90%" 

screenshot_directory = "screenshots/"

try:  
    driver = webdriver.Chrome(service=service, options=options)  
    driver.set_window_size(1920, 1020)
  
    # Open a webpage  
    driver.get("https://webticketing/login")
    set_zoom_level(driver, zoom_level)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "j_username")))
    driver.find_element(By.ID, "j_username").send_keys("username") 
    wait.until(EC.presence_of_element_located((By.ID, "j_password")))
    driver.find_element(By.ID,  "j_password").send_keys("password") 
    wait.until(EC.presence_of_element_located((By.NAME, "submit")))
    driver.find_element(By.NAME, "submit").click()

    driver.get("https://webticketing/fastsearch")
    print(driver.title)
    i=0
    for index, row in df.iterrows():
        try:
            field_name = row['field']
            sample_value = row['sample']
            column_name = row['column']
            driver.refresh()
            wait.until(EC.presence_of_element_located((By.ID, field_name)))
            driver.find_element(By.ID, field_name).send_keys(sample_value) 
            wait.until(EC.presence_of_element_located((By.ID, "showAllFilter")))
            driver.find_element(By.ID, "showAllFilter").click()
            time.sleep(5)

            # Get the scrollable table element
            table = driver.find_element(By.XPATH, "//div[contains(@class, 'dt-scroll-body')]")
            
            while True:
                try:
                    # Check if the column is visible
                    column_xpath = f"//span[@class='dt-column-title' and text()='{column_name}']"
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, column_xpath)))
                    print("Scrolled to the element:", WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, column_xpath))).text)
                    break  # Exit the loop if the column is found
                except:
                    # Scroll right
                    driver.execute_script("arguments[0].scrollLeft += 500;", table)  # Adjust the scroll amount as needed
                    time.sleep(1)  # Wait for the scroll to take effect
            try:
                # time.sleep(5)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_filename = f"{i}_screenshot_{column_name}_{timestamp}.png"
                screenshot_path = os.path.join(screenshot_directory, screenshot_filename)
                driver.save_screenshot(screenshot_path)
                i=+1
                print(f"Screenshot saved: {screenshot_path}")                   
                                    
                wait.until(EC.presence_of_element_located((By.ID, "clearFilter")))
                driver.find_element(By.ID, "clearFilter").click()
                driver.refresh()
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("Capture process stopped manually.")
            # except TimeoutException:
            #     print("Span element not found within the specified time.")
            # except NoSuchElementException:
            #     print("Span element not found on the page.")

        except:
            print(row['field']+"ERROR")
    
    print(driver.title)
finally:  
    driver.quit()


# In[ ]:




