
from re import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from secrets import email, password

def login(username, password):
    '''Create driver, navigate to LLP website and login'''
    # Create firefox webdriver instance
    global driver
    driver = webdriver.Firefox()

    # Navigate to lifelong learning landing page
    driver.get("https://lifelong.rcoa.ac.uk")
    assert "RCoA Lifelong Learning" in driver.title

    # Login to website
    address = driver.find_element(By.NAME, "email")
    address.clear()
    address.send_keys(username)

    pswd = driver.find_element(By.NAME, "password")
    pswd.clear()
    pswd.send_keys(password)
    pswd.send_keys(Keys.RETURN)

    # Wait for logbook dashboard to load
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard-logbook"))
        )

def date(dd, mm, yyyy):
    '''enter date of case'''
    driver.find_element(By.ID, "dynamic_date_dd").clear().send_keys(dd)
    driver.find_element(By.ID, "dynamic_date_mm").clear().send_keys(mm)
    driver.find_element(By.ID, "dynamic_date_yyyy").clear().send_keys(yyyy)

def check_box(cat, vars):
    '''check all boxes in a category (cat) defined in list vars, for yes/no selections use this as the var'''
    for var in vars:
        xpath = f"//input[contains(@name, '{cat}') and contains(@id, '{var}')]"
        driver.find_element(By.XPATH, xpath).click()

def search_box(cat, var):
    '''Open dropdown, enter text and confirm'''
    dropdown_xpath = f"//span[contains(@id, 'select2-dynamic_{cat}')"
    driver.find_element(By.XPATH, dropdown_xpath).click()
    search_box = driver.find_element(By.XPATH, "//input[contains(@class, 'select2')]")
    search_box.send_keys(var, Keys.RETURN)

def text_box():
    #TODO
    pass

# Form variable placeholders
# TODO: These could a dictionary to be looped over? Divide by required entry function?

dd = "7"
mm = "8"
yyyy = "2022"
time = "night"
# hospital = "Peterborough"
reference = ""
pt_age = "27"
age_units = "years"
asa = 1
day = 'no'
priority = 'immediate'
speciality = 'general'
operation = 'laparotomy'
second = 'no'
second_spec = None
supervision = 'immediate'
supervisor = 'consultant'
teaching = 'none'
mode = 'GA ETT RSI'
regional = 'no'
procedure = 'no'
event = 'no'
notes = ''

def main():
    '''Log into LLP, open logbook form, fill in with variables above and submit'''
    login(email, password)
    driver.get("https://lifelong.rcoa.ac.uk/form/logbook-case-anaesthetic/create-submission")

    # Fills in the form 
    date(dd, mm, yyyy)
    check_box('time', time)

    # plain text box entry - could be another function I guess
    driver.find_element(By.ID, "dynamic_personal-reference").send_keys(reference)
    driver.find_element(By.ID, "dynamic_patient-age").send_keys(pt_age)

    # select age units - special case dropdown box
    age_units_xpath = f"//li[contains(@id, '{age_units}')]"
    driver.find_element(By.ID, "select2-dynamic_patient-age-units-container").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, age_units_xpath)))
    driver.find_element(By.XPATH, age_units_xpath).click() # path only valid after opening dropdown

    # More data entry
    check_box('asa', asa)
    check_box('day-case', day)
    check_box('priority', priority)
    search_box('speciality', speciality)
    search_box('operation', operation)
    check_box('secondary-speciality', second)

    if second == 'yes':
        search_box('secondary-speciality', second_spec)
    else:
        pass

    if supervision == 'solo':
        pass
    else:
        check_box('supervision', supervision)

    check_box('teaching', teaching)
    search_box('anaesthesia-mode', mode)

    # these 3 need conditional entry adding
    check_box('regional', regional)
    check_box('procedure', procedure)
    check_box('significant-event', event)

    # submit the form
    driver.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()
