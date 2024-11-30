from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_login():
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()

    # Đặt username và password
    username = "trhuuhau"
    password = "Vkl041103"

    try:
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(2)  # Chờ 2 giây

        # Nhấp vào nút login trên trang chủ
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)  # Chờ 2 giây

        # Nhập username
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )
        username_field.send_keys(username)
        time.sleep(2)  # Chờ 2 giây

        # Nhập password
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)
        time.sleep(2)  # Chờ 2 giây

        # Nhấn nút login trên trang đăng nhập
        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(5)  # Chờ 5 giây để trang tải

        # Kiểm tra thành công bằng cách tìm phần tử có chứa tên người dùng
        success_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
        )

        # Thực hiện assert để xác minh đăng nhập thành công
        assert success_indicator is not None, "Đăng nhập không thành công: không tìm thấy phần tử xác nhận đăng nhập."

    except Exception as e:
        assert False, f"Đăng nhập thất bại với lỗi: {e}"

    finally:
        driver.quit()  # Đảm bảo đóng trình duyệt


def test_login_invalid_username():
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()

    # Đặt username và password (username sai)
    invalid_username = "wrongusername"
    password = "Vkl041103"  # Giữ nguyên mật khẩu đúng

    try:
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(2)  # Chờ 2 giây

        # Nhấp vào nút login trên trang chủ
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)  # Chờ 2 giây

        # Nhập username sai
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )
        username_field.send_keys(invalid_username)
        time.sleep(2)  # Chờ 2 giây

        # Nhập password đúng
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)
        time.sleep(2)  # Chờ 2 giây

        # Nhấn nút login
        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(5)  # Chờ 5 giây để trang tải

        # Kiểm tra thông báo lỗi xuất hiện
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//mat-error"))
        )

        # Thực hiện assert để xác minh đăng nhập thất bại
        assert error_message is not None, "Không tìm thấy thông báo lỗi khi đăng nhập thất bại với username sai."

    except Exception as e:
        assert False, f"Đăng nhập thất bại với lỗi: {e}"

    finally:
        driver.quit()  # Đảm bảo đóng trình duyệt
