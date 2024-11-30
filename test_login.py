from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_login_valid():
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
        time.sleep(2)

        # Nhập username và password
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)

        # Nhấn nút login
        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(5)

        # Kiểm tra thành công bằng cách tìm phần tử có chứa tên người dùng
        success_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
        )

        # Kiểm tra thành công
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
        time.sleep(2)

        # Nhấp vào nút login trên trang chủ
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)

        # Nhập username sai và password đúng
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )
        username_field.send_keys(invalid_username)
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)

        # Nhấn nút login
        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(5)

        # Kiểm tra thông báo lỗi xuất hiện
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//mat-error"))
        )

        # Kiểm tra thất bại
        assert error_message is not None, "Không tìm thấy thông báo lỗi khi đăng nhập thất bại với username sai."

    except Exception as e:
        assert False, f"Đăng nhập thất bại với lỗi: {e}"

    finally:
        driver.quit()  # Đảm bảo đóng trình duyệt

def test_register():
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()

    # Đặt thông tin đăng ký
    user_info = {
        "firstname": "Hau",
        "lastname": "Truu",
        "username": "carrot",
        "password": "Vkl041103",
        "confirm_password": "Vkl041103",
        "gender": "Male"
    }

    try:
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(2)  # Chờ 2 giây để trang tải

        # Nhấp vào nút login trên trang chủ
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)  # Chờ 2 giây sau khi nhấp nút login

        # Nhấp vào nút Register trên trang đăng nhập
        register_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Register']]"))
        )
        register_button.click()
        time.sleep(2)  # Chờ 2 giây sau khi nhấp nút đăng ký

        # Nhập thông tin đăng ký
        fields = {
            "firstname": "//input[@formcontrolname='firstname']",
            "lastname": "//input[@formcontrolname='lastname']",
            "username": "//input[@formcontrolname='username']",
            "password": "//input[@formcontrolname='password']",
            "confirm_password": "//input[@formcontrolname='confirmPassword']"
        }

        for key, xpath in fields.items():
            try:
                field = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                field.clear()  # Xóa trường nếu có dữ liệu cũ
                field.send_keys(user_info[key])
                time.sleep(1)  # Chờ 1 giây sau khi nhập dữ liệu vào mỗi trường
            except Exception as e:
                assert False, f"Không tìm thấy trường {key} với XPath: {xpath}. Lỗi: {e}"

        # Chọn giới tính
        gender_radio = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info['gender']}']"))
        )
        gender_radio.click()
        time.sleep(1)  # Chờ 1 giây sau khi chọn giới tính

        # Nhấn nút đăng ký
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-mdc-raised-button span.mdc-button__label"))
        ).click()
        time.sleep(5)  # Chờ 5 giây để nhìn cho rõ sau khi nhấn nút đăng ký

        # Chờ cho URL chuyển đổi đến trang đăng nhập
        WebDriverWait(driver, 30).until(
            EC.url_to_be("https://bookcart.azurewebsites.net/login")
        )

        # Kiểm tra thành công bằng cách xác minh URL
        assert driver.current_url == "https://bookcart.azurewebsites.net/login", "Đăng ký không thành công: không chuyển đến trang đăng nhập."

    except Exception as e:
        assert False, f"Đăng ký thất bại với lỗi: {e}"

    finally:
        driver.quit()  # Đảm bảo đóng trình duyệt

def test_register_invalid():
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()

    # Đặt thông tin đăng ký không hợp lệ
    user_info_invalid = {
        "firstname": "",  # Để trống trường firstname để kiểm tra thông báo lỗi
        "lastname": "Truu",
        "username": "existing_user",  # Giả sử tên người dùng này đã tồn tại
        "password": "Vkl041103",
        "confirm_password": "wrong_password",  # Mật khẩu xác nhận không khớp
        "gender": "Male"
    }

    try:
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(2)  # Thêm thời gian nghỉ sau khi tải trang

        # Nhấp vào nút login trên trang chủ
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)

        # Nhấp vào nút Register trên trang đăng nhập
        register_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Register']]"))
        )
        register_button.click()
        time.sleep(2)

        # Nhập thông tin đăng ký không hợp lệ
        fields = {
            "firstname": "//input[@formcontrolname='firstname']",
            "lastname": "//input[@formcontrolname='lastname']",
            "username": "//input[@formcontrolname='username']",
            "password": "//input[@formcontrolname='password']",
            "confirm_password": "//input[@formcontrolname='confirmPassword']"
        }

        for key, xpath in fields.items():
            field = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            field.clear()
            field.send_keys(user_info_invalid[key])
            time.sleep(1)

        # Chọn giới tính
        gender_radio = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info_invalid['gender']}']"))
        )
        gender_radio.click()
        time.sleep(1)

        # Nhấp vào nút đăng ký
        submit_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/div/app-user-registration/div/mat-card/mat-card-content/form/mat-card-actions/button"))
        )
        submit_button.click()
        time.sleep(2)

        # Kiểm tra thông báo lỗi
        error_messages = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "mat-mdc-form-field-error"))
        )

        # Lấy các thông báo lỗi và loại bỏ khoảng trắng thừa
        error_texts = [msg.text.strip() for msg in error_messages]

        # Danh sách các thông báo lỗi mong đợi
        expected_errors = ["First Name is required", "Password do not match"]

        # Kiểm tra các thông báo lỗi
        for error in expected_errors:
            assert error in error_texts, f"Thông báo lỗi '{error}' không xuất hiện."

        print("Kiểm tra thông báo lỗi thành công.")

    except Exception as e:
        assert False, f"Đăng ký không thành công với lỗi: {e}"

    finally:
        driver.quit()
