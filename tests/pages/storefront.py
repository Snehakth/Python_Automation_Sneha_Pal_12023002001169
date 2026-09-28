"""Page actions for the Tutorialsninja OpenCart demo storefront."""

from uuid import uuid4

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Storefront:
    def __init__(self, driver, base_url: str, timeout: int = 15):
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/"
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.base_url)

    def register_account_and_login(self):
        """Create a disposable demo account, then log in through the login form."""
        account = {
            "email": f"selenium.{uuid4().hex[:12]}@example.com",
            "password": f"Capstone-{uuid4().hex[:10]}!",
        }
        self.driver.get(self.base_url + "index.php?route=account/register")
        self.wait.until(EC.visibility_of_element_located((By.NAME, "firstname"))).send_keys("Selenium")
        self.driver.find_element(By.NAME, "lastname").send_keys("Capstone")
        self.driver.find_element(By.NAME, "email").send_keys(account["email"])
        self.driver.find_element(By.NAME, "telephone").send_keys("5551234567")
        self.driver.find_element(By.NAME, "password").send_keys(account["password"])
        self.driver.find_element(By.NAME, "confirm").send_keys(account["password"])
        self.driver.find_element(By.NAME, "agree").click()
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#content h1"), "Your Account Has Been Created")
        )

        self.driver.get(self.base_url + "index.php?route=account/logout")
        self.driver.get(self.base_url + "index.php?route=account/login")
        self.wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(account["email"])
        self.driver.find_element(By.NAME, "password").send_keys(account["password"])
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#content h2"), "My Account"))

    def search_for_product(self, product_name: str):
        search_box = self.wait.until(EC.visibility_of_element_located((By.NAME, "search")))
        search_box.clear()
        search_box.send_keys(product_name, Keys.ENTER)
        product_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class, 'product-layout')]//h4/a[normalize-space()='{product_name}']")
            )
        )
        product_link.click()

    def add_product_to_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "button-cart"))).click()
        self.handle_popups()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))

    def handle_popups(self):
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass

        for close_button in self.driver.find_elements(By.CSS_SELECTOR, ".alert button.close"):
            if close_button.is_displayed():
                close_button.click()

    def update_and_read_cart(self, product_name: str, quantity: int) -> dict:
        self.driver.get(self.base_url + "index.php?route=checkout/cart")
        product_row = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//div[@id='content']//tr[.//a[normalize-space()='{product_name}']]")
            )
        )
        quantity_input = product_row.find_element(By.CSS_SELECTOR, "input[name^='quantity']")
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
        product_row.find_element(
            By.CSS_SELECTOR, "button[data-original-title='Update'], button[title='Update']"
        ).click()

        self.wait.until(
            lambda current_driver: current_driver.find_element(
                By.XPATH, f"//div[@id='content']//tr[.//a[normalize-space()='{product_name}']]"
            ).find_element(By.CSS_SELECTOR, "input[name^='quantity']").get_attribute("value")
            == str(quantity)
        )
        product_row = self.driver.find_element(
            By.XPATH, f"//div[@id='content']//tr[.//a[normalize-space()='{product_name}']]"
        )
        return {
            "product_name": product_row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a").text.strip(),
            "quantity": product_row.find_element(By.CSS_SELECTOR, "input[name^='quantity']").get_attribute("value"),
            "row_text": product_row.text.strip(),
        }