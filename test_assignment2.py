from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# *************LOGIN - REGISTER - LOGOUT**************

# 1. test đăng ký
# nhớ mỗi lần chạy demo phải đổi username mới thành công
def test_registration(driver):
    # Mở trang đăng ký
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Thời gian chờ để người kiểm thử xem trang

    # Nhấn nút `Login`
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Login' and .//span[text()=' Login ']]"))
    )   # chờ 1 đk cụ thể
    #EC là viết tắt của expected_conditions, giúp bạn chờ và kiểm tra các điều kiện trong quá trình tự động hóa kiểm thử
    login_button.click()
    time.sleep(2)

    # Nhấn nút "User Registration"
    register_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='mdc-button__label' and text()='Register']"))
    )
    register_button.click()
    time.sleep(2)

    # Nhập thông tin vào các trường đăng ký
    first_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='firstname']"))
    )   # chờ Khi ô nhập liệu xuất hiện
    last_name = driver.find_element(By.XPATH, "//input[@formcontrolname='lastname']")
    user_name = driver.find_element(By.XPATH, "//input[@formcontrolname='username']")
    password = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    confirm_password = driver.find_element(By.XPATH, "//input[@formcontrolname='confirmPassword']")

    # Điền thông tin vào các trường
    first_name.send_keys("Khanh Linh")
    time.sleep(1)  # Chờ một chút để thấy thao tác
    last_name.send_keys("Vo")
    time.sleep(1)
    user_name.send_keys("hiloaqfe")
    time.sleep(1)
    password.send_keys("Linh123456789")
    time.sleep(1)
    confirm_password.send_keys("Linh123456789")
    time.sleep(1)

    # Chọn giới tính
    gender_male = driver.find_element(By.XPATH, "//input[@value='Male']")
    gender_male.click()
    time.sleep(1)

    # Nhấn nút `Register`
    register_submit = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='mdc-button__label' and text()='Register']"))
    )
    register_submit.click()
    time.sleep(5)  # Chờ để đảm bảo đăng ký thành công

    # Kiểm tra xem đã chuyển đến trang đăng nhập
    assert "login" in driver.current_url, "Không chuyển hướng đến trang đăng nhập sau khi đăng ký."

    # Nếu assert thành công, in ra thông báo
    print("Đã chuyển hướng đến trang đăng nhập sau khi đăng ký thành công.")

# 2. test đăng ký với first_name để trống và confirm_pw không khớp
def test_register_invalid(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Thời gian chờ để người kiểm thử xem trang

    user_info_invalid = {   #Một dictionary chứa thông tin người dùng không hợp lệ
        "firstname": "",    # Tên để trống
        "lastname": "Linh",
        "username": "motconvit1",
        "password": "Vkl041103",
        "confirm_password": "wrong_password",   # Mật khẩu xác nhận không khớp
        "gender": "Male"
    }

    try:    # Nhấn nút "Login" để chuyển tới trang đăng nhập
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )   # Đợi nút "Login" có thể nhấp được
        login_button.click()
        time.sleep(2)

        # Nhấn nút "Register"
        register_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Register']]"))
        )
        register_button.click()
        time.sleep(2)

        # Tạo một dictionary chứa các trường nhập liệu và các XPath tương ứng
        fields = {
            "firstname": "//input[@formcontrolname='firstname']",
            "lastname": "//input[@formcontrolname='lastname']",
            "username": "//input[@formcontrolname='username']",
            "password": "//input[@formcontrolname='password']",
            "confirm_password": "//input[@formcontrolname='confirmPassword']"
        }

        # Điền thông tin vào các trường trên form đăng ký
        for key, xpath in fields.items():
            field = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )   # Đợi trường nhập liệu xuất hiện trên giao diện
            field.clear()   # Xóa giá trị hiện tại (nếu có)
            field.send_keys(user_info_invalid[key])  # Nhập giá trị từ dictionary vào trường tương ứng
            time.sleep(1)

        # Chọn giới tính từ radio button
        gender_radio = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info_invalid['gender']}']"))
        )
        gender_radio.click()
        time.sleep(1)

        # Nhấn nút "Register" để gửi form
        submit_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-user-registration/div/mat-card/mat-card-content/form/mat-card-actions/button"))
        )
        submit_button.click()
        time.sleep(2)

        #Kiểm tra các thông báo lỗi
        error_messages = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "mat-mdc-form-field-error"))
        )   # Đợi các thông báo lỗi xuất hiện trên giao diện
        error_texts = [msg.text.strip() for msg in error_messages]  # Lấy nội dung các thông báo lỗi

        # msg.text dùng để lấy văn bản (text) nội dung các thông báo lỗi
        # nếu một phần tử WebElement có văn bản là "First Name is required", thì msg.text sẽ trả về chuỗi này
        #.strip() : loại bỏ khoảng trắng ở đầu và cuối, đảm bảo thông báo lỗi không bị ảnh hưởng bởi khoảng trắng thừa khi kiểm tra

        # Kiểm tra xem các thông báo lỗi mong đợi có xuất hiện không
        expected_errors = ["First Name is required", "Password do not match"]
        for error in expected_errors:
            assert error in error_texts, f"Thông báo lỗi '{error}' không xuất hiện."
                            #error_texts là danh sách các thông báo lỗi mà bạn thu thập được từ trang web

        # In thông báo khi tất cả kiểm tra thành công
        print("Pass: hệ thống đã thông báo lỗi.")

    except Exception as e:
        assert False, f"Đăng ký không thành công với lỗi: {e}"

# 3. test đăng nhập
def test_login(driver):
    # Mở trang đăng nhập
    driver.get("https://bookcart.azurewebsites.net/login")
    time.sleep(2)  # Thời gian chờ để đảm bảo trang đã tải

    # Nhập tên người dùng
    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']"))
    )
    username_input.send_keys("heheee")
    time.sleep(1)  # Thời gian chờ sau khi nhập tên người dùng

    # Nhập mật khẩu
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    password_input.send_keys("Linh123456789")
    time.sleep(1)  # Thời gian chờ sau khi nhập mật khẩu

    # Nhấn nút `Login`
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
    )
    login_button.click()
    time.sleep(5)  # Chờ một chút để trang phản hồi

    # Kiểm tra rằng đã chuyển đến trang chính sau khi đăng nhập
    time.sleep(2)  # Thời gian chờ trước khi kiểm tra URL
    assert driver.current_url == "https://bookcart.azurewebsites.net/", "Đăng nhập không thành công, không chuyển đến trang chính."
    print("Đăng nhập thành công, đã chuyển đến trang chính.")

# 4. test đăng nhập sai
def test_login_error(driver):
    # Mở trang đăng nhập
    driver.get("https://bookcart.azurewebsites.net/login")
    time.sleep(2)

    # Nhập tên người dùng sai
    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']"))
    )
    username_input.send_keys("heh13455f")
    time.sleep(1)

    # Nhập mật khẩu
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    password_input.send_keys("Linh123456789")
    time.sleep(1)

    # Nhấn nút `Login`
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
    )
    login_button.click()
    time.sleep(5)  # Chờ một chút để trang đăng nhập phản hồi

    # Kiểm tra thông báo lỗi
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//mat-error[contains(text(), 'Username or Password is incorrect')]"))
    )

    #kiểm tra xem phần tử có được hiển thị trên giao diện người dùng hay không
    assert error_message.is_displayed(), "Thông báo lỗi không được hiển thị."
    # ss văn bản của thông báo lỗi với văn bản mong đợi "Username or Password is incorrect.".
    assert error_message.text == "Username or Password is incorrect.", f"Thông báo lỗi không khớp: {error_message.text}"
    print("Test Passed: Thông báo lỗi được hiển thị đúng.")

    # Kiểm tra rằng trang chính không được hiển thị
    assert "Book Cart" not in driver.title, "Đăng nhập thành công khi không nên như vậy."
    print("Đăng nhập thất bại như mong đợi.")

# 5. test đăng xuất
def test_logout(driver):
    # Mở trang đăng nhập
    driver.get("https://bookcart.azurewebsites.net/login")
    time.sleep(2)

    # Nhập tên người dùng
    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']"))
    )
    username_input.send_keys("heheee")
    time.sleep(1)

    # Nhập mật khẩu
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    password_input.send_keys("Linh123456789")
    time.sleep(1)

    # Nhấn nút `Login`
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[span[@class='mdc-button__label' and text()='Login']]"))
    )
    login_button.click()
    time.sleep(5)  # Đợi một chút để trang chính tải

    # Nhấp vào nút người dùng theo XPath cụ thể
    user_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]"))
    )
    user_button.click()
    time.sleep(2)  # Thời gian chờ trước khi nhấp vào nút Logout

    # Nhấp vào nút Logout
    logout_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Logout']]"))
    )
    logout_button.click()
    time.sleep(5)  # Đợi để xác nhận đã quay lại trang đăng nhập

    # Kiểm tra URL hiện tại
    current_url = driver.current_url
    print("Current URL after logout:", current_url)

    # Assert để kiểm tra đăng xuất thành công
    assert current_url == "https://bookcart.azurewebsites.net/login", "Đăng xuất không thành công, không chuyển về trang đăng nhập."

    print("Đăng xuất thành công và đã chuyển về trang đăng nhập.")

# **************FORM SUBMISSION*******************

# 10. kiểm tra đăng ký với first_name và last_name là các chữ số (false)
def test_form_submission_with_numeric_firstname_lastname(driver):
    user_info = {
        "firstname": "123",
        "lastname": "456",
        "username": "carrotne123",
        "password": "Vkl041103",
        "confirm_password": "Vkl041103",
        "gender": "Male"
    }

    try:
        # Mở trang đăng ký
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(2)  # Thời gian chờ để người kiểm thử xem trang

        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)

        register_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Register']]"))
        )
        register_button.click()
        time.sleep(2)

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
            field.send_keys(user_info[key])
            time.sleep(1)

        gender_radio = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info['gender']}']"))
        )
        gender_radio.click()
        time.sleep(1)

        submit_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-mdc-raised-button span.mdc-button__label"))
        )
        submit_button.click()
        time.sleep(3)

        # Kiểm tra thông báo lỗi
        try:
            error_message = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='error-message']"))
            )
            assert error_message.is_displayed(), "Thông báo lỗi không hiển thị."
            print("Pass: Thông báo lỗi hiển thị khi first name và last name là số.")
        except Exception:
            assert False, "Fail: Không có thông báo lỗi khi first name và last name là số."

    except Exception as e:
        assert False, f"Đăng ký thất bại với lỗi: {e}"

# 11. kiểm tra đăng ký mà không chọn giới tính (false)
def test_form_submission_register_without_gender_selection(driver):
    user_info = {
        "firstname": "Khanh Linh",
        "lastname": "Vo",
        "username": "carrot1",
        "password": "Vkl041103",  # Mật khẩu hợp lệ
        "confirm_password": "Vkl041103"
    }

    try:
        # Mở trang đăng ký
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(2)  # Thời gian chờ để người kiểm thử xem trang

        # Nhấn nút đăng nhập
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)  # Thời gian chờ sau khi nhấn nút đăng nhập

        # Nhấn nút đăng ký
        register_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Register']]"))
        )
        register_button.click()
        time.sleep(2)  # Thời gian chờ sau khi nhấn nút đăng ký

        # Điền thông tin vào các trường
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
            field.send_keys(user_info[key])
            time.sleep(1)  # Thời gian chờ sau khi nhập mỗi trường

        # Nhấn nút đăng ký mà không chọn giới tính
        submit_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-mdc-raised-button span.mdc-button__label"))
        )
        submit_button.click()
        time.sleep(2)  # Thời gian chờ sau khi nhấn nút gửi

        # Kiểm tra thông báo lỗi yêu cầu chọn giới tính
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-user-registration/div/mat-card/mat-card-content/form/mat-form-field[5]/div[2]/div"))
        )

        # Định nghĩa thông báo lỗi mong đợi
        expected_error_message = "please select your gender"
        assert expected_error_message in error_message.text.lower(), f"Expected error message not found. Actual message: {error_message.text}"
        print("Test Passed: Error message for gender selection displayed as expected.")

    except TimeoutException:
        assert False, "False: Thông báo lỗi yêu cầu chọn giới tính không xuất hiện."
    except Exception as e:
        assert False, f"Đăng ký thất bại với lỗi: {e}"


# 12. Kiểm tra có cho checkout với các trường trong place order bỏ trống không
def test_form_submission_checkout_without_info(driver):
    # Gọi hàm đăng nhập hợp lệ trước khi thực hiện các bước tiếp theo
    test_login(driver)

    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
    )
    add_to_cart_button.click()

    cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
    )
    cart_icon.click()

    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[2]/td[6]/button"))
    )
    checkout_button.click()

    time.sleep(3)

    place_order_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    place_order_button.click()
    time.sleep(3)

    # Kiểm tra nếu các trường bị lỗi có lớp 'mat-form-field-invalid'
    required_fields = driver.find_elements(By.CSS_SELECTOR, 'mat-form-field.mat-form-field-invalid')
    for field in required_fields:
        assert "mat-form-field-invalid" in field.get_attribute("class"), \
            "Trường không có lớp 'mat-form-field-invalid' khi không nhập thông tin."

    # In thông báo khi bài kiểm tra pass
    print("Pass: Tất cả các trường yêu cầu hiển thị lỗi khi không nhập thông tin.")


# *****************NAVIGATION*******************

# 13. test điều hướng giữa các trang khi nhấp nút danh mục sản phẩm
def test_category_navigation(driver):
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Thời gian chờ để đảm bảo trang đã tải

    # Kiểm tra điều hướng đến trang chính
    expected_url = "https://bookcart.azurewebsites.net/"
    current_url = driver.current_url
    assert current_url == expected_url, f"Expected URL: {expected_url}, but got: {current_url}"
    print(f"Điều hướng đến trang chính thành công. URL đúng: {current_url}")

    # Nhấp vào các danh mục và kiểm tra điều hướng
    categories = {
        "Biography": "https://bookcart.azurewebsites.net/filter?category=biography",
        "Fiction": "https://bookcart.azurewebsites.net/filter?category=fiction",
        "Mystery": "https://bookcart.azurewebsites.net/filter?category=mystery",
        "Fantasy": "https://bookcart.azurewebsites.net/filter?category=fantasy",
        "Romance": "https://bookcart.azurewebsites.net/filter?category=romance",
        "All Categories": "https://bookcart.azurewebsites.net/"
    }

    # Kiểm tra từng danh mục riêng lẻ
    for category, expected_url in categories.items():
        # Nhấp vào danh mục
        category_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, category))
        )
        category_button.click()
        time.sleep(2)  # Thời gian chờ sau khi nhấp vào danh mục

        # Kiểm tra URL hiện tại sau khi nhấp vào danh mục
        current_url = driver.current_url
        assert current_url == expected_url, f"Expected URL: {expected_url}, but got: {current_url}"
        print(f"Điều hướng đến danh mục {category} thành công. URL đúng: ", current_url)  # Thông báo thành công
        time.sleep(2)  # Thời gian chờ sau khi xác nhận URL

# 14. test điều hướng các chức năng trên thanh menu
def test_navigation_of_menu_functions(driver):
    """
    Kiểm tra khả năng điều hướng trong ứng dụng web sau khi đăng nhập.
    Mở các trang như Wishlist, Giỏ hàng, Menu tài khoản, My Orders, kiểm tra Swagger, GitHub và thực hiện Logout.
    Sau mỗi bước, quay lại trang chủ.
    """
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(3)  # Thời gian chờ để trang chủ tải hoàn toàn

    username = "heheee"
    password = "Linh123456789"

    print("Bắt đầu quá trình đăng nhập...")
    try:
        # Đăng nhập
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(3)

        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)

        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(4)

        success_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' heheee']"))
        )
        assert success_indicator is not None, "Đăng nhập không thành công: không tìm thấy phần tử xác nhận đăng nhập."
        print("Đăng nhập thành công.")

        # Mở Wishlist
        print("Đang mở Wishlist...")
        wishlist_button = driver.find_element(By.XPATH,
                                              "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[1]")
        wishlist_button.click()
        time.sleep(5)
        print("Đã mở Wishlist, quay lại trang chủ.")
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(3)

        # Mở Giỏ hàng
        print("Đang mở Giỏ hàng...")
        cart_button = driver.find_element(By.XPATH,
                                          "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]")
        cart_button.click()
        time.sleep(5)
        print("Đã mở Giỏ hàng, quay lại trang chủ.")
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(3)

        # Mở Menu tài khoản
        print("Đang mở Menu tài khoản...")
        account_menu = driver.find_element(By.XPATH,
                                           "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]")
        account_menu.click()
        time.sleep(5)

        # Mở My Orders từ menu tài khoản
        print("Đang mở My Orders...")
        my_orders_button = driver.find_element(By.XPATH, "//*[@id='mat-menu-panel-0']/div/button[1]")
        my_orders_button.click()
        time.sleep(5)
        print("Đã mở My Orders, quay lại trang chủ.")
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(3)

        # Mở Swagger (kiểm tra tính năng Swagger)
        print("Đang mở Swagger...")
        main_window = driver.current_window_handle
        swagger_button = driver.find_element(By.XPATH,
                                             "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[2]")
        swagger_button.click()
        time.sleep(5)

        # Đóng tab Swagger sau khi kiểm tra
        all_windows = driver.window_handles
        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(main_window)
        print("Đã mở Swagger, đóng tab Swagger và quay lại trang chủ.")
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(5)

        # Mở GitHub (kiểm tra tính năng GitHub)
        print("Đang mở GitHub...")
        github_button = driver.find_element(By.XPATH,
                                            "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[3]")
        github_button.click()
        time.sleep(5)

        # Đóng tab GitHub sau khi kiểm tra
        all_windows = driver.window_handles
        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(main_window)
        print("Đã mở GitHub, đóng tab GitHub và quay lại trang chủ.")
        driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(5)

        # Mở Menu tài khoản
        print("Đang mở Menu tài khoản...")
        account_menu = driver.find_element(By.XPATH,
                                           "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]")
        account_menu.click()
        time.sleep(5)

        # Mở Logout từ menu tài khoản
        print("Đang thực hiện Logout...")
        logout_button = driver.find_element(By.XPATH, "//*[@id='mat-menu-panel-0']/div/button[2]")
        logout_button.click()
        time.sleep(4)

        # Kiểm tra trang login sau khi logout bằng URL
        print("Đã thực hiện Logout, kiểm tra URL...")
        current_url = driver.current_url
        expected_url = "https://bookcart.azurewebsites.net/login"
        assert current_url == expected_url, f"Kiểm tra URL thất bại. URL hiện tại là: {current_url}, nhưng kỳ vọng: {expected_url}"
        print(f"Đã chuyển đến trang Login thành công. URL hiện tại: {current_url}")

    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình kiểm tra điều hướng: {e}")

# 15. test điều hướng giữa các trang trong my order
def test_check_and_navigation_myorder(driver):
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Thời gian chờ để đảm bảo trang đã tải

    username = "heheee"
    password = "Linh123456789"

    try:
        # Nhấn vào nút đăng nhập
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)

        # Nhập tên người dùng và mật khẩu
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)

        # Nhấn nút `Login`
        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(5)

        # Kiểm tra đăng nhập thành công
        success_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' heheee']"))
        )
        assert success_indicator is not None, "Đăng nhập không thành công."
        print("Đăng nhập thành công.")

        # Mở menu người dùng
        user_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]"))
        )
        user_button.click()
        time.sleep(2)

        # Nhấn chọn `My Orders`
        my_orders_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='My Orders']]"))
        )
        my_orders_button.click()
        time.sleep(5)

        # Chọn một đơn hàng trong danh sách (161-209324)
        order_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//tr[@role='row' and contains(@class, 'example-element-row')]//td[contains(text(), '161-209324')]")
            )
        )
        order_element.click()
        time.sleep(5)

        print("Đã chọn đơn hàng cụ thể.")

        # Cuộn trang từ từ để  thấy các sản phẩm
        for _ in range(1):  # Số lần cuộn trang (có thể điều chỉnh)
            driver.execute_script("window.scrollBy(0, 300);")  # Cuộn 300px mỗi lần
            time.sleep(1)  # Thời gian chờ mỗi lần cuộn

        # Nhấn nút `Next Page` cho đến khi không nhấn được nữa
        while True:
            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']"))
                )
                next_page_button.click()
                print("Đã chuyển sang trang tiếp theo của danh sách đơn hàng.")
                time.sleep(5)  # Chờ cho nội dung tải
            except:
                print("Không thể nhấn nút 'Next Page' nữa, đã đến trang cuối cùng.")
                break

        print("Đã chuyển sang trang tiếp theo của danh sách đơn hàng.")

        # Nhấp vào nút người dùng để mở menu
        user_button.click()
        time.sleep(2)

        # Nhấp vào nút `Logout`
        logout_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Logout']]"))
        )
        logout_button.click()
        time.sleep(5)

        # Kiểm tra URL hiện tại để xác nhận đã đăng xuất
        current_url = driver.current_url
        print("URL hiện tại sau khi đăng xuất:", current_url)

        # Xác nhận URL của trang đăng nhập để kiểm tra đăng xuất thành công
        assert current_url == "https://bookcart.azurewebsites.net/login", "Đăng xuất không thành công, không chuyển về trang đăng nhập."

        print("Đăng xuất thành công và đã chuyển về trang đăng nhập.")

    except Exception as e:
        assert False, f"Kiểm thử thất bại với lỗi: {e}"

# *******************DATA VALIDATION********************

# 16. test đăng ký với username đã tồn tại
def test_registration_error(driver):
    # Mở trang đăng chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Thời gian chờ để người kiểm thử xem trang

    # Nhấn nút `Login`
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Login' and .//span[text()=' Login ']]"))
    )
    login_button.click()
    time.sleep(2)

    # Nhấn nút "Registration"
    register_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='mdc-button__label' and text()='Register']"))
    )
    register_button.click()
    time.sleep(2)

    # Nhập thông tin vào các trường đăng ký
    first_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='firstname']"))
    )
    last_name = driver.find_element(By.XPATH, "//input[@formcontrolname='lastname']")
    user_name = driver.find_element(By.XPATH, "//input[@formcontrolname='username']")
    password = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    confirm_password = driver.find_element(By.XPATH, "//input[@formcontrolname='confirmPassword']")

    # Điền thông tin vào các trường theo ảnh
    first_name.send_keys("holalinh")
    time.sleep(1)
    last_name.send_keys("carot")
    time.sleep(1)
    user_name.send_keys("hehee")  # Tên người dùng đã tồn tại
    time.sleep(3)
    password.send_keys("Linh12345")
    time.sleep(1)
    confirm_password.send_keys("Linh12345")
    time.sleep(1)

    # Chọn giới tính
    gender_female = driver.find_element(By.XPATH, "//input[@value='Female']")
    gender_female.click()
    time.sleep(1)

    # Nhấn nút `Register`
    register_submit = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='mdc-button__label' and text()='Register']"))
    )
    register_submit.click()
    time.sleep(2)  # Chờ một chút để thông báo lỗi hiển thị nếu có

    # Kiểm tra xem có thông báo lỗi "User Name is not available" hay không
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//mat-error[contains(text(), 'User Name is not available')]"))
        )
        assert error_message.is_displayed(), "Thông báo lỗi 'User Name is not available' không hiển thị."
        print("Thông báo lỗi 'User Name is not available' đã hiển thị đúng cách.")
    except:
        print("Thông báo lỗi 'User Name is not available' không xuất hiện khi tên người dùng đã tồn tại.")

# 18. test để trống các trường khi đăng nhập
def test_login_blank_fields(driver):
    try:
        # Mở trang đăng nhập
        driver.get("https://bookcart.azurewebsites.net/login")
        time.sleep(5)  # Thời gian chờ dài hơn để đảm bảo trang đã tải (5 giây)

        # Để trống các trường nhập liệu (không nhập dữ liệu vào)
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']"))
        )
        time.sleep(1)  # Thêm thời gian chờ sau khi tìm thấy trường nhập username

        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='password']"))
        )
        time.sleep(1)  # Thêm thời gian chờ sau khi tìm thấy trường nhập password

        # Để trống cả hai trường nhập liệu
        username_input.send_keys("")
        time.sleep(1)  # Thêm thời gian chờ sau khi nhập username

        password_input.send_keys("")
        time.sleep(1)  # Thêm thời gian chờ sau khi nhập password

        # Nhấn nút `Login` để gửi form
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        time.sleep(1)  # Thêm thời gian chờ trước khi nhấn nút Login

        login_button.click()
        time.sleep(2)  # Thêm thời gian chờ sau khi nhấn nút Login

        # Chờ để thông báo lỗi xuất hiện
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//mat-error"))
        )
        time.sleep(1)  # Thêm thời gian chờ sau khi thông báo lỗi xuất hiện

        assert error_message is not None, "Không tìm thấy thông báo lỗi khi không nhập thông tin đăng nhập."

        print("Kiểm thử thành công: Thông báo lỗi hiển thị khi để trống trường đăng nhập.")

    except Exception as e:
        assert False, f"Đăng nhập thất bại với lỗi: {e}"

# 17. test chỉ nhập 2 chữ số cho pincode
def test_data_validation_placeorder(driver):
    try:
        # Đăng nhập trước
        test_login(driver)

        # Nhấn vào nút "add_to_cart"
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
        )
        add_to_cart_button.click()
        time.sleep(1)

        # Kiểm tra thông báo thêm vào giỏ hàng hay chưa
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.mdc-snackbar__label'))
        )
        assert "one item added to cart" in success_message.text.lower(), "Sản phẩm chưa được thêm vào giỏ hàng."

        # Nhấn vào biểu tượng giỏ hàng
        cart_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        cart_icon.click()
        time.sleep(1)

        # Nhấn vào nút checkout
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[2]/td[6]/button"))
        )
        checkout_button.click()
        time.sleep(1)

        # Điền thông tin vào biểu mẫu
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@formcontrolname="name"]'))
        ).send_keys('Nguyen Thi L')

        driver.find_element(By.XPATH, '//*[@formcontrolname="addressLine1"]').send_keys('888 đường hcm')
        driver.find_element(By.XPATH, '//*[@formcontrolname="addressLine2"]').send_keys('nhà thuốc')

        # Nhập mã pin không hợp lệ (2 chữ số)
        driver.find_element(By.XPATH, '//*[@formcontrolname="pincode"]').send_keys('68')
        driver.find_element(By.XPATH, '//*[@formcontrolname="state"]').send_keys('Hồ Chí Minh')

        # Nhấn vào nút "Place Order"
        place_order_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        time.sleep(2)  # Thêm thời gian chờ trước khi nhấn nút Place Order

        place_order_button.click()
        time.sleep(2)  # Thêm thời gian chờ sau khi nhấn nút Place Order

        # Kiểm tra thông báo lỗi cho trường pincode
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'mat-error'))
        )
        assert error_message is not None, "Không tìm thấy thông báo lỗi cho trường pincode."

        assert "pincode must have 6 digits only and cannot start with 0" in error_message.text.lower(), "Thông báo lỗi cho trường pincode không đúng."

        print("Pass: Lỗi nhập pincode đã được thông báo.")

    except Exception as e:
        assert False, f"Kiểm thử thất bại với lỗi: {e}"

# ***************ADD TO CART - CHECKOUT*****************


def add_to_wishlist(driver, quantity=1):
    # Mở trang đăng nhập
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Thời gian chờ để đảm bảo trang đã tải


    username = "heheee"
    password = "Linh123456789"

    print("Bắt đầu quá trình đăng nhập...")
    try:
        # Đăng nhập
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)

        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)

        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(5)

        success_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' heheee']"))
        )
        assert success_indicator is not None, "Đăng nhập không thành công: không tìm thấy phần tử xác nhận đăng nhập."
        print("Đăng nhập thành công. Tiến hành tìm kiếm sản phẩm...")

    except Exception as e:
        print(f"Đăng nhập thất bại với lỗi: {e}")
        return []

    try:
        # Tìm tất cả sản phẩm
        products = WebDriverWait(driver, 15).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//app-book-card"))
        )

        added_products = set()
        print(f"Tìm thấy {len(products)} sản phẩm. Sẽ thêm sản phẩm vào danh sách yêu thích...")

        for product in products:
            product_name = product.find_element(By.XPATH, ".//strong").text

            try:
                # Kiểm tra xem nút đã được chọn chưa
                add_to_wishlist_button = product.find_element(By.XPATH,
                                                              ".//span[contains(@class, 'favourite-unselected')]")
                is_selected = "favourite-selected" in add_to_wishlist_button.get_attribute("class")

                if is_selected:
                    print(f"Sản phẩm '{product_name}' đã có trong danh sách yêu thích, bỏ qua...")
                    continue  # Chuyển sang sản phẩm tiếp theo nếu đã được chọn

                # Thêm sản phẩm vào wishlist
                add_to_wishlist_button.click()
                print(f"Đang thêm sản phẩm: {product_name} vào danh sách yêu thích...")

                # Kiểm tra thông báo thành công
                success_message = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.mdc-snackbar__label'))
                )
                assert "item added to your wishlist" in success_message.text.lower(), f"Sản phẩm '{product_name}' chưa được thêm vào danh sách yêu thích."
                print(f"Sản phẩm '{product_name}' đã được thêm vào danh sách yêu thích thành công.")

                # Chỉ thêm vào added_products khi sản phẩm được thêm thành công
                added_products.add(product_name)

                break  # Dừng vòng lặp nếu đã thêm thành công 1 sản phẩm

            except TimeoutException:
                print(f"Không thể thêm sản phẩm '{product_name}' vào danh sách yêu thích.")
            except Exception as e:
                print(f"Lỗi xảy ra khi thêm sản phẩm '{product_name}' vào danh sách yêu thích: {e}")

        return list(added_products)

    except TimeoutException:
        assert False, "Không tìm thấy danh sách sản phẩm sau khi đăng nhập."

# 19. test thêm sản phẩm vào yêu thích
def test_add_1_product_to_wishlist(driver):

    print("Thêm 1 sản phẩm vào danh sách yêu thích khi nó chưa có trong wishlist...")

    # Gọi hàm `add_to_wishlist` để thêm sản phẩm vào wishlist
    added_products = add_to_wishlist(driver, quantity=1)

    try:
        # Điều hướng đến trang wishlist nếu cần
        wishlist_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[1]"))
            # Chỉnh sửa XPATH nếu cần
        )
        wishlist_button.click()
        time.sleep(3)  # Đợi trang wishlist tải

        # Đợi danh sách wishlist xuất hiện sau khi thêm sản phẩm
        wishlist_items = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//app-wishlist//table/tbody/tr"))
        )

        # Đếm số lượng sản phẩm trong wishlist
        wishlist_item_count = len(wishlist_items)
        assert wishlist_item_count >= 1, "Danh sách yêu thích không có sản phẩm."

        # Lấy tên tất cả các sản phẩm trong wishlist
        wishlist_product_names = []
        for item in wishlist_items:
            product_name_in_wishlist = item.find_element(
                By.XPATH, ".//td[contains(@class, 'mat-column-title')]//a"
            ).text
            wishlist_product_names.append(product_name_in_wishlist)

        # Kiểm tra xem sản phẩm vừa thêm có nằm trong danh sách yêu thích
        for product_name in added_products:
            assert product_name in wishlist_product_names, (
                f"Sản phẩm '{product_name}' không có trong danh sách yêu thích."
            )

        print(f"Tất cả các sản phẩm đã được thêm vào danh sách yêu thích thành công!")

    except TimeoutException:
        raise Exception("Không thể mở danh sách yêu thích hoặc không tìm thấy sản phẩm trong danh sách yêu thích.")

# 20. test thêm sản phẩm (Nhấp vào sản phẩm cụ thể)
def test_add_to_cart(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")

    # Đợi để trang tải
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))

    # Nhấp vào sản phẩm cụ thể
    product_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/books/details/15']"))  # ID sản phẩm là 15
    )

    # Cuộn đến phần tử trước khi nhấp
    driver.execute_script("arguments[0].scrollIntoView(true);", product_link)
    time.sleep(1)  # Đợi để cuộn hoàn tất
    driver.execute_script("arguments[0].click();", product_link)
    time.sleep(2)  # Đợi cho trang sản phẩm tải

    # Nhấp vào nút "Add to Cart"
    add_to_cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Add to Cart')]]"))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button)

    # Nhấp vào giỏ hàng
    cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[mat-icon[contains(text(), 'shopping_cart')]]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", cart_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", cart_button)

    # Đợi trang giỏ hàng tải
    time.sleep(2)

    # Xác nhận tiêu đề sản phẩm
    product_title_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//td[contains(@class, 'mat-column-title')]//a"))
    )

    # Lấy văn bản tiêu đề sản phẩm
    actual_title = product_title_element.text

    # Tiêu đề sản phẩm mong muốn
    expected_title = "Harry Potter and the Sorcerer's Stone"  # Cập nhật tiêu đề mong đợi

    # Kiểm tra xem tiêu đề sản phẩm có đúng không
    assert actual_title == expected_title, f"Tiêu đề sản phẩm không khớp. Mong đợi: '{expected_title}', nhưng nhận được: '{actual_title}'"

# 21. test thêm 2 sản phẩm ngay trang chính
def test_add_two_products_to_cart(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(3)  # Thời gian chờ để trang tải

    # Đợi để trang tải
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
    time.sleep(2)  # Thời gian chờ thêm sau khi tải xong hình ảnh

    # Nhấp vào nút "Add to Cart" cho sản phẩm thứ nhất
    add_to_cart_button_1 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button_1)
    time.sleep(2)  # Thời gian chờ sau khi thêm sản phẩm thứ nhất

    # Nhấp vào nút "Add to Cart" cho sản phẩm thứ hai
    add_to_cart_button_2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-home/div/div[2]/div/div[2]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button_2)
    time.sleep(2)  # Thời gian chờ sau khi thêm sản phẩm thứ hai

    # Nhấp vào giỏ hàng để kiểm tra sản phẩm
    cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[mat-icon[contains(text(), 'shopping_cart')]]"))
    )
    driver.execute_script("arguments[0].click();", cart_button)

    # Đợi trang giỏ hàng tải
    time.sleep(2)

    # Kiểm tra sản phẩm thứ nhất có trong giỏ hàng
    product_1_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[1]/table/tbody/tr[1]/td[2]"))
    )
    assert product_1_name.is_displayed(), "Sản phẩm thứ nhất không có trong giỏ hàng."

    # Kiểm tra sản phẩm thứ hai có trong giỏ hàng
    product_2_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[1]/table/tbody/tr[2]/td[2]"))
    )
    assert product_2_name.is_displayed(), "Sản phẩm thứ hai không có trong giỏ hàng."

    print("Kiểm tra giỏ hàng thành công: Cả hai sản phẩm đã được thêm vào giỏ hàng.")

# 22. test xem giỏ hàng
def test_view_cart(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(5)  # Thời gian chờ để trang tải

    # Đợi để trang tải
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
    time.sleep(3)  # Thời gian chờ thêm sau khi tải xong hình ảnh

    # Nhấp vào sản phẩm cụ thể
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/books/details/85']"))  # ID sản phẩm là 85
    )
    time.sleep(2)  # Thời gian chờ trước khi nhấp vào sản phẩm

    # Cuộn đến phần tử trước khi nhấp
    driver.execute_script("arguments[0].scrollIntoView(true);", product_link)
    time.sleep(2)  # Đợi để cuộn hoàn tất
    driver.execute_script("arguments[0].click();", product_link)
    time.sleep(3)  # Đợi cho trang sản phẩm tải

    # Nhấp vào nút "Add to Cart" bằng đường dẫn XPath mới
    add_to_cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-book-details/mat-card/mat-card-content/div[2]/div/app-addtocart/button"))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button)
    time.sleep(2)  # Thời gian chờ sau khi nhấp vào "Add to Cart"

    # Nhấp vào giỏ hàng
    cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[mat-icon[contains(text(), 'shopping_cart')]]"))
    )
    driver.execute_script("arguments[0].click();", cart_button)
    time.sleep(5)  # Đợi trang giỏ hàng tải

    # Kiểm tra URL sau khi nhấp vào giỏ hàng
    assert driver.current_url == "https://bookcart.azurewebsites.net/shopping-cart", "Chuyển trang giỏ hàng không thành công."

    # Assert kiểm tra sản phẩm có trong giỏ hàng
    cart_product = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'All of Us with Wings')]"))
    )
    assert cart_product.is_displayed(), "Sản phẩm không có trong giỏ hàng."

    print("Kiểm tra giỏ hàng thành công: Sản phẩm đã được thêm vào giỏ hàng.")

# dùng cho hàm test_calculate_cart_total()
#hàm thêm sp xong r kiểm tra ss tên  với giỏ hàng
def add_to_cart(driver, quantity=3):
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Thời gian chờ để đảm bảo trang đã tải

    # Đăng nhập vào hệ thống
    username = "heheee"
    password = "Linh123456789"

    try:
        # Nhấn vào nút đăng nhập
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(2)

        # Nhập tên đăng nhập
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )   #Xác minh rằng phần tử hiển thị trên giao diện
        username_field.send_keys(username)

        # Nhập mật khẩu
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)

        # Nhấn nút xác nhận đăng nhập
        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(5)

        # Kiểm tra đăng nhập thành công
        success_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' heheee']"))
        )
        assert success_indicator is not None, "Đăng nhập không thành công: không tìm thấy phần tử xác nhận đăng nhập."
        print("Đăng nhập thành công. Tiến hành tìm kiếm sản phẩm...")

    except Exception as e:
        print(f"Đăng nhập thất bại với lỗi: {e}")
        return []  # Trả về danh sách rỗng nếu đăng nhập thất bại

    try:
        # Tìm tất cả sản phẩm trên trang
        products = WebDriverWait(driver, 15).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//app-book-card"))
        )

        # Chỉ lấy số sản phẩm theo yêu cầu
        product_count = min(quantity, len(products))  # Số lượng sản phẩm cần thêm vào giỏ hàng
        added_products = []  # Danh sách lưu trữ tên sản phẩm đã thêm

        for i in range(product_count):
            product = products[i]

            # Lấy tên sản phẩm
            product_name = product.find_element(By.XPATH, ".//strong").text
            added_products.append(product_name)  # Lưu tên sản phẩm đã thêm

            # Nhấn vào nút "Thêm vào giỏ hàng" cho sản phẩm hiện tại
            add_to_cart_button = product.find_element(By.XPATH, ".//button[contains(., 'Add to Cart')]")
            add_to_cart_button.click()

            # Kiểm tra thông báo thành công
            try:
                success_message = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.mdc-snackbar__label'))
                )
                assert "one item added to cart" in success_message.text.lower(), f"Sản phẩm '{product_name}' chưa được thêm vào giỏ hàng."
            except TimeoutException:
                assert False, "Thông báo thêm sản phẩm vào giỏ hàng không xuất hiện."

            # Quay lại trang chính để thêm tiếp sp khác
            driver.get("https://bookcart.azurewebsites.net/")
            products = WebDriverWait(driver, 15).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//app-book-card"))
            )

        # Hiển thị các sản phẩm đã thêm
        print("Danh sách sản phẩm đã thêm vào giỏ hàng:", added_products)   # in ra tên các sp đã thêm vào giỏ hàng

        # Nhấn vào biểu tượng giỏ hàng
        cart_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        cart_icon.click()

        # Kiểm tra xem tên sản phẩm đã được thêm vào giỏ hàng chưa
        for product_name in added_products:
            try:
                product_in_cart = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//td[contains(@class, 'mat-column-title')]//a[text()='{product_name}']"))
                )
                assert product_in_cart.is_displayed(), f"Sản phẩm '{product_name}' không có trong giỏ hàng."
            except TimeoutException:
                assert False, f"Sản phẩm '{product_name}' không xuất hiện trong giỏ hàng."

        print(f"Tất cả {product_count} sản phẩm đã được thêm vào giỏ hàng thành công!")
        return added_products  # Trả về danh sách các sản phẩm đã thêm

    except TimeoutException:
        assert False, "Không tìm thấy danh sách sản phẩm sau khi đăng nhập."

# 23. test tổng giá tiền giỏ hàng
def test_calculate_cart_total(driver):
    # Đăng nhập và thêm một số sản phẩm vào giỏ hàng trước khi kiểm tra
    quantity_to_add = 3
    added_products = add_to_cart(driver, quantity=quantity_to_add)

    # Mở giỏ hàng
    cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]")
        )
    )
    cart_icon.click()
    time.sleep(5)  # Thêm thời gian chờ để đảm bảo giao diện được tải hoàn chỉnh

    try:
        # Lấy tất cả các sp trong giỏ hàng
        cart_items = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//app-shoppingcart//table/tbody/tr"))
        )
        time.sleep(2)  # Chờ thêm thời gian để đảm bảo dữ liệu được tải

        # Tính tổng giá trị giỏ hàng
        total_price = 0.0
        for item in cart_items:
            # Lấy giá của sản phẩm
            price_xpath = ".//td[contains(@class, 'mat-column-price')]"
            price_element = item.find_element(By.XPATH, price_xpath)
            price_text = price_element.text.strip()

            # Chuyển đổi giá trị về số
            if '₹' in price_text:
                item_price = float(price_text.replace('₹', '').replace(',', '').strip())
            elif '$' in price_text:
                item_price = float(price_text.replace('$', '').replace(',', '').strip())
            else:
                raise ValueError(f"Không nhận diện được ký hiệu tiền tệ: {price_text}")

            # Lấy số lượng của sản phẩm
            quantity_xpath = ".//td[contains(@class, 'mat-column-quantity')]//div[2]"  # Sử dụng div thứ hai
            quantity_element = item.find_element(By.XPATH, quantity_xpath)
            quantity_text = quantity_element.text.strip()
            item_quantity = int(quantity_text)

            # Cập nhật tổng giá tiền
            total_price += item_price * item_quantity

        # Kiểm tra tổng giá trị hiển thị trong giỏ hàng
        total_value_xpath = "//app-shoppingcart//td[contains(@class, 'mat-column-action')]/strong[not(contains(text(), 'Cart Total:'))]"
        displayed_total_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, total_value_xpath))
        )
        time.sleep(2)  # Chờ thêm để đảm bảo giá trị tổng được tải đầy đủ

        # Lấy nội dung văn bản và loại bỏ các phần không cần thiết
        displayed_total_text = displayed_total_element.text.strip()

        # In ra giá trị để kiểm tra
        print(f"Giá trị tổng giỏ hàng hiển thị: '{displayed_total_text}'")

        # Chuyển đổi thành số
        if '₹' in displayed_total_text:
            total_value_text = displayed_total_text.replace('₹', '').replace(',', '').strip()
        else:
            raise ValueError(f"Không nhận diện được ký hiệu tiền tệ: {displayed_total_text}")

        # Kiểm tra nếu total_value_text là chuỗi rỗng
        if not total_value_text:
            raise ValueError("Giá trị tổng giỏ hàng không hợp lệ, chuỗi rỗng.")

        # Chuyển đổi thành float
        displayed_total_value = float(total_value_text)

        print(f"Tổng giá trị giỏ hàng: {displayed_total_value}")  # In ra tổng giá trị

        # So sánh tổng giá trị tính toán với tổng giá trị hiển thị
        assert abs(displayed_total_value - total_price) < 0.01, \
            f"Tổng giá trị trong giỏ hàng không chính xác. Mong muốn: {total_price}, thực tế: {displayed_total_value}."

        print(f"Tổng giá trị giỏ hàng được tính toán thành công: ${total_price:.2f}")
        print("Tổng giá trị trong giỏ hàng chính xác.")

    except TimeoutException:
        raise Exception("Không thể mở giỏ hàng hoặc không tìm thấy sản phẩm trong giỏ hàng.")

# 24. test clear cart
def test_clear_cart(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(3)  # Thời gian chờ để trang tải

    # Đợi để trang tải hoàn toàn (chờ hình ảnh tải lên)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
    time.sleep(2)  # Thời gian chờ thêm sau khi tải xong hình ảnh

    # Nhấp vào "romance" để vào danh mục sản phẩm
    romance = driver.find_element(By.XPATH,
                                  "/html/body/app-root/div/app-home/div/div[1]/div/app-book-filter/mat-nav-list/mat-list-item[6]")
    romance.click()
    time.sleep(2)  # Đợi để trang sản phẩm romance tải xong

    # Lấy danh sách các nút "Add to cart" trong các sản phẩm
    add_to_cart_buttons = [
        "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button",
        "/html/body/app-root/div/app-home/div/div[2]/div/div[2]/app-book-card/mat-card/mat-card-content/app-addtocart/button",
        "/html/body/app-root/div/app-home/div/div[2]/div/div[3]/app-book-card/mat-card/mat-card-content/app-addtocart/button",
        "/html/body/app-root/div/app-home/div/div[2]/div/div[4]/app-book-card/mat-card/mat-card-content/app-addtocart/button",
        "/html/body/app-root/div/app-home/div/div[2]/div/div[6]/app-book-card/mat-card/mat-card-content/app-addtocart/button"
    ]

    # Thêm các sản phẩm vào giỏ hàng và cuộn trang từ từ
    for button_xpath in add_to_cart_buttons:
        # Cuộn xuống sản phẩm để nút "Add to cart" có thể nhấp được
        product = driver.find_element(By.XPATH, button_xpath)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", product)
        time.sleep(1)  # Thời gian chờ giữa các lần cuộn

        # Đợi nút "Add to cart" có thể nhấp được
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))

        # Nhấn nút "Add to cart"
        add_button = driver.find_element(By.XPATH, button_xpath)
        add_button.click()
        time.sleep(1)  # Thời gian chờ giữa các lần thêm vào giỏ hàng

    # Nhấp vào giỏ hàng
    cart_button_xpath = "//button[mat-icon[contains(text(), 'shopping_cart')]]"
    try:
        # Đợi cho nút giỏ hàng có thể nhấp được
        cart_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, cart_button_xpath))
        )
        # Nhấp vào giỏ hàng
        driver.execute_script("arguments[0].click();", cart_button)
        time.sleep(2)  # Đợi trang giỏ hàng tải
    except TimeoutException:
        assert False, "Không thể nhấp vào giỏ hàng trong thời gian chờ."
    except Exception as e:
        assert False, f"Có lỗi xảy ra: {str(e)}"

    # Nhấp vào nút Clear Cart
    clear_cart_button_xpath = "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-header/div[2]/button"
    try:
        # Đợi nút Clear Cart có thể nhấp được
        clear_cart_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, clear_cart_button_xpath))
        )
        # Nhấn nút Clear Cart
        clear_cart_button.click()
        time.sleep(2)  # Đợi sau khi nhấp vào Clear Cart
    except TimeoutException:
        assert False, "Không thể nhấp vào nút Clear Cart trong thời gian chờ."
    except Exception as e:
        assert False, f"Có lỗi xảy ra khi nhấp vào Clear Cart: {str(e)}"

    # Kiểm tra thông báo giỏ hàng trống
    empty_cart_message_xpath = "//mat-card-title[contains(text(), 'Your shopping cart is empty.')]"
    try:
        # Kiểm tra nếu thông báo giỏ hàng trống xuất hiện
        empty_cart_message = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, empty_cart_message_xpath))
        )
        # Kiểm tra nếu thông báo giỏ hàng trống là đúng
        assert empty_cart_message.is_displayed(), "Thông báo giỏ hàng không trống không hiển thị!"
        print("Giỏ hàng đã được xóa thành công.")
    except TimeoutException:
        assert False, "Không tìm thấy thông báo giỏ hàng trống."
    except Exception as e:
        assert False, f"Có lỗi xảy ra khi kiểm tra thông báo giỏ hàng trống: {str(e)}"

# 25.test tăng giảm số lượng sản phẩm
def test_adjust_quantity(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(3)  # Thời gian chờ để trang tải

    # Đợi để trang tải
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
    time.sleep(2)  # Thời gian chờ thêm sau khi tải xong hình ảnh

    # Nhấp vào nút "Add to Cart" cho sản phẩm thứ nhất
    add_to_cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button)
    time.sleep(2)  # Thời gian chờ sau khi thêm sản phẩm

    # Nhấp vào giỏ hàng
    cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[mat-icon[contains(text(), 'shopping_cart')]]"))
    )
    driver.execute_script("arguments[0].click();", cart_button)

    # Đợi trang giỏ hàng tải
    time.sleep(2)

    # Nhấp vào nút để tăng số lượng sản phẩm 4 lần
    for _ in range(4):  # Nhấp 4 lần để tăng số lượng lên 5
        increase_quantity_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[mat-icon[contains(text(), 'add_circle')]]"))
        )
        driver.execute_script("arguments[0].click();", increase_quantity_button)
        time.sleep(1)  # Thời gian chờ sau mỗi lần nhấp

    # Thời gian chờ thêm sau khi tăng số lượng
    time.sleep(3)

    # Kiểm tra số lượng sản phẩm đã tăng lên 5 hay chưa
    quantity_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH,
                                        "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[1]/table/tbody/tr/td[4]/div/div[2]"))
    )

    # In nội dung phần tử để kiểm tra
    print("Nội dung phần tử số lượng sau khi tăng:", quantity_element.text)

    try:
        actual_quantity = int(quantity_element.text)
        assert actual_quantity == 5, f"Số lượng sản phẩm không chính xác. Mong đợi: 5, nhưng nhận được: {actual_quantity}"
        print("Kiểm tra tăng số lượng sản phẩm thành công: Số lượng sản phẩm đã tăng lên 5.")

        # Giảm số lượng sản phẩm 1 lần
        decrease_quantity_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[mat-icon[contains(text(), 'remove_circle')]]"))
        )
        driver.execute_script("arguments[0].click();", decrease_quantity_button)
        time.sleep(3)  # Thời gian chờ sau khi giảm số lượng

        # Thời gian chờ thêm sau khi giảm số lượng
        time.sleep(3)

        # Kiểm tra số lượng sản phẩm đã giảm xuống còn 4 hay chưa
        quantity_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[1]/table/tbody/tr/td[4]/div/div[2]"))
        )

        # In nội dung phần tử để kiểm tra
        print("Nội dung phần tử số lượng sau khi giảm:", quantity_element.text)

        actual_quantity = int(quantity_element.text)
        assert actual_quantity == 4, f"Số lượng sản phẩm không chính xác sau khi giảm. Mong đợi: 4, nhưng nhận được: {actual_quantity}"
        print("Kiểm tra giảm số lượng sản phẩm thành công: Số lượng sản phẩm đã giảm xuống còn 4.")

    except ValueError:
        print("Lỗi: không thể chuyển đổi nội dung phần tử thành số nguyên.")

# 26. test checkout
def test_checkout(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(5)  # Chờ để trang tải

    # Đợi để trang tải
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
    time.sleep(3)  # Thời gian chờ thêm sau khi tải xong hình ảnh

    # Nhấp vào sản phẩm cụ thể
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/books/details/85']"))  # ID sản phẩm là 85
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", product_link)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", product_link)
    time.sleep(3)  # Đợi cho trang sản phẩm tải

    # Nhấp vào nút "Add to Cart"
    add_to_cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-book-details/mat-card/mat-card-content/div[2]/div/app-addtocart/button"))
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button)
    time.sleep(2)

    # Nhấp vào giỏ hàng
    cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//mat-icon[contains(text(), 'shopping_cart')]]"))
    )
    driver.execute_script("arguments[0].click();", cart_button)
    time.sleep(5)

    # Kiểm tra URL của giỏ hàng
    assert driver.current_url == "https://bookcart.azurewebsites.net/shopping-cart", "Không chuyển đến trang giỏ hàng."

    # Kiểm tra sản phẩm có trong giỏ hàng
    cart_product = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'All of Us with Wings')]"))
    )
    assert cart_product.is_displayed(), "Sản phẩm không có trong giỏ hàng."

    # Nhấp vào nút "CheckOut" và sẽ chuyển đến trang đăng nhập
    checkout_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()=' CheckOut ']]"))
    )
    driver.execute_script("arguments[0].click();", checkout_button)
    time.sleep(5)  # Đợi trang đăng nhập tải

    # Nhập tên người dùng
    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
    )
    username_input.send_keys("heheee")
    time.sleep(1)

    # Nhập mật khẩu
    password_input = driver.find_element(By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input")
    password_input.send_keys("Linh123456789")
    time.sleep(1)

    # Nhấn nút "Login"
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-card-actions/button"))
    )
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(5)  # Đợi chuyển sang trang thanh toán

    # Kiểm tra chuyển đến trang thanh toán
    assert driver.current_url == "https://bookcart.azurewebsites.net/checkout", "Không chuyển đến trang thanh toán sau khi đăng nhập."
    # Nhập thông tin thanh toán
    # Điền Name
    name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/app-checkout/mat-card/mat-card-content/div/div[1]/mat-card-content/form/mat-form-field[1]/div[1]//input"))
    )
    name_input.send_keys("Võ Khánh Linh")
    time.sleep(1)

    # Điền Address Line 1
    address_line1_input = driver.find_element(By.XPATH, "/html/body/app-root/div/app-checkout/mat-card/mat-card-content/div/div[1]/mat-card-content/form/mat-form-field[2]/div[1]//input")
    address_line1_input.send_keys("1234")
    time.sleep(1)

    # Điền Address Line 2
    address_line2_input = driver.find_element(By.XPATH, "/html/body/app-root/div/app-checkout/mat-card/mat-card-content/div/div[1]/mat-card-content/form/mat-form-field[3]/div[1]//input")
    address_line2_input.send_keys("324")
    time.sleep(1)

    # Điền Pincode
    pincode_input = driver.find_element(By.XPATH, "/html/body/app-root/div/app-checkout/mat-card/mat-card-content/div/div[1]/mat-card-content/form/mat-form-field[4]/div[1]//input")
    pincode_input.send_keys("234355")
    time.sleep(1)

    # Điền State
    state_input = driver.find_element(By.XPATH, "/html/body/app-root/div/app-checkout/mat-card/mat-card-content/div/div[1]/mat-card-content/form/mat-form-field[5]/div[1]//input")
    state_input.send_keys("Ho Chi Minh City")
    time.sleep(1)

    # Nhấp nút Place Order
    place_order_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-checkout/mat-card/mat-card-content/div/div[1]/mat-card-content/form/mat-card-actions/button[1]"))
    )
    driver.execute_script("arguments[0].click();", place_order_button)
    time.sleep(5)  # Chờ chuyển trang

    # Kiểm tra chuyển sang trang myorders
    assert driver.current_url == "https://bookcart.azurewebsites.net/myorders", "Checkout không thành công."
    print("Checkout thành công.")

#27. Kiểm tra xem ứng dụng có chuyển đến trang đăng nhập khi checkout mà chưa đăng nhập
def test_checkout_without_login(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(5)  # Chờ để trang tải

    # Thử nhấn vào nút "Thêm vào giỏ hàng" mà không đăng nhập
    try:
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
        )
        add_to_cart_button.click()
        time.sleep(2)  # Tạm dừng 2 giây để quan sát

    except TimeoutException:
        print("Không tìm thấy nút 'Thêm vào giỏ hàng'.")
        return

    # Nhấn vào biểu tượng giỏ hàng
    try:
        cart_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[1]"))
        )
        cart_icon.click()
        time.sleep(5)  # Tạm dừng 5 giây để quan sát

    except TimeoutException:
        print("Không tìm thấy biểu tượng giỏ hàng.")
        return

    # Nhấn vào nút "Checkout"
    try:
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[2]/td[6]/button"))
        )
        checkout_button.click()
        time.sleep(2)  # Tạm dừng 2 giây để kiểm tra quá trình chuyển hướng

        # Kiểm tra URL hiện tại xem có phải là trang đăng nhập không
        current_url = driver.current_url
        assert "login" in current_url.lower(), f"Ứng dụng không chuyển hướng đến trang đăng nhập khi checkout mà không đăng nhập. URL hiện tại: {current_url}"

        print("Chuyển hướng đến trang đăng nhập thành công.")

    except TimeoutException:
        print("Không tìm thấy nút 'Checkout' hoặc có thể đã chuyển hướng đến trang đăng nhập tự động.")
    except AssertionError as e:
        print(str(e))

    # In ra URL hiện tại để xác nhận
    print("URL hiện tại:", driver.current_url)


# ****************SEARCH********************

# 6. test tìm kiếm khi nhấn enter (lỗi)
def test_search_product_enter(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Thời gian chờ để trang tải

    # Tìm kiếm sản phẩm
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
    )
    search_box.send_keys("Harry Potter and the Chamber of Secrets")
    time.sleep(1)  # Thời gian chờ để thấy thao tác

    # Nhấn Enter để tìm kiếm
    search_box.send_keys(u'\ue007')  # Gửi phím Enter
    time.sleep(5)  # Chờ để xem kết quả tìm kiếm

    # Kiểm tra kết quả tìm kiếm
    try:
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Harry Potter and the Chamber of Secrets')]"))
        )
        assert result.is_displayed(), "Không tìm thấy sản phẩm 'Harry Potter and the Chamber of Secrets' trong kết quả tìm kiếm."
        print("Tìm kiếm thành công cho sản phẩm: 'Harry Potter and the Chamber of Secrets'")
    except TimeoutException:
        assert False, "Không tìm thấy sản phẩm 'Harry Potter and the Chamber of Secrets' trong kết quả tìm kiếm."

# 7. test tìm kiếm slayer rồi chọn trên đề xuất mới hiện sản phẩm
def test_search_for_slayer(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(7)  # Thời gian chờ để trang tải

    # Nhấp vào ô tìm kiếm
    search_box = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='search' and @placeholder='Search books or authors']"))
    )
    search_box.click()
    time.sleep(2)  # Thời gian chờ sau khi nhấp vào ô tìm kiếm

    # Nhập từ khóa tìm kiếm
    search_box.send_keys("slayer")
    time.sleep(3)  # Thời gian chờ để gợi ý hiện ra

    # Nhấp vào gợi ý sản phẩm
    suggestion = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-option[contains(@class, 'mat-mdc-option') and .//span[text()=' Slayer ']]"))
    )
    suggestion.click()
    time.sleep(7)  # Thời gian chờ để trang sản phẩm tải

    # Kiểm tra xem sản phẩm có tên là "Slayer" hay không
    product_name_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//strong[contains(text(), 'Slayer')]"))
    )

    # In nội dung phần tử để kiểm tra
    print("Tên sản phẩm:", product_name_element.text)

    # Kiểm tra tên sản phẩm
    assert product_name_element.text == "Slayer", f"Tên sản phẩm không chính xác. Mong đợi: Slayer, nhưng nhận được: {product_name_element.text}"
    print("Kiểm tra tìm kiếm sản phẩm thành công: Tên sản phẩm là 'Slayer'.")

# 8. test tìm kiếm theo price
def test_filter_price(driver):
    # Mở trang chính
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(5)  # Chờ để trang tải hoàn tất

    # Đợi để thanh trượt xuất hiện
    slider = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/app-home/div/div[1]/div/app-price-filter/mat-card/mat-card-content[1]/mat-slider/input"))
    )
    time.sleep(3)  # Thời gian chờ để thanh trượt sẵn sàng

    # Đặt giá trị thanh trượt trực tiếp bằng JavaScript và kích hoạt sự kiện 'input' và 'change'
    driver.execute_script("""
    arguments[0].value = 311; 
    arguments[0].dispatchEvent(new Event('input'));
    arguments[0].dispatchEvent(new Event('change'));
    """, slider)
    time.sleep(3)  # Đợi để trang cập nhật kết quả

    # Kiểm tra giá trị của thanh trượt sau khi điều chỉnh có đúng 311 k
    slider_value = driver.execute_script("return arguments[0].value", slider)
    assert int(slider_value) == 311, f"Thanh trượt không được đặt đúng mức 311, mà là {slider_value}"

    # Cuộn trang từ từ để thấy các sản phẩm
    for _ in range(5):  # Số lần cuộn trang (có thể điều chỉnh)
        driver.execute_script("window.scrollBy(0, 300);")  # Cuộn 300px mỗi lần
        time.sleep(1)  # Thời gian chờ mỗi lần cuộn

    # Lấy giá tiền sản phẩm hiển thị trên trang
    prices = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//p[contains(text(), '₹')]"))
    )

    # Kiểm tra giá tiền từng sản phẩm để đảm bảo giá <= 311
    for price in prices:
        # Lấy giá trị và làm sạch khoảng trắng, ký tự không cần thiết
        price_text = price.text.replace("₹", "").replace(",", "").strip()

        try:
            # Chuyển đổi giá trị chuỗi thành số nguyên
            price_value = int(float(price_text))
        except ValueError:
            print(f"Không thể chuyển đổi giá trị: {price.text}")
            continue  # Bỏ qua giá trị không chuyển đổi được

        # Kiểm tra điều kiện
        assert price_value <= 311, f"Giá {price_value} lớn hơn 311"

    print("Tất cả giá sản phẩm đều <= 311")

# mới thêm
# 9. kiểm tra tìm kiếm order
def test_search_my_orders(driver):
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)  # Đợi trang tải

    username = "heheee"
    password = "Linh123456789"

    try:
        # Nhấn vào nút đăng nhập
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        login_button.click()
        time.sleep(3)  # Đợi sau khi nhấn nút đăng nhập

        # Nhập tên người dùng và mật khẩu
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
        )
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
        )
        password_field.send_keys(password)
        time.sleep(2)  # Đợi sau khi nhập tên và mật khẩu

        # Nhấn nút `Login`
        login_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
        )
        login_submit_button.click()
        time.sleep(5)  # Đợi sau khi nhấn nút Login

        # Kiểm tra đăng nhập thành công
        success_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' heheee']"))
        )
        assert success_indicator is not None, "Đăng nhập không thành công."
        print("Đăng nhập thành công.")
        time.sleep(2)  # Đợi sau khi xác nhận đăng nhập thành công

        # Mở menu người dùng
        user_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]"))
        )
        user_button.click()
        time.sleep(2)  # Đợi sau khi nhấn vào menu người dùng

        # Nhấn chọn `My Orders`
        my_orders_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='My Orders']]"))
        )
        my_orders_button.click()
        time.sleep(5)  # Đợi sau khi nhấn vào "My Orders"

        # Tìm kiếm đơn hàng
        search_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-my-orders/mat-card/div/mat-card-content/mat-form-field/div[1]/div/div[2]/input"))
        )
        search_input.send_keys("171-197788")  # Nhập mã đơn hàng để tìm kiếm
        time.sleep(3)  # Đợi sau khi nhập mã đơn hàng

        # Kiểm tra kết quả tìm kiếm
        result_table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/app-root/div/app-my-orders/mat-card/div/mat-card-content/div/table"))
        )
        time.sleep(2)  # Đợi sau khi bảng kết quả được hiển thị

        result_row = driver.find_element(By.XPATH, "//tr[td[contains(text(), '171-197788')]]")
        time.sleep(2)  # Đợi sau khi tìm kiếm kết quả

        # Kiểm tra kết quả có chứa mã đơn hàng tìm kiếm
        assert result_row is not None, "Không tìm thấy đơn hàng với mã '171-197788'."
        print("Đã tìm thấy đơn hàng với mã '171-197788'.")

        # Thực hiện thêm các bước kiểm tra khác nếu cần (ví dụ: kiểm tra chi tiết đơn hàng)
    except Exception as e:
        assert False, f"Kiểm thử thất bại với lỗi: {e}"


# *****************REPONSIVE DESIGN**************

# kiểm tra khi phóng to thu nhỏ
def _test_responsive_design_for_size(driver, width, height):
    failed_checks = []  # Danh sách để lưu các phần tử không hiển thị đúng

    try:
        # Đặt kích thước cửa sổ theo từng màn hình
        driver.set_window_size(width, height)
        print(f"Kiểm tra giao diện ở kích thước: {width}x{height}")

        # Kiểm tra xem logo có hiển thị đúng không
        try:
            icon = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//mat-icon[text()='book']"))
            )
            assert icon.is_displayed(), f"Logo không hiển thị đúng cách ở kích thước {width}x{height}"
        except Exception as e:
            failed_checks.append(f"Logo không hiển thị đúng ở kích thước {width}x{height}: {e}")  #thêm

        # Kiểm tra thanh điều hướng ở chế độ mobile (menu icon)
        if (width <= 768) and (width, height) != (375, 667):  # Bỏ qua kiểm tra menu icon với kích thước 375x667
            try:
                menu_icon = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]"))
                )
                assert menu_icon.is_displayed(), f"Menu icon không hiển thị ở chế độ mobile tại kích thước {width}x{height}"
            except Exception as e:
                failed_checks.append(f"Menu icon không hiển thị ở chế độ mobile tại kích thước {width}x{height}: {e}")
        else:  # Với màn hình lớn
            navbar_buttons = driver.find_elements(By.XPATH,
                                                  "//div[@class='d-flex align-items-center']//button")
            try:
                assert len(
                    navbar_buttons) > 0, f"Các liên kết điều hướng không hiển thị ở chế độ desktop tại kích thước {width}x{height}"
            except AssertionError as e:
                failed_checks.append(
                    f"Các liên kết điều hướng không hiển thị ở chế độ desktop tại kích thước {width}x{height}: {e}")

        # Kiểm tra liên kết Swagger và GitHub, nhưng bỏ qua đối với kích thước cụ thể
        if (width, height) != (375, 667) and (width, height) != (768, 1024):
            # Kiểm tra liên kết Swagger
            try:
                swagger_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='/swagger/index.html']"))
                )
                assert swagger_link.is_displayed(), f"Liên kết Swagger không hiển thị ở kích thước {width}x{height}"
            except Exception as e:
                failed_checks.append(f"Liên kết Swagger không hiển thị ở kích thước {width}x{height}: {e}")

            # Kiểm tra liên kết GitHub
            try:
                github_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='https://github.com/AnkitSharma-007/bookcart']"))
                )
                assert github_link.is_displayed(), f"Liên kết GitHub không hiển thị ở kích thước {width}x{height}"
            except Exception as e:
                failed_checks.append(f"Liên kết GitHub không hiển thị ở kích thước {width}x{height}: {e}")

        # Kiểm tra nếu có bất kỳ phần tử nào không hiển thị đúng
        if len(failed_checks) > 0:
            print(f"Tổng cộng có {len(failed_checks)} lỗi khi kiểm tra giao diện: ")
            for error in failed_checks:
                print(f"- {error}")
        assert len(failed_checks) == 0, f"Có {len(failed_checks)} lỗi khi kiểm tra giao diện: {failed_checks}"

    except Exception as e:
        print(f"Lỗi khi kiểm tra ở kích thước {width}x{height}: {e}")
        assert False, f"Lỗi ở kích thước {width}x{height}: {e}"


# 28 Test cho các kích thước màn hình khác nhau
def test_responsive_small(driver):
    # Đầu tiên, thực hiện đăng nhập trước
    test_login(driver)  # Đảm bảo driver được truyền vào trong hàm login
    # Kích thước màn hình: iPhone 8
    width, height = 375, 667
    _test_responsive_design_for_size(driver, width, height)

#29
def test_responsive_ipad(driver):
    # Đầu tiên, thực hiện đăng nhập trước
    test_login(driver)
    # Kích thước màn hình: iPad
    width, height = 768, 1024
    _test_responsive_design_for_size(driver, width, height)

#30
def test_responsive_tablet(driver):
    # Đầu tiên, thực hiện đăng nhập trước
    test_login(driver)
    # Kích thước màn hình: Tablet
    width, height = 1280, 800
    _test_responsive_design_for_size(driver, width, height)

#31
def test_responsive_desktop(driver):
    # Đầu tiên, thực hiện đăng nhập trước
    test_login(driver)
    # Kích thước màn hình: Desktop Full HD
    width, height = 1920, 1080
    _test_responsive_design_for_size(driver, width, height)
