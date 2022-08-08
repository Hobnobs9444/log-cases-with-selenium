# Script to login to lifelong learning and submit an anaesthetic logbook entry
# Aim to integrate with google sheets version of logbook for batch entry

# Functions for:
# - yes / no box select
# - multiple choice box select
# - dropdown box click and send keys

from termios import TIOCPKT_DOSTOP
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from secrets import email, password

# Form variable placeholders
'''placeholders for spreadsheet variables'''
dd = "7"
mm = "8"
yyyy = "2022"
time = "night"
# hospital = "Peterborough"
reference = ""
pt_age = "27"
age_units = "years"
asa = 1
day = False
priority = 'immediate'
speciality = 'general'
operation = 'laparotomy'
second = False
supervision = 'immediate'
supervisor = 'consultant'
teaching = 'none'
mode = 'GA ETT RSI'
regional = False
procdeure = False
event = False
notes = ''

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
'''if searched by XPATH contains rather than ID, time variable could be used alone for function'''
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
driver.find_element(By.ID, "dynamic_personal-reference").send_keys(reference)

# Age
'''TODO needs XPATH searches for years, months, days - f' strings don't work ?XPATH as variable conditional on age_units'''
driver.find_element(By.ID, "dynamic_patient-age").send_keys(pt_age)
driver.find_element(By.ID, "select2-dynamic_patient-age-units-container").click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@id, 'years')]")))
driver.find_element(By.XPATH, "//li[contains(@id, 'years')]").click() # path only valid after opening dropdown

# ASA
if asa == 1:
    driver.find_element(By.ID, "dynamic[asa]_asa-1").click()
elif asa == 2:
    driver.find_element(By.ID, "dynamic[asa]_asa-2").click()
elif asa == 3:
    driver.find_element(By.ID, "dynamic[asa]_asa-3").click()
elif asa == 4:
    driver.find_element(By.ID, "dynamic[asa]_asa-4").click()
elif asa == 5:
    driver.find_element(By.ID, "dynamic[asa]_asa-5").click()
elif asa == 'donor':
    driver.find_element(By.ID, "dynamic[asa]_donor").click()
else:
    print('asa error')

# Day case
if day == True:
    driver.find_element(By.ID, "dynamic[day-case]_yes").click()
else:
    driver.find_element(By.ID, "dynamic[day-case]_no").click()

# Priotiry
if priority == 'immediate':
    driver.find_element(By.ID, "dynamic[priority]_immediate").click()
elif priority == 'urgent':
    driver.find_element(By.ID, "dynamic[priority]_urgent").click()
elif priority == 'expedited':
    driver.find_element(By.ID, "dynamic[priority]_expedited").click()
elif priority == 'elective':
    driver.find_element(By.ID, "dynamic[priority]_elective").click()
else:
    print('Priority error')

# Primary speciality
driver.find_element(By.ID, "select2-dynamic_primary-specialty-container").click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'select2')]")))
speciality_search = driver.find_element(By.XPATH, "//input[contains(@class, 'select2')]")
speciality_search.send_keys(speciality)
speciality_search.send_keys(Keys.RETURN)

# Operation
op_ID = f"select2-dynamic_operation-{speciality}-container"
driver.find_element(By.ID, op_ID).click()
op_search = driver.find_element(By.XPATH, "//input[contains(@class, 'select2')]")
op_search.send_keys(operation)
op_search.send_keys(Keys.RETURN)

# Second speciality
'''TODO needs send keys for second speciality if present'''
if second == True:
    driver.find_element(By.ID, "dynamic[was-there-a-secondary-specialty]_yes").click()
else:
    driver.find_element(By.ID, "dynamic[was-there-a-secondary-specialty]_no").click()

# Supervision
if supervision == 'immediate':
    driver.find_element(By.ID, "dynamic[supervision]_immediate").click()
elif supervision == 'local':
    driver.find_element(By.ID, "dynamic[supervision]_local").click()
elif supervision == 'distant':
    driver.find_element(By.ID, "dynamic[supervision]_distant").click()
elif supervision == 'solo':
    driver.find_element(By.ID, "dynamic[supervision]_solo").click()
else:
    print('supervision error')

# Supervisor
if supervision == 'solo':
    pass
else:
    if supervisor == 'consultant':
        driver.find_element(By.ID, "dynamic[supervisor]_consultant").click()
    elif supervisor == 'sas':
        driver.find_element(By.ID, "dynamic[supervisor]_sas").click()
    elif supervisor == 'senior-trainee':
        driver.find_element(By.ID, "dynamic[supervisor]_senior-trainee").click()
    elif supervisor == 'other':
        driver.find_element(By.ID, "dynamic[supervisor]_other").click()


# Teaching
'''TODO teaching strings will need formating to match spreadsheet'''
if teaching == 'trainee':
    driver.find_element(By.ID, "dynamic[teaching]_trainee").click()
elif teaching == 'consultant-career-grade':
    driver.find_element(By.ID, "dynamic[teaching]_consultant-career-grade").click()
elif teaching == 'medical-student':
    driver.find_element(By.ID, "dynamic[teaching]_medical-student").click()
elif teaching == 'allied-health-professional':
    driver.find_element(By.ID, "dynamic[teaching]_allied-health-professional").click()
elif teaching == 'novice':
    driver.find_element(By.ID, "dynamic[teaching]_novice").click()
elif teaching == 'none':
    driver.find_element(By.ID, "dynamic[teaching]_none").click()
else:
    print('teaching error')

# Mode of anaesthesia
driver.find_element(By.ID, "select2-dynamic_anaesthesia-mode-container").click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'select2')]")))
mode_search = driver.find_element(By.XPATH, "//input[contains(@class, 'select2')]")
mode_search.send_keys(mode)
mode_search.send_keys(Keys.RETURN)

# Regional
'''TODO needs regional entry variables'''
if regional == True:
    driver.find_element(By.ID, "dynamic[regional]_yes").click()
else:
    driver.find_element(By.ID, "dynamic[regional]_no").click()

# Procedure
if procdeure == True:
    driver.find_element(By.ID, "dynamic[procedure]_yes").click()
else:
    driver.find_element(By.ID, "dynamic[procedure]_no").click()

# Significant event
if event == True:
    driver.find_element(By.ID, "dynamic[significant-event]_yes").click()
else:
    driver.find_element(By.ID, "dynamic[significant-event]_no").click()

# Notes
'''TODO can't locate box element'''
# driver.find_element(By.XPATH, "//*[@data-id='dynamic_notes']").send_keys(notes)

# Submit log
driver.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()
