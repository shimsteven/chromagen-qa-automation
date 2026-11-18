import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

os.environ["SE_OFFLINE"] = "true"

# Team Leader Account Credentials
EMAIL = "shimsteven@gmail.com"
PASSWORD = "ABCabc123!"

# New user details
NEW_USER_NAME = "Juan Dela Cruz"
NEW_USER_EMAIL = "juan.delacruz2@gmail.com"
NEW_USER_ROLE = "Telemarketer"
NEW_USER_PASSWORD = "ABCabc123!"

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

try:
    print("Test Case TC-TL-003")
    print("-----------------------------------")

    # OPEN THE WEBSITE
    driver.get("https://sortrleaddistribution-client.onrender.com/")
    print("Website opened.")

    # ENTER EMAIL
    email_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_field.send_keys(EMAIL)
    print("Email entered.")

    # ENTER PASSWORD
    password_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_field.send_keys(PASSWORD)
    print("Password entered.")

    # CLICK LOG IN
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log In']"))
    )
    login_button.click()
    print("Log In button clicked.")

    # WAIT FOR DASHBOARD
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )
    print("Login successful.")

    # OPEN ADD NEW USER FORM
    add_lead_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Add New User']"))
    )
    add_lead_link.click()
    print("Opened add new user form.")
    print("Entering user credentials...")

    # Enter User Name
    fname_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Full Name"]')
        )
    )
    fname_box.clear()
    fname_box.send_keys(NEW_USER_NAME)

    # Enter User Email
    email_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="chromagen@sortr.com.au"]')
        )
    )
    email_box.clear()
    email_box.send_keys(NEW_USER_EMAIL)

    # Enter User Password
    password_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Enter unique password"]')
        )
    )
    password_box.clear()
    password_box.send_keys(NEW_USER_PASSWORD)

    # Select User Role
    dropdown = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//label[contains(., 'Select Role')]/following-sibling::div//div[@role='combobox']"
        ))
    )
    ActionChains(driver).move_to_element(dropdown).click_and_hold().release().perform()

    option = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            f"//ul[@role='listbox']//li[@role='option'][contains(normalize-space(), '{NEW_USER_ROLE}')]"
        ))
    )
    option.click()

    # Click Add New User Button
    submit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_btn.click()
    print("Add New User submitted.")
    print("Waiting for success message...")
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='New User Added Successfully!']")
        )
    )
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # Open Users page
    add_lead_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Users']"))
    )
    add_lead_link.click()
    print("Opened users page.")
    print("Verifying user credentials...")

    # Wait for the users page heading
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Chromagen Staffs']"))
    )

    # Find the Search input
    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Search"]')
        )
    )

    # Search for the existing lead
    search_box.clear()
    search_box.send_keys(NEW_USER_NAME)

    # Verify that the user appears in the results
    matching_user_name = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[normalize-space()='{NEW_USER_NAME}']")
        )
    )
    matching_user_email = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//*[normalize-space()='{NEW_USER_EMAIL}']")
            )
        )
    matching_user_role = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//*[normalize-space()='{NEW_USER_ROLE}']")
            )
        )

    print("-----------------------------------")
    print("TEST TC-TL-003 PASSED - User found!")
    print("User name:", matching_user_name.text)
    print("User email:", matching_user_email.text)
    print("User role:", matching_user_role.text)
    print("The search returned the expected user.")
    print("-----------------------------------")

except TimeoutException:
    print()
    print("------------------------------------------")
    print("TEST TC-TL-003 FAILED")
    print("------------------------------------------")
    print("A required element did not appear in time.")
    print("Current URL:", driver.current_url)
    print("Check the last printed step for the failure.")
    print("------------------------------------------")

except Exception as error:
    print()
    print("------------------------------------------")
    print("TEST TC-TL-003 FAILED")
    print("------------------------------------------")
    print("Error type:", type(error).__name__)
    print("Error details:", error)
    print("------------------------------------------")

finally:
    input("\nPress Enter to close the browser...")
    driver.quit()