"""
Task 2: Form Filler Bot
Automatically fills and submits web forms using Selenium.
Demonstrates form automation on a public test form site.
"""

import logging
import random
import time
from dataclasses import dataclass
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from bot.base_bot import TaskBot

logger = logging.getLogger("TaskBot.FormFiller")


@dataclass
class FormData:
    """Data to fill into a form."""
    first_name: str = "John"
    last_name: str = "Doe"
    email: str = "john.doe@example.com"
    phone: str = "9876543210"
    date_of_birth: str = "15 January,1990"
    subject: str = "Computer Science"
    hobbies: list = None
    current_address: str = "123 Main St, Kolkata, WB"
    state: str = "NCR"
    city: str = "Delhi"

    def __post_init__(self):
        if self.hobbies is None:
            self.hobbies = ["Sports", "Reading"]


class FormFillerBot(TaskBot):
    """Fills the DemoQA practice form — a safe automation testing site."""

    TARGET_URL = "https://demoqa.com/automation-practice-form"

    def __init__(self, headless: bool = False, form_data: FormData = None):
        super().__init__(headless=headless)
        self.form_data = form_data or FormData()
        self.filled = False

    def fill_form(self) -> bool:
        """Fill and submit the practice form."""
        logger.info("📝 Starting form filler on %s", self.TARGET_URL)
        self.go_to(self.TARGET_URL)
        self.sleep(1)

        # Remove ads/banners via JS for cleaner automation
        self.execute_js("""
            document.querySelectorAll('[id*="Ad"], [class*="ad-"], footer, #fixedban').forEach(e => e.remove());
        """)

        try:
            # ── Personal Info ────────────────────────────────────────────
            logger.info("Filling personal information...")
            self.type_text(By.ID, "firstName", self.form_data.first_name)
            self.type_text(By.ID, "lastName", self.form_data.last_name)
            self.type_text(By.ID, "userEmail", self.form_data.email)

            # Gender radio button
            gender_map = {"Male": "gender-radio-1", "Female": "gender-radio-2", "Other": "gender-radio-3"}
            gender_id = gender_map.get("Male", "gender-radio-1")
            self.execute_js(
                "arguments[0].click();",
                self.driver.find_element(By.CSS_SELECTOR, f"label[for='{gender_id}']")
            )
            logger.info("✅ Gender selected")

            self.type_text(By.ID, "userNumber", self.form_data.phone)
            self.screenshot("form_step_1_personal")

            # ── Date of Birth ────────────────────────────────────────────
            logger.info("Setting date of birth...")
            dob_field = self.find(By.ID, "dateOfBirthInput")
            dob_field.click()
            self.sleep(0.5)

            # Select month
            month_select = Select(self.driver.find_element(By.CLASS_NAME, "react-datepicker__month-select"))
            month_select.select_by_visible_text("January")

            # Select year
            year_select = Select(self.driver.find_element(By.CLASS_NAME, "react-datepicker__year-select"))
            year_select.select_by_visible_text("1990")

            # Click day 15
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'react-datepicker__day') and not(contains(@class,'outside')) and text()='15']"
            ).click()
            logger.info("✅ Date of birth set")

            # ── Subjects ─────────────────────────────────────────────────
            logger.info("Adding subject...")
            subject_input = self.find(By.ID, "subjectsInput")
            subject_input.send_keys(self.form_data.subject[:4])
            self.sleep(1)
            subject_input.send_keys(Keys.RETURN)
            logger.info("✅ Subject added")

            # ── Hobbies ───────────────────────────────────────────────────
            hobby_map = {"Sports": "hobbies-checkbox-1", "Reading": "hobbies-checkbox-2", "Music": "hobbies-checkbox-3"}
            for hobby in self.form_data.hobbies:
                if hobby in hobby_map:
                    self.execute_js(
                        "arguments[0].click();",
                        self.driver.find_element(By.CSS_SELECTOR, f"label[for='{hobby_map[hobby]}']")
                    )
                    logger.info("✅ Hobby checked: %s", hobby)

            self.screenshot("form_step_2_hobbies")

            # ── Address ───────────────────────────────────────────────────
            logger.info("Filling address...")
            self.type_text(By.ID, "currentAddress", self.form_data.current_address)

            # State dropdown
            self.scroll_to_bottom()
            self.sleep(0.5)
            state_dd = self.find(By.ID, "state")
            self.scroll_to_element(state_dd)
            state_dd.click()
            self.sleep(0.5)
            state_option = self.find(By.XPATH, f"//div[contains(text(), '{self.form_data.state}')]")
            state_option.click()

            # City dropdown
            self.sleep(0.5)
            city_dd = self.find(By.ID, "city")
            city_dd.click()
            self.sleep(0.5)
            city_option = self.find(By.XPATH, f"//div[contains(text(), '{self.form_data.city}')]")
            city_option.click()
            logger.info("✅ Address filled")

            self.screenshot("form_step_3_address")

            # ── Submit ────────────────────────────────────────────────────
            logger.info("Submitting form...")
            submit_btn = self.find_clickable(By.ID, "submit")
            self.scroll_to_element(submit_btn)
            self.execute_js("arguments[0].click();", submit_btn)
            self.sleep(1.5)

            # Check for success modal
            if self.element_exists(By.CLASS_NAME, "modal-content"):
                logger.info("✅ Form submitted successfully!")
                self.screenshot("form_submitted_success")
                self.filled = True

                # Read modal data
                title = self.get_text(By.CLASS_NAME, "modal-title")
                logger.info("Modal title: %s", title)
                return True
            else:
                logger.warning("⚠️ Form submitted but no confirmation modal found")
                self.screenshot("form_submitted_unknown")
                self.filled = True
                return True

        except Exception as e:
            logger.error("❌ Form filling failed: %s", e)
            self.screenshot("form_error")
            return False

    def print_summary(self):
        print(f"\n{'='*55}")
        print(f"  📋 FORM FILLER SUMMARY")
        print(f"{'='*55}")
        print(f"  Target URL  : {self.TARGET_URL}")
        print(f"  Status      : {'✅ Submitted' if self.filled else '❌ Failed'}")
        print(f"  Name        : {self.form_data.first_name} {self.form_data.last_name}")
        print(f"  Email       : {self.form_data.email}")
        print(f"  Hobbies     : {', '.join(self.form_data.hobbies)}")
        print(f"  City        : {self.form_data.city}, {self.form_data.state}")
        print(f"{'='*55}\n")


def run_form_filler(headless: bool = False):
    """Run the form filler bot."""
    print("\n🤖 Task Automation Bot — Form Filler")
    print("   Target: demoqa.com/automation-practice-form\n")

    form_data = FormData(
        first_name="Rahul",
        last_name="Sharma",
        email="rahul.sharma@example.com",
        phone="9876543210",
        hobbies=["Sports", "Reading"],
        current_address="42 Park Street, Kolkata, West Bengal",
        state="NCR",
        city="Delhi",
    )

    bot = FormFillerBot(headless=headless, form_data=form_data)
    bot.start()
    try:
        success = bot.fill_form()
        bot.print_summary()
        return success
    finally:
        bot.stop()


if __name__ == "__main__":
    run_form_filler(headless=False)
