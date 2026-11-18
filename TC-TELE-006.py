import os
import platform
import time
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
EMAIL = "shimmanaloto@gmail.com"
PASSWORD = "ABCabc123!"

# TEST DATA
LEAD_NAME = "Dressed by Jackie"
EXPECTED_RECIPIENT = "mikeandjac@live.com.au"

SUBJECT_TEMPLATE = (
    "Congratulations! You're Eligible for a Free Hot Water System Upgrade"
)

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
    print("Test Case TC-TELE-006")
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

    # ==========================================
    # STEP 5: SEARCH FOR TARGET LEAD
    # ==========================================

    print("Step 4: Searching for target lead...")

    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Search"]')
        )
    )

    search_box.clear()
    search_box.send_keys(LEAD_NAME)

    target_row_xpath = "//*[@role='row' and " f".//*[normalize-space()='{LEAD_NAME}']]"

    target_row = wait.until(
        EC.visibility_of_element_located((By.XPATH, target_row_xpath))
    )

    print("TEST PASSED: Target lead found.")

    # ==========================================
    # STEP 6: VERIFY RECIPIENT
    # ==========================================

    print("Step 5: Verifying recipient...")

    if EXPECTED_RECIPIENT.lower() not in target_row.text.lower():
        raise Exception(
            "Expected recipient was not found in the target lead row. "
            "Email was not sent."
        )

    print("Recipient verified:", EXPECTED_RECIPIENT)

    # ==========================================
    # STEP 7: LOCATE EMAIL ICON
    # ==========================================

    print("Step 6: Locating email icon...")

    email_button = None

    # First, try finding the icon inside the target row.
    try:
        icon = target_row.find_element(
            By.CSS_SELECTOR, 'svg[data-testid="AttachEmailIcon"]'
        )

        email_button = icon.find_element(By.XPATH, "./ancestor::button[1]")

    except Exception:
        print("Icon not found inside the target row.")
        print("Searching all email icons on the page...")

    # Fallback: search globally and identify the action
    # associated with the expected recipient.
    if email_button is None:
        icons = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'svg[data-testid="AttachEmailIcon"]')
            )
        )

        print("Email icons found:", len(icons))

        for icon in icons:
            try:
                candidate = icon.find_element(By.XPATH, "./ancestor::button[1]")
            except Exception:
                try:
                    candidate = icon.find_element(By.XPATH, "./ancestor::a[1]")
                except Exception:
                    continue

            surrounding_html = driver.execute_script(
                """
                let element = arguments[0];
                const recipient = arguments[1];

                for (let i = 0; i < 10 && element; i++) {
                    if (
                        (element.innerText || "").includes(recipient)
                    ) {
                        return element.outerHTML;
                    }

                    element = element.parentElement;
                }

                return "";
                """,
                candidate,
                EXPECTED_RECIPIENT,
            )

            if surrounding_html:
                email_button = candidate
                break

        if email_button is None:
            raise Exception(
                "Could not safely identify the email action " "for the target lead."
            )

    for i in range(0, 4):
        # STEP 8: CLICK EMAIL ICON
        driver.execute_script(
            "arguments[0].scrollIntoView(" "{block: 'center', inline: 'center'});",
            email_button,
        )
        wait.until(lambda d: email_button.is_displayed() and email_button.is_enabled())
        try:
            email_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", email_button)

        # STEP 9: WAIT FOR EMAIL MODAL
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[normalize-space()='Send An Email']")
            )
        )

        # STEP 10: VERIFY MODAL RECIPIENT
        recipient_field_xpath = f"//input[@value='{EXPECTED_RECIPIENT}']"
        recipient_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, recipient_field_xpath))
        )
        if recipient_field.get_attribute("value") != EXPECTED_RECIPIENT:
            raise Exception("Recipient mismatch. Email was not sent.")

        from_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, f"//input[@name='from']"))
        )
        clear(from_field)
        if i != 0:
            from_field.send_keys(EMAIL)

        to_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, f"//input[@name='to']"))
        )
        if (i == 1):
            clear(to_field)

        if i != 2:
            # STEP 11: SELECT SUBJECT TEMPLATE
            subject_dropdown = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[normalize-space()='Subject']"
                        "/ancestor::div[contains(@class,'MuiFormControl-root')]"
                        "//*[self::div or self::input]"
                        "[@role='combobox' or @aria-haspopup='listbox']",
                    )
                )
            )
            subject_dropdown.click()

            # Handle the apostrophe in "You're" safely.
            subject_option_xpath = (
                "//*[@role='option' and normalize-space(.)="
                "concat('Congratulations! You', \"'\", "
                "'re Eligible for a Free Hot Water System Upgrade')]"
            )
            subject_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, subject_option_xpath))
            )
            subject_option.click()

            if i != 3:
                # STEP 12: WAIT FOR TEMPLATE TEXT
                text_area_xpath = "//textarea[@name='text']"
                text_area = wait.until(
                    EC.visibility_of_element_located((By.XPATH, text_area_xpath))
                )
                wait.until(
                    lambda d: bool(
                        d.find_element(By.XPATH, text_area_xpath).get_attribute("value").strip()
                    )
                )
                message_text = text_area.get_attribute("value")

                # STEP 13: DEFINE PLACEHOLDER VALUES
                # Replace these example values with approved information.
                PLACEHOLDER_VALUES = {
                    "[Customer's Name]": "Ivan Soriano",
                    "[Your Contact Information]": "1300 000 000",
                    "[Your Website URL]": "https://example.com",
                    "[Telemarketer Name]": "BSIT 3D",
                }

                # STEP 14: EDIT TEMPLATE PLACEHOLDERS
                for placeholder, replacement in PLACEHOLDER_VALUES.items():
                    if placeholder not in message_text:
                        raise Exception(f"Expected placeholder not found: {placeholder}")
                    message_text = message_text.replace(placeholder, replacement)

                # STEP 15: UPDATE EMAIL MESSAGE
                text_area = wait.until(
                    EC.visibility_of_element_located((By.XPATH, text_area_xpath))
                )
                # Select and replace the entire textarea content.
                text_area.click()
                text_area.send_keys(Keys.CONTROL, "a")
                text_area.send_keys(Keys.BACKSPACE)
                text_area.send_keys(message_text)

                # Read the actual value back from the form.
                updated_message = text_area.get_attribute("value") or ""

                # STEP 16: VERIFY PLACEHOLDERS
                remaining_placeholders = re.findall(r"\[[^\]]+\]", updated_message)
                if remaining_placeholders:
                    raise Exception(
                        "Unedited placeholders remain: "
                        + ", ".join(remaining_placeholders)
                        + ". Email was NOT sent."
                    )

            else:
                text_area = wait.until(
                    EC.visibility_of_element_located((By.XPATH, text_area_xpath))
                )

                # Select and replace the entire textarea content.
                text_area.click()
                text_area.send_keys(Keys.CONTROL, "a")
                text_area.send_keys(Keys.BACKSPACE)

        else:
            text_area = wait.until(
                EC.visibility_of_element_located((By.XPATH, text_area_xpath))
            )

            # Select and replace the entire textarea content.
            text_area.click()
            text_area.send_keys(Keys.CONTROL, "a")
            text_area.send_keys(Keys.BACKSPACE)
            text_area.send_keys("This is a test message.")

        # LOCATE SEND BUTTON
        send_button_xpath = "//button[@type='submit' and normalize-space()='Send']"
        send_button = short_wait.until(
            EC.presence_of_element_located((By.XPATH, send_button_xpath))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", send_button
        )
        if not send_button.is_enabled():
            raise Exception("Send button is disabled. Email was not sent.")

        # SEND EMAIL

        # Wait briefly for the actual Send button to be clickable.
        send_button = short_wait.until(
            EC.element_to_be_clickable((By.XPATH, send_button_xpath))
        )

        try:
            send_button.click()

        except Exception as click_error:
            send_button = driver.find_element(By.XPATH, send_button_xpath)
            driver.execute_script("arguments[0].click();", send_button)


        # VERIFY APPLICATION REJECTION
        print("Verifying email rejection...")
        EXPECTED_ERROR = "Please complete the following required fields:"
        try:
            success_message = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//*[contains(normalize-space(.), \"{EXPECTED_ERROR}\")]")
                ))

            print("Validation error detected.")
            print(f"Iteration {i} passed.")
            time.sleep(1)

        except TimeoutException:
            raise Exception(f"[Bug] Validation error was not detected at iteration {i}. Email might have been accepted")

        ActionChains(driver).send_keys(Keys.ESCAPE).perform()


    # ==========================================
    # STEP 21: FINAL SUMMARY
    # ==========================================

    print("------------------------------------------")
    print("TEST TC-TELE-006 PASSED")
    print("Login successful.")
    print("Target lead verified.")
    print("Recipient checked.")
    print("Subject template selected.")
    print("Placeholders replaced and verified.")
    print("Send action attempted.")
    print("Confirm successful rejection in the application.")
    print("------------------------------------------")

except TimeoutException:
    print()
    print("------------------------------------------")
    print("TEST TC-TELE-006 FAILED")
    print("------------------------------------------")
    print("A required element did not appear in time.")
    print("Current URL:", driver.current_url)
    print("Check the last printed step for the failure.")
    print("------------------------------------------")

except Exception as error:
    print()
    print("------------------------------------------")
    print("TEST TC-TELE-006 FAILED")
    print("------------------------------------------")
    print("Error type:", type(error).__name__)
    print("Error details:", error)
    print("------------------------------------------")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
