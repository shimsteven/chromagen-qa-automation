import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

os.environ["SE_OFFLINE"] = "true"
MOD = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
HEADLESS = False

# Lead gen specialist account credentials
EMAIL = "josephperez20064567@gmail.com"
PASSWORD = "newpass123"

# Lead details
LEAD_NAME = "Sample Cafe"
LEAD_TYPE = "Cafe"
PHONE = "0412345678"
STREET = "123 Emerald St., Brgy. Baliti"
CITY = "City of San Fernando"
POSTCODE = "2000"
LEAD_EMAIL = "samplecafe@gmail.com"

# ==========================================
# STEP 1: OPEN CHROME
# ==========================================

options = webdriver.ChromeOptions()

# Open Chrome in a maximized window
options.add_argument("--start-maximized")

# Set browser zoom to 80%
options.add_argument("--force-device-scale-factor=0.8")

if HEADLESS:
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 60)

def clear(field):
    field.click()
    field.send_keys(MOD + "a")
    field.send_keys(Keys.BACKSPACE)

try:
    print("Test Case TC-LEADGEN-002")
    print("-----------------------------------")

    # ==========================================
    # STEP 2: OPEN THE WEBSITE
    # ==========================================

    driver.get("https://sortrleaddistribution-client.onrender.com/")
    print("Website opened.")

    # ==========================================
    # STEP 3: ENTER EMAIL
    # ==========================================

    email_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_field.send_keys(EMAIL)
    print("Email entered.")

    # ==========================================
    # STEP 4: ENTER PASSWORD
    # ==========================================

    password_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_field.send_keys(PASSWORD)
    print("Password entered.")

    # ==========================================
    # STEP 5: CLICK LOG IN
    # ==========================================

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log In']"))
    )
    login_button.click()
    print("Log In button clicked.")

    # ==========================================
    # STEP 6: WAIT FOR DASHBOARD
    # ==========================================

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )
    print("Login successful.")

    # ==========================================
    # STEP 7: OPEN ADD NEW LEAD
    # ==========================================

    add_lead_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Add New Lead']"))
    )
    add_lead_link.click()
    print("Add New Lead page opened.")

    for i in range(0, 7):
        # ENTER LEAD NAME
        name_field = wait.until(EC.visibility_of_element_located((By.NAME, "name")))
        clear(name_field)
        if i != 0: name_field.send_keys(LEAD_NAME)

        # SELECT LEAD TYPE
        # Locate the Material UI dropdown.
        type_dropdown = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="combobox"]'))
        )
        type_dropdown.click()


        # Locate the exact option using its data-value.
        if i != 1:
            option_locator = (By.CSS_SELECTOR, f'li[role="option"][data-value="{LEAD_TYPE}"]')
            type_option = wait.until(EC.visibility_of_element_located(option_locator))

            # Scroll the option into the visible area of the dropdown.
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", type_option
            )

            # Wait briefly for the dropdown to finish scrolling,
            # then try a normal Selenium click first.
            wait.until(EC.element_to_be_clickable(option_locator)).click()

            wait.until(
                lambda d: (
                    LEAD_TYPE
                    in [
                        element.get_attribute("data-value")
                        for element in d.find_elements(
                            By.CSS_SELECTOR, '[role="option"][aria-selected="true"]'
                        )
                    ]
                    or LEAD_TYPE
                    in [
                        element.get_attribute("value")
                        for element in d.find_elements(By.CSS_SELECTOR, '[role="combobox"]')
                    ]
                    or any(
                        LEAD_TYPE in (element.text or "")
                        for element in d.find_elements(By.CSS_SELECTOR, '[role="combobox"]')
                    )
                )
            )
        else:
            option_locator = (By.CSS_SELECTOR, 'li[role="option"][data-value=""]')
            type_option = wait.until(EC.visibility_of_element_located(option_locator))

            # Scroll the option into the visible area of the dropdown.
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", type_option
            )

            # Wait briefly for the dropdown to finish scrolling,
            # then try a normal Selenium click first.
            wait.until(EC.element_to_be_clickable(option_locator)).click()


        # ENTER PHONE NUMBER
        phone_field = wait.until(EC.visibility_of_element_located((By.NAME, "phonenumber")))
        clear(phone_field)
        if i != 2: phone_field.send_keys(PHONE)

        # ENTER STREET ADDRESS
        street_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "streetaddress"))
        )
        clear(street_field)
        if i != 3: street_field.send_keys(STREET)

        # ENTER CITY
        city_field = wait.until(EC.visibility_of_element_located((By.NAME, "city")))
        clear(city_field)
        if i != 4: city_field.send_keys(CITY)

        # ENTER POSTCODE
        postcode_field = wait.until(EC.visibility_of_element_located((By.NAME, "postcode")))
        clear(postcode_field)
        if i != 5: postcode_field.send_keys(POSTCODE)

        # ENTER LEAD EMAIL
        lead_email_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "emailaddress"))
        )
        clear(lead_email_field)
        if i != 6: lead_email_field.send_keys(LEAD_EMAIL)


        # STEP 15: SUBMIT THE FORM
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        submit_button.click()
        print(f"Lead form iteration {i} completed.")

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(), 'Saving, please wait')]")))
            save_started = True
        except TimeoutException:
            save_started = False

        accepted = False
        if save_started:
            try:
                WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[normalize-space()='New lead added!']")))
                accepted = True
            except TimeoutException:
                accepted = False
                pass

        if accepted:
            raise Exception(f"[Bug] Iteration {i}: ACCEPTED.")

    print("-----------------------------------")
    print("TEST TC-LEADGEN-002 PASSED - all 7 invalid leads were rejected")
    print("-----------------------------------")

except TimeoutException:
    print("-----------------------------------")
    print("SCENARIO 2: TEST FAILED")
    print("A required element did not appear in time.")
    print("Check the last progress message above.")
    print("Current URL:", driver.current_url)
    print("-----------------------------------")

except Exception as error:
    print("-----------------------------------")
    print("SCENARIO 2: TEST FAILED")
    print("An unexpected error occurred:")
    print(error)
    print("-----------------------------------")

finally:
    input("\nPress Enter to close the browser...")
    driver.quit()
