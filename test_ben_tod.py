from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.support.wait import WebDriverWait

from Custom.custom_user_agent import get_driver_with_custom_profile
from config import profile_path


def clear_cart(driver):
    # Open the cart page
    driver.get("https://benandtod.com/cart")
    time.sleep(2)  # Wait for the page to load

    # Check if the cart is empty by looking for the "empty cart" message
    empty_cart_elements = driver.find_elements(By.XPATH,
                                               "//div[@class='title-cart text-center']//h3[text(🙁'“Hổng” có gì trong giỏ hết']")
    if empty_cart_elements:
        print("The cart is currently empty.")
    else:
        # Wait until the remove buttons are clickable (focusing on the 'remove-item-cart' class)
        remove_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "remove-item-cart"))
        )

        # Loop through all the remove buttons and click the icon within each button
        for button in remove_buttons:
            # Find the SVG element within the remove button
            svg_icon = button.find_element(By.XPATH, ".//svg[@class='icon']")

            # Wait until the icon is clickable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(svg_icon)
            )
            # Click the SVG icon to remove the item
            svg_icon.click()
            time.sleep(1)  # Short pause to ensure each item is removed

        print("All items have been removed from the cart.")

def checkout(driver):
    # Step 1: Open the product page
    driver.get("https://benandtod.com/products/gift-card-ngan")
    time.sleep(2)  # Wait for the page to load

    # Step 2: Enter quantity
    quantity_input = driver.find_element(By.ID, "qtym")
    quantity_input.clear()
    quantity_input.send_keys("1")  # Enter desired quantity

    # Step 3: Click "MUA NGAY" button to buy now
    buy_now_button = driver.find_element(By.CLASS_NAME, "buynow")
    buy_now_button.click()
    time.sleep(2)  # Wait to be redirected to the checkout page

    # Step 4: Fill in shipping information
    try:
        # Full name
        full_name_input = driver.find_element(By.ID, "billing_address_full_name")
        full_name_input.clear()
        full_name_input.send_keys("Trần Thẩm Khang")

        # Email
        email_input = driver.find_element(By.ID, "checkout_user_email")
        email_input.clear()
        email_input.send_keys("thamkhang2003@gmail.com")

        # Phone number
        phone_input = driver.find_element(By.ID, "billing_address_phone")
        phone_input.clear()
        phone_input.send_keys("0931142093")

        # Address
        address_input = driver.find_element(By.ID, "billing_address_address1")
        address_input.clear()
        address_input.send_keys("Tra Ngoa, Tra Con, Tra On")

        # Province
        province_select = driver.find_element(By.ID, "customer_shipping_province")
        province_select.click()
        time.sleep(1)
        province_option = province_select.find_element(By.XPATH, "//option[@value='50']")
        province_option.click()
        time.sleep(3)

        # District
        district_select = driver.find_element(By.ID, "customer_shipping_district")
        district_select.click()
        time.sleep(1)
        district_option = district_select.find_element(By.XPATH, "//option[@value='485']")
        district_option.click()
        time.sleep(3)

        # Town
        town_select = driver.find_element(By.ID, "customer_shipping_ward")
        town_select.click()
        time.sleep(1)
        town_option = town_select.find_element(By.XPATH, "//option[@value='27595']")
        town_option.click()
        time.sleep(3)

        continue_button = driver.find_element(By.CLASS_NAME, "step-footer-continue-btn")
        continue_button.click()
        time.sleep(5)

    except Exception as e:
        print("Error filling shipping information:", e)
        return

    # Step 4: Apply discount code if at the checkout page
    try:
        # Locate the discount input field by ID
        discount_input = driver.find_element(By.XPATH, "//input[@id='discount.code']")
        discount_input.send_keys("BT10KT11")  # Enter the discount code
        time.sleep(3)  # Wait for the discount to apply

        # Locate and click the "Sử dụng" (Use) button with the new class
        apply_discount_button = driver.find_element(By.XPATH, "//*[@id=\"form_discount_add\"]/div/div/div/button")

        apply_discount_button.click()
        time.sleep(3)  # Wait for the discount to apply

        # Step 5: Print entire order summary
        try:
            # Locate and print the subtotal
            subtotal_element = driver.find_element(By.XPATH,
                                                   "//tr[@class='total-line total-line-subtotal']//span[@class='order-summary-emphasis']")
            subtotal = subtotal_element.text.strip()

            # Locate and print the discount amount
            discount_element = driver.find_element(By.XPATH,
                                                   "//tr[@class='total-line total-line-reduction']//span[@class='order-summary-emphasis']")
            discount = discount_element.text.strip()

            # Locate and print the shipping fee
            shipping_element = driver.find_element(By.XPATH,
                                                   "//tr[@class='total-line total-line-shipping']//span[@class='order-summary-emphasis']")
            shipping = shipping_element.text.strip()

            # Locate and print the total amount
            total_element = driver.find_element(By.CLASS_NAME, "payment-due-price")
            total_price = total_element.text.strip()

            # Print all values
            print("Order Summary:")
            print(f"Subtotal: {subtotal}")
            print(f"Discount: {discount}")
            print(f"Shipping: {shipping}")
            print(f"Total: {total_price}")

        except Exception as e:
            print("Could not retrieve order summary:", e)


    except Exception as e:
        print("Could not apply discount code or find total price:", e)
# Set up Chrome options
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Call the clear_cart function
    # clear_cart(driver)

    checkout(driver)
finally:
    # Close the WebDriver
    time.sleep(2)
    driver.quit()