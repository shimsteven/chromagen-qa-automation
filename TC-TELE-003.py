import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)
import re

os.environ["SE_OFFLINE"] = "true"
MOD = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

# Telemarketer account credentials
EMAIL = "shimmanaloto2@gmail.com"
PASSWORD = "ABCabc123!"

WEBSITE = "https://sortrleaddistribution-client.onrender.com/"

LEAD_NAME = "Gardern Atrium Restaurant"
LEAD_TYPE = "Cafe"
LEAD_PHONE_NUMBER = "61269216411"
LEAD_STREET_ADDRESS = "Ground/22-30 kincaid St."
LEAD_CITY = "Wagga Wagga"
LEAD_POSTCODE = "2650"
LEAD_EMAIL_ADDRESS = "pavilion.res@mantra.com.au"
LEAD_CALL_DISPOSITION = "Warm Lead"
LEAD_REMARKS = "10 liters of tank. Call back later @.11 a.m"

# ==========================================
# STEP 1: OPEN CHROME
# ==========================================

options = webdriver.ChromeOptions()

# Open Chrome in a maximized window
options.add_argument("--start-maximized")

# Set browser zoom to 80%
options.add_argument("--force-device-scale-factor=0.8")

driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 60)
short_wait = WebDriverWait(driver, 10)

def clear(field):
    field.click()
    field.send_keys(MOD + "a")
    field.send_keys(Keys.BACKSPACE)

try:
    print("Test Case TC-TELE-003")
    print("-----------------------------------")

    # ==========================================
    # STEP 2: OPEN APPLICATION
    # ==========================================

    print("Step 1: Opening application...")
    driver.get(WEBSITE)

    # ==========================================
    # STEP 3: LOG IN
    # ==========================================

    print("Step 2: Logging in...")

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    ).send_keys(EMAIL)

    driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(PASSWORD)

    driver.find_element(By.XPATH, "//button[normalize-space()='Log In']").click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("TEST PASSED: Login successful.")

    # ==========================================
    # STEP 4: OPEN LEADS PAGE
    # ==========================================

    print("Step 3: Opening Leads page...")

    leads_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Leads']"))
    )

    leads_link.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='ASSIGNED LEADS']")
        )
    )

    print("Leads page opened.")

    # Click edit icon on the first lead
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="row"][data-rowindex]'))
    )
    rows = driver.find_elements(By.CSS_SELECTOR, 'div[role="row"][data-rowindex]')
    n_leads = len(rows)

    edit_button = None
    try:
        icon = rows[0].find_element(
            By.CSS_SELECTOR, 'svg[data-testid="EditIcon"]'
        )

        edit_button = icon.find_element(By.XPATH, "./ancestor::button[1]")

    except Exception:
        print("Icon not found inside the target row.")
        print("Searching all email icons on the page...")

    driver.execute_script(
        "arguments[0].scrollIntoView(" "{block: 'center', inline: 'center'});",
        edit_button,
    )
    wait.until(lambda d: edit_button.is_displayed() and edit_button.is_enabled())

    try:
        edit_button.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", edit_button)

    # Edit fields
    for i in range(0, 9):
        # ENTER LEAD NAME
        name_field = wait.until(EC.visibility_of_element_located((By.NAME, "name")))
        clear(name_field)
        if i != 0: name_field.send_keys(LEAD_NAME)

        # SELECT LEAD TYPE
        # Locate the Material UI dropdown.
        type_dropdown = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                '.MuiModal-root:not(.MuiPopover-root) [role="combobox"]'
            ))
        )
        type_dropdown.click()

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
        if i != 2: phone_field.send_keys(LEAD_PHONE_NUMBER)

        # ENTER STREET ADDRESS
        street_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "streetaddress"))
        )
        clear(street_field)
        if i != 3: street_field.send_keys(LEAD_STREET_ADDRESS)

        # ENTER CITY
        city_field = wait.until(EC.visibility_of_element_located((By.NAME, "city")))
        clear(city_field)
        if i != 4: city_field.send_keys(LEAD_CITY)

        # ENTER POSTCODE
        postcode_field = wait.until(EC.visibility_of_element_located((By.NAME, "postcode")))
        clear(postcode_field)
        if i != 5: postcode_field.send_keys(LEAD_POSTCODE)

        # ENTER LEAD EMAIL
        lead_email_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "emailaddress"))
        )
        clear(lead_email_field)
        if i != 6: lead_email_field.send_keys(LEAD_EMAIL_ADDRESS)

        # SELECT CALL DISPOSITION
        modal_selector = '.MuiModal-root:not(.MuiPopover-root) [role="combobox"]'

        def second_combobox(d):
            els = d.find_elements(By.CSS_SELECTOR, modal_selector)
            return els[1] if len(els) > 1 else False

        disposition_dropdown = wait.until(second_combobox)
        wait.until(EC.element_to_be_clickable(disposition_dropdown)).click()

        if i != 7:
            option_locator = (By.CSS_SELECTOR, f'li[role="option"][data-value="{LEAD_CALL_DISPOSITION}"]')
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
                    LEAD_CALL_DISPOSITION
                    in [
                        element.get_attribute("data-value")
                        for element in d.find_elements(
                            By.CSS_SELECTOR, '[role="option"][aria-selected="true"]'
                        )
                    ]
                    or LEAD_CALL_DISPOSITION
                    in [
                        element.get_attribute("value")
                        for element in d.find_elements(By.CSS_SELECTOR, '[role="combobox"]')
                    ]
                    or any(
                        LEAD_CALL_DISPOSITION in (element.text or "")
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

        # ENTER LEAD REMARKS
        lead_remarks_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "remarks"))
        )
        clear(lead_remarks_field)
        if i != 8: lead_remarks_field.send_keys(LEAD_REMARKS)


        # STEP 15: SUBMIT THE FORM
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        submit_button.click()
        print(f"Lead form iteration {i} completed.")

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(), 'Updating, please wait...')]")))
            save_started = True
        except TimeoutException:
            save_started = False

        accepted = False
        if save_started:
            try:
                WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[normalize-space()='Update Successfully!']")))
                accepted = True
            except TimeoutException:
                accepted = False
                pass

        if accepted:
            raise Exception(f"[Bug] Iteration {i}: ACCEPTED.")

    print("------------------------------------------")
    print("TEST TC-TELE-003 PASSED")
    print("Login successful.")
    print("Confirm sucessfully rejected all invalid lead forms")
    print("------------------------------------------")

except TimeoutException:
    print()
    print("------------------------------------------")
    print("TEST TC-TELE-003 FAILED")
    print("------------------------------------------")
    print("A required element did not appear in time.")
    print("Current URL:", driver.current_url)
    print("Check the last printed step for the failure.")
    print("------------------------------------------")

except Exception as error:
    print()
    print("------------------------------------------")
    print("TEST TC-TELE-003 FAILED")
    print("------------------------------------------")
    print("Error type:", type(error).__name__)
    print("Error details:", error)
    print("------------------------------------------")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
