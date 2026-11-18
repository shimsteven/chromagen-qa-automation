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
    print("Test Case TC-TELE-001")
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
    actual = len(rows)
    assert actual == EXPECTED_LEAD_COUNT, f"Expected {EXPECTED_LEAD_COUNT} leads, found {actual}"

    footer = driver.find_element(
        By.CSS_SELECTOR, '.MuiTablePagination-displayedRows'
    ).text
    assert footer.strip().endswith(f"of {EXPECTED_LEAD_COUNT}"), f"Footer says: {footer}"
    print(f"Verified: {actual} leads assigned.")

    print("------------------------------------------")
    print("TEST TC-TELE-001 PASSED")
    print("Login successful.")
    print("Confirm sucessfully assigned 10 leads")
    print("------------------------------------------")

except TimeoutException:
    print()
    print("------------------------------------------")
    print("TEST TC-TELE-001 FAILED")
    print("------------------------------------------")
    print("A required element did not appear in time.")
    print("Current URL:", driver.current_url)
    print("Check the last printed step for the failure.")
    print("------------------------------------------")

except Exception as error:
    print()
    print("------------------------------------------")
    print("TEST TC-TELE-001 FAILED")
    print("------------------------------------------")
    print("Error type:", type(error).__name__)
    print("Error details:", error)
    print("------------------------------------------")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
