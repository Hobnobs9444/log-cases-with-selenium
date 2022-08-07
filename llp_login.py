from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from secrets import email, password

# Create firefox webdriver instance
driver = webdriver.Firefox()

# Navigate to lifelong learning landing page
driver.get("https://lifelong.rcoa.ac.uk")
assert "RCoA Lifelong Learning" in driver.title

# Login to website
address = driver.find_element(By.NAME, "email")
address.clear()
address.send_keys(email)

pswd = driver.find_element(By.NAME, "password")
pswd.clear()
pswd.send_keys(password)
pswd.send_keys(Keys.RETURN)

# Wait for logbook dashboard to load
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dashboard-logbook"))
    )

# Go to logbook submission
driver.get("https://lifelong.rcoa.ac.uk/form/logbook-case-anaesthetic/create-submission")

# Form variable placeholders
'''placeholders for spreadsheet variables'''
dd = "7"
mm = "8"
yyyy = "2022"
time = "night"
# hospital = "Peterborough"
# refernce = ""
pt_age = "27"
age_units = "Years"

# Fill date
day = driver.find_element(By.ID, "dynamic_date_dd")
day.clear()
day.send_keys(dd)

month = driver.find_element(By.ID, "dynamic_date_mm")
month.clear()
month.send_keys(mm)

year = driver.find_element(By.ID, "dynamic_date_yyyy")
year.clear()
year.send_keys(yyyy)

# Select time
morning = driver.find_element(By.ID, "dynamic_time_morning-0800-1300")
afternoon = driver.find_element(By.ID, "dynamic_time_afternoon-1300-1800")
evening = driver.find_element(By.ID, "dynamic_time_evening-1800-2200")
night = driver.find_element(By.ID, "dynamic_time_night-2200-0800")

if time == "night":
    night.click()
elif time == "morning":
    morning.click()
elif time == "evening":
    evening.click()
elif time == "afternoon":
    afternoon.click()
else:
    print("invalid time")

# Change Hosptial
# TODO

# Personal Reference
# TODO

# Age
driver.find_element(By.ID, "dynamic_patient-age").send_keys(pt_age)

# Age units
'''failing due to Element <option> could not be scrolled into view'''
# find_age_units = driver.find_element(By.ID, "dynamic_patient-age-units")
# select_age_units = Select(find_age_units)
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dynamic_patient-age-units")))
# select_age_units.select_by_visible_text("Years")

'''fails as element is not reachable by keyboard'''
# driver.find_element(By.ID, "select2-dynamic_patient-age-units-container").click()
# driver.find_element(By.ID, "select2-dynamic_patient-age-units-results").send_keys(Keys.ARROW_DOWN)

age_units = driver.find_element(By.ID, "select2-dynamic_patient-age-units-container")
years = driver.find_element(By.XPATH, "//option[contains(@value, 'years')]") # path valid but doesn't do anything...
action = ActionChains(driver)
action.move_to_element(age_units).click()
action.move_to_element(years).click()

# XPATH to dropdown: //*[@id="select2-dynamic_patient-age-units-results"]
# XPATH to years (nlsn is dynamic): //*[@id="select2-dynamic_patient-age-units-result-nlsn-years"]
# Search just for years?: //*[contains(@id, 'years')]
