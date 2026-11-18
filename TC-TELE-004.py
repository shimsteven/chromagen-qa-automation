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

LEAD_CALL_DISPOSITION = "Warm Lead"

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
    print("Test Case TC-TELE-004")
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

    # Check if 10 leads are assigned.
    EXPECTED_LEAD_COUNT = 10
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="row"][data-rowindex]'))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, 'div[role="row"][data-rowindex]')
    lead_ids = [r.get_attribute("data-id") for r in rows]
    assert len(lead_ids) == EXPECTED_LEAD_COUNT, f"Expected 10 leads, found {len(lead_ids)}"

    NEW_REMARK_PREFIX = "Auto-test"
    for i, lead_id in enumerate(lead_ids):
        new_remark = f"{NEW_REMARK_PREFIX} {lead_id}"
        print(f"Editing {lead_id}...")

        row = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'div[role="row"][data-id="{lead_id}"]')
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", row)

        # Click the edit button
        edit_btn = row.find_element(
            By.XPATH,
            ".//*[@data-testid='EditIcon']/ancestor::*[self::button or @role='button'][1]",
        )
        try:
            edit_btn.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click()", edit_btn)

        # SELECT CALL DISPOSITION
        modal_selector = '.MuiModal-root:not(.MuiPopover-root) [role="combobox"]'

        def second_combobox(d):
            els = d.find_elements(By.CSS_SELECTOR, modal_selector)
            return els[1] if len(els) > 1 else False

        disposition_dropdown = wait.until(second_combobox)
        wait.until(EC.element_to_be_clickable(disposition_dropdown)).click()

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

        # Replace phone number
        PHONE_NUMBER = 61269310073
        phone_field = wait.until(EC.visibility_of_element_located((By.NAME, "phonenumber")))
        clear(phone_field)
        phone_field.send_keys(PHONE_NUMBER)

        # Add remarks
        lead_remarks_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "remarks"))
        )
        clear(lead_remarks_field)
        lead_remarks_field.send_keys(new_remark)

        # Click Submit
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        submit_button.click()
        print(f"Submit button clicked for iteration {i}.")

        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[normalize-space()='Update Successfully!']")))
        import time
        time.sleep(5)

    # Check if 10 new leads were assigned
    time.sleep(5)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="row"][data-rowindex]'))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, 'div[role="row"][data-rowindex]')
    actual = len(rows)
    assert actual == EXPECTED_LEAD_COUNT, f"Expected {EXPECTED_LEAD_COUNT} leads, found {actual}"

    footer = driver.find_element(
        By.CSS_SELECTOR, '.MuiTablePagination-displayedRows'
    ).text
    assert footer.strip().endswith(f"of {EXPECTED_LEAD_COUNT}"), f"Footer says: {footer}"
    print(f"Verified: {actual} leads assigned.")

    print("------------------------------------------")
    print("TEST TC-TELE-004 PASSED")
    print("Login successful.")
    print("Confirm sucessfully assigned 10 leads")
    print("------------------------------------------")

except TimeoutException:
    print()
    print("------------------------------------------")
    print("TEST TC-TELE-004 FAILED")
    print("------------------------------------------")
    print("A required element did not appear in time.")
    print("Current URL:", driver.current_url)
    print("Check the last printed step for the failure.")
    print("------------------------------------------")

except Exception as error:
    print()
    print("------------------------------------------")
    print("TEST TC-TELE-004 FAILED")
    print("------------------------------------------")
    print("Error type:", type(error).__name__)
    print("Error details:", error)
    print("------------------------------------------")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
