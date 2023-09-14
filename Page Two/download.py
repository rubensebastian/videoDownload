from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://mediasite.capd.fsu.edu/Mediasite/Manage")

username = driver.find_element(By.ID, "UserName")
password = driver.find_element(By.ID, "Password")

username.clear()
password.clear()

username.send_keys("USERNAME")
password.send_keys("PASSWORD")
password.send_keys(Keys.RETURN)

geoset_folder = wait.until(EC.element_to_be_clickable((By.ID, '3bd4c40ce4104ba485945b9891cfeefd14')))
geoset_folder.click()

show_more = wait.until(EC.element_to_be_clickable((By.ID, "ToggleView")))
show_more.click()

time.sleep(3)

next_page = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
next_page.click()

#ensure all list items are loaded first
time.sleep(5)

for i in range(244,260):
    confirm_load = wait.until(EC.element_to_be_clickable((By.ID, "ToggleView")))
    video_list = driver.find_elements(By.ID, "Name")
    video_item = video_list[i]
    video_title = video_item.text

    video_item.click()
    close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "panel-close")))

    try:
        download_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "download-toolbar")))#if no download button is found, close out and continue
    except:
        close_button.click()
        print("couldn't download entry", i, ":", video_title)
        break
    download_button.click()
    
    try:
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary")))
    except:
        try:
            submit_close = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.close")))
            submit_close.click()
            close_button.click()
        except:
            print("couldn't submit entry", i, ":", video_title)
            break
    submit_button.click()
    
    close_button.click()
    print("successfully completed entry", i, ":", video_title)

    driver.refresh()

driver.close()