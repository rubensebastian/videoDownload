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

#restart range if breaks and delete entry if needed
#does the first page, then needs to move to the next page
for i in range(202,260):
    #known videos that don't work
    if i == 0:
        continue
    if i == 8:
        continue
    if i == 16:
        continue
    if i == 20:
        continue
    if i == 24:
        continue
    if i == 37:
        continue
    if i == 48:
        continue
    if i == 53:
        continue
    if i == 88:
        continue
    if i == 99:
        continue
    if i == 126:
        continue
    if i == 128:
        continue
    if i == 129:
        continue
    if i == 145:
        continue
    if i == 150:
        continue
    if i == 163:
        continue
    if i == 165:
        continue
    if i == 169:
        continue
    if i >= 173 and i <= 176:
        continue
    if i == 196:
        continue
    if i == 199:
        continue
    if i == 201:
        continue
    if i == 202:
        continue

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

    try:
        submit_finished_close = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.close")))
    except:
        print("couldn't close entry", i, ":", video_title)
        break
    submit_finished_close.click()
    
    close_button.click()
    print("successfully completed entry", i, ":", video_title)
    #refreshing the page entirely ensures selenium doesn't get confused on which element it's looking for
    driver.refresh()

driver.close()