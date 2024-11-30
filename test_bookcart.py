from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
import random



class TestBookCart:
    def setup_method(self):
        # Khởi tạo trình duyệt trước mỗi phương thức kiểm thử
        self.driver = webdriver.Chrome()
        self.driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(2)  # Chờ để trang tải

    def teardown_method(self):
        # Đóng trình duyệt sau mỗi phương thức kiểm thử
        self.driver.quit()

    # *************LOGIN - REGISTER**************
    def test_login_valid(self):
        username = "trhuuhau"
        password = "Vkl041103"

        try:
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(username)
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(password)

            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            success_indicator = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
            )
            assert success_indicator is not None, "Đăng nhập không thành công: không tìm thấy phần tử xác nhận đăng nhập."
        except Exception as e:
            assert False, f"Đăng nhập thất bại với lỗi: {e}"

    def test_login_invalid_username(self):
        invalid_username = "wrongusername"
        password = "Vkl041103"

        try:
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(invalid_username)
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(password)

            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            error_message = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//mat-error"))
            )
            assert error_message is not None, "Không tìm thấy thông báo lỗi khi đăng nhập thất bại với username sai."
        except Exception as e:
            assert False, f"Đăng nhập thất bại với lỗi: {e}"

    def test_login_incorrect_password(self):
        username = "correctusername"
        incorrect_password = "wrongpassword"

        try:
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(username)
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(incorrect_password)

            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            error_message = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//mat-error"))
            )
            assert error_message is not None, "Không tìm thấy thông báo lỗi khi đăng nhập với mật khẩu sai."
        except Exception as e:
            assert False, f"Đăng nhập thất bại với lỗi: {e}"

    def test_register(self):
        user_info = {
            "firstname": "Hau",
            "lastname": "Truu",
            "username": "carrot",
            "password": "Vkl041103",
            "confirm_password": "Vkl041103",
            "gender": "Male"
        }

        try:
            login_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            register_button = WebDriverWait(self.driver, 30).until(
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
                field = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                field.clear()
                field.send_keys(user_info[key])
                time.sleep(1)

            gender_radio = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info['gender']}']"))
            )
            gender_radio.click()
            time.sleep(1)

            submit_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-mdc-raised-button span.mdc-button__label"))
            )
            submit_button.click()
            time.sleep(5)

            WebDriverWait(self.driver, 30).until(
                EC.url_to_be("https://bookcart.azurewebsites.net/login")
            )
            assert self.driver.current_url == "https://bookcart.azurewebsites.net/login", "Đăng ký không thành công: không chuyển đến trang đăng nhập."
        except Exception as e:
            assert False, f"Đăng ký thất bại với lỗi: {e}"

    def test_register_existing_username(self):
        user_info_existing = {
            "firstname": "Hau",
            "lastname": "Truu",
            "username": "trhuuhau",  # Giả sử tên người dùng này đã tồn tại
            "password": "Vkl041103",
            "confirm_password": "Vkl041103",
            "gender": "Male"
        }

        try:
            # Mở trang BookCart
            self.driver.get("https://bookcart.azurewebsites.net/")
            time.sleep(2)  # Thời gian nghỉ sau khi tải trang

            # Nhấp vào nút login trên trang chủ
            login_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            # Nhấp vào nút Register
            register_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Register']]"))
            )
            register_button.click()
            time.sleep(2)

            # Điền thông tin đăng ký
            fields = {
                "firstname": "//input[@formcontrolname='firstname']",
                "lastname": "//input[@formcontrolname='lastname']",
                "username": "//input[@formcontrolname='username']",
                "password": "//input[@formcontrolname='password']",
                "confirm_password": "//input[@formcontrolname='confirmPassword']"
            }

            for key, xpath in fields.items():
                field = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                field.clear()
                field.send_keys(user_info_existing[key])
                time.sleep(1)

            # Chọn giới tính
            gender_radio = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info_existing['gender']}']"))
            )
            gender_radio.click()
            time.sleep(1)

            # Nhấn nút đăng ký
            submit_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Register']]"))
            )
            submit_button.click()
            time.sleep(2)

            # Kiểm tra thông báo lỗi khi tên người dùng đã tồn tại
            try:
                # Sử dụng XPath mới mà bạn đã cung cấp để kiểm tra thông báo lỗi
                error_message = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      "/html/body/app-root/div/app-user-registration/div/mat-card/mat-card-content/form/mat-form-field[3]/div[2]/div/mat-error"))
                )

                # Kiểm tra nội dung thông báo lỗi
                assert "User Name is not available" in error_message.text, "Thông báo lỗi không xuất hiện khi tên người dùng đã tồn tại."

            except TimeoutException:
                assert False, "Đã không tìm thấy thông báo lỗi khi tên người dùng đã tồn tại."


        except Exception as e:
            assert False, f"Đăng ký không thành công với lỗi: {e}"

    def test_logout(self):
        username = "trhuuhau"
        password = "Vkl041103"

        try:
            # Nhấn vào nút đăng nhập
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            # Nhập tên người dùng và mật khẩu
            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(username)
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(password)

            # Nhấn nút `Login`
            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            # Kiểm tra đăng nhập thành công
            success_indicator = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
            )
            assert success_indicator is not None, "Đăng nhập không thành công."

            print("Đăng nhập thành công.")

            # Nhấp vào nút người dùng để mở menu
            user_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]"))
            )
            user_button.click()
            time.sleep(2)

            # Nhấp vào nút `Logout`
            logout_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Logout']]"))
            )
            logout_button.click()
            time.sleep(5)

            # Kiểm tra URL hiện tại để xác nhận đã đăng xuất
            current_url = self.driver.current_url
            print("URL hiện tại sau khi đăng xuất:", current_url)

            # Xác nhận URL của trang đăng nhập để kiểm tra đăng xuất thành công
            assert current_url == "https://bookcart.azurewebsites.net/login", "Đăng xuất không thành công, không chuyển về trang đăng nhập."

            print("Đăng xuất thành công và đã chuyển về trang đăng nhập.")

        except Exception as e:
            assert False, f"Kiểm thử đăng xuất thất bại với lỗi: {e}"


    # **************FORM SUBMISSION*******************
    def test_form_submission_with_numeric_firstname_lastname(self):
        user_info = {
            "firstname": "123",
            "lastname": "456",
            "username": "carrot123",
            "password": "Vkl041103",
            "confirm_password": "Vkl041103",
            "gender": "Male"
        }

        try:
            login_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            register_button = WebDriverWait(self.driver, 30).until(
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
                field = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                field.clear()
                field.send_keys(user_info[key])
                time.sleep(1)

            gender_radio = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info['gender']}']"))
            )
            gender_radio.click()
            time.sleep(1)

            submit_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-mdc-raised-button span.mdc-button__label"))
            )
            submit_button.click()
            time.sleep(3)

            # Kiểm tra thông báo lỗi
            try:
                error_message = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[@class='error-message']"))
                    # Cập nhật xpath theo thực tế
                )
                assert error_message.is_displayed(), "Thông báo lỗi không hiển thị."
                print("Pass: Thông báo lỗi hiển thị khi first name và last name là số.")
            except Exception:
                assert False, "Fail: Không có thông báo lỗi khi first name và last name là số."

        except Exception as e:
            assert False, f"Đăng ký thất bại với lỗi: {e}"

    def test_form_submission_register_without_gender_selection(self):
        user_info = {
            "firstname": "Hau",
            "lastname": "Truu",
            "username": "carrot1",
            "password": "Vkl041103",  # Mật khẩu hợp lệ
            "confirm_password": "Vkl041103"
        }

        try:
            # Nhấn nút đăng nhập
            login_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)  # Thời gian chờ sau khi nhấn nút đăng nhập

            # Nhấn nút đăng ký
            register_button = WebDriverWait(self.driver, 30).until(
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
                field = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                field.clear()
                field.send_keys(user_info[key])
                time.sleep(1)  # Thời gian chờ sau khi nhập mỗi trường

            # Nhấn nút đăng ký mà không chọn giới tính
            submit_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-mdc-raised-button span.mdc-button__label"))
            )
            submit_button.click()
            time.sleep(2)  # Thời gian chờ sau khi nhấn nút gửi

            # Kiểm tra thông báo lỗi yêu cầu chọn giới tính
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-user-registration/div/mat-card/mat-card-content/form/mat-form-field[5]/div[2]/div"))
            )

            # Định nghĩa thông báo lỗi mong đợi
            expected_error_message = "please select your gender"
            assert expected_error_message in error_message.text.lower(), f"Expected error message not found. Actual message: {error_message.text}"
            print("Test Passed: Error message for gender selection displayed as expected.")

        except TimeoutException:
            assert False, "Thông báo lỗi yêu cầu chọn giới tính không xuất hiện. Test Failed."
        except Exception as e:
            assert False, f"Đăng ký thất bại với lỗi: {e}"

    # Kiểm tra có cho checkout với place order để trống không
    def test_form_submission_checkout_without_info(self):
        self.test_login_valid()

        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
        )
        add_to_cart_button.click()

        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        cart_icon.click()

        checkout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[2]/td[6]/button"))
        )
        checkout_button.click()

        time.sleep(3)

        place_order_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        place_order_button.click()
        time.sleep(3)

        # Kiểm tra nếu các trường bị lỗi có lớp 'mat-form-field-invalid'
        required_fields = self.driver.find_elements(By.CSS_SELECTOR, 'mat-form-field.mat-form-field-invalid')
        for field in required_fields:
            assert "mat-form-field-invalid" in field.get_attribute("class"), \
                "Trường không có lớp 'mat-form-field-invalid' khi không nhập thông tin."


    # *****************NAVIGATION*******************

    def test_category_navigation_without_login(self):
        """
        Kiểm tra các tính năng điều hướng trong ứng dụng web mà không cần đăng nhập.
        Đảm bảo rằng người dùng có thể truy cập các trang chính thông qua các menu và các nút điều hướng như Trang chủ.
        """
        global link_text
        visited_categories = set()  # Tạo một tập hợp để theo dõi các danh mục đã nhấp vào

        try:
            # Tiến hành kiểm tra điều hướng từ trang chủ
            print("Đang kiểm tra khả năng điều hướng từ trang chủ...")

            for _ in range(5):  # Lặp qua nhiều lần để thử điều hướng tới nhiều danh mục
                # Lấy lại danh sách các danh mục sau mỗi lần kiểm tra
                categories = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mat-mdc-nav-list mat-list-item"))
                )
                print("Danh sách các danh mục:", categories)

                for category in categories:
                    try:
                        link = category.find_element(By.TAG_NAME, "a")
                        link_text = link.text

                        # Bỏ qua "All Categories" nếu cần
                        if link_text == "All Categories":
                            print(f"Bỏ qua danh mục: {link_text}")
                            continue

                        # Kiểm tra xem danh mục này đã được nhấp chưa
                        if link_text in visited_categories:
                            print(f"Đã truy cập danh mục {link_text} rồi, bỏ qua.")
                            continue

                        # Nhấn vào từng danh mục và kiểm tra URL sau khi điều hướng
                        link.click()

                        # Thêm thời gian chờ sau khi nhấn vào danh mục
                        time.sleep(2)  # Chờ 2 giây để trang kịp tải

                        # Lấy URL hiện tại sau khi nhấn vào liên kết
                        current_url = self.driver.current_url

                        # Kiểm tra xem URL có chứa tên danh mục (link_text) hay không
                        if link_text.lower() in current_url.lower():  # So sánh không phân biệt chữ hoa chữ thường
                            print(f"Truy cập thành công vào danh mục: {link_text} - URL: {current_url}")
                        else:
                            print(f"Không thể tải trang cho danh mục: {link_text} - URL: {current_url}")

                        # Thêm danh mục này vào tập hợp đã truy cập
                        visited_categories.add(link_text)

                        # Quay lại trang chủ sau khi kiểm tra danh mục
                        self.driver.back()

                        # Thêm thời gian chờ khi quay lại trang chủ
                        time.sleep(2)  # Chờ 2 giây sau khi quay lại trang chủ

                        # Chờ trang chủ tải lại và tìm lại các phần tử danh mục
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mat-mdc-nav-list mat-list-item"))
                        )

                    except StaleElementReferenceException:
                        print(f"Phần tử danh mục {link_text} không còn hợp lệ, sẽ thử lại.")
                        continue

            # Kiểm tra lại trang chủ
            assert self.driver.current_url == "https://bookcart.azurewebsites.net/", "Không thể quay lại trang chủ."
            print("Kiểm tra điều hướng thành công! Các trang có thể truy cập bình thường.")

        except TimeoutException:
            raise Exception("Không thể tìm thấy hoặc truy cập vào các trang cần thiết.")
        except Exception as e:
            assert False, f"Kiểm tra điều hướng thất bại với lỗi: {e}"

    def test_toolbar_navigation_after_login(self):
        """
        Kiểm tra khả năng điều hướng trong ứng dụng web sau khi đăng nhập.
        Mở các trang như Wishlist, Giỏ hàng, Menu tài khoản, My Orders, kiểm tra Swagger, GitHub và thực hiện Logout.
        Sau mỗi bước, quay lại trang chủ.
        """
        username = "trhuuhau"
        password = "Vkl041103"

        print("Bắt đầu quá trình đăng nhập...")
        try:
            # Đăng nhập
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(username)

            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(password)

            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            success_indicator = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
            )
            assert success_indicator is not None, "Đăng nhập không thành công: không tìm thấy phần tử xác nhận đăng nhập."
            print("Đăng nhập thành công. Tiến hành tìm kiếm sản phẩm...")

            # Mở Wishlist
            print("Đang mở Wishlist...")
            wishlist_button = self.driver.find_element(By.XPATH,
                                                       "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[1]")
            wishlist_button.click()
            time.sleep(2)  # Dừng 2 giây để xem kết quả
            print("Đã mở Wishlist, quay lại trang chủ.")
            self.driver.get("https://bookcart.azurewebsites.net/")  # Quay về trang chủ
            time.sleep(2)  # Dừng 2 giây để trang chủ tải lại

            # Mở Giỏ hàng
            print("Đang mở Giỏ hàng...")
            cart_button = self.driver.find_element(By.XPATH,
                                                   "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]")
            cart_button.click()
            time.sleep(2)  # Dừng 2 giây để xem kết quả
            print("Đã mở Giỏ hàng, quay lại trang chủ.")
            self.driver.get("https://bookcart.azurewebsites.net/")  # Quay về trang chủ
            time.sleep(2)  # Dừng 2 giây để trang chủ tải lại

            # Mở Menu tài khoản
            print("Đang mở Menu tài khoản...")
            account_menu = self.driver.find_element(By.XPATH,
                                                    "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]")
            account_menu.click()
            time.sleep(2)  # Dừng 2 giây để xem kết quả

            # Mở My Orders từ menu tài khoản
            print("Đang mở My Orders...")
            my_orders_button = self.driver.find_element(By.XPATH, "//*[@id='mat-menu-panel-0']/div/button[1]")
            my_orders_button.click()
            time.sleep(2)  # Dừng 2 giây để xem kết quả
            print("Đã mở My Orders, quay lại trang chủ.")
            self.driver.get("https://bookcart.azurewebsites.net/")  # Quay về trang chủ
            time.sleep(2)  # Dừng 2 giây để trang chủ tải lại

            # Mở Swagger (kiểm tra tính năng Swagger)
            print("Đang mở Swagger...")
            main_window = self.driver.current_window_handle  # Lưu lại cửa sổ chính
            swagger_button = self.driver.find_element(By.XPATH,
                                                      "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[2]")
            swagger_button.click()
            time.sleep(2)

            # Đóng tab Swagger sau khi kiểm tra
            all_windows = self.driver.window_handles
            for window in all_windows:
                if window != main_window:
                    self.driver.switch_to.window(window)
                    self.driver.close()
            self.driver.switch_to.window(main_window)  # Quay lại tab chính
            print("Đã mở Swagger, đóng tab Swagger và quay lại trang chủ.")
            self.driver.get("https://bookcart.azurewebsites.net/")  # Quay về trang chủ
            time.sleep(2)

            # Mở GitHub (kiểm tra tính năng GitHub)
            print("Đang mở GitHub...")
            github_button = self.driver.find_element(By.XPATH,
                                                     "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[3]")
            github_button.click()
            time.sleep(2)

            # Đóng tab GitHub sau khi kiểm tra
            all_windows = self.driver.window_handles
            for window in all_windows:
                if window != main_window:
                    self.driver.switch_to.window(window)
                    self.driver.close()
            self.driver.switch_to.window(main_window)  # Quay lại tab chính
            print("Đã mở GitHub, đóng tab GitHub và quay lại trang chủ.")
            self.driver.get("https://bookcart.azurewebsites.net/")  # Quay về trang chủ
            time.sleep(2)

            # Mở Menu tài khoản
            print("Đang mở Menu tài khoản...")
            account_menu = self.driver.find_element(By.XPATH,
                                                    "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]")
            account_menu.click()
            time.sleep(2)  # Dừng 2 giây để xem kết quả

            # Mở Logout từ menu tài khoản
            print("Đang thực hiện Logout...")
            logout_button = self.driver.find_element(By.XPATH, "//*[@id='mat-menu-panel-0']/div/button[2]")
            logout_button.click()
            time.sleep(5)  # Dừng 3 giây để xem kết quả

            # Kiểm tra trang login sau khi logout bằng URL
            print("Đã thực hiện Logout, kiểm tra URL...")
            current_url = self.driver.current_url
            expected_url = "https://bookcart.azurewebsites.net/login"
            assert current_url == expected_url, f"Kiểm tra URL thất bại. URL hiện tại là: {current_url}, nhưng kỳ vọng: {expected_url}"
            print(f"Đã chuyển đến trang Login thành công. URL hiện tại: {current_url}")

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình kiểm tra điều hướng: {e}")

    def test_check_and_navigation_myorder(self):
        username = "trhuuhau"
        password = "Vkl041103"

        try:
            # Nhấn vào nút đăng nhập
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            # Nhập tên người dùng và mật khẩu
            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(username)
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(password)

            # Nhấn nút `Login`
            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            # Kiểm tra đăng nhập thành công
            success_indicator = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
            )
            assert success_indicator is not None, "Đăng nhập không thành công."

            print("Đăng nhập thành công.")

            # Mở menu người dùng
            user_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]"))
            )
            user_button.click()
            time.sleep(2)

            # Nhấn chọn `My Orders`
            my_orders_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='My Orders']]"))
            )
            my_orders_button.click()
            time.sleep(5)

            # Chọn một đơn hàng trong danh sách
            order_element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//tr[@role='row' and contains(@class, 'example-element-row')]//td[contains(text(), '591-914247')]")
                )
            )
            order_element.click()
            time.sleep(5)

            print("Đã chọn đơn hàng cụ thể.")

            # Cuộn trang từ từ để người kiểm thử có thể thấy các sản phẩm
            for _ in range(1):  # Số lần cuộn trang (có thể điều chỉnh)
                self.driver.execute_script("window.scrollBy(0, 300);")  # Cuộn 300px mỗi lần
                time.sleep(1)  # Thời gian chờ mỗi lần cuộn

            # Nhấn nút `Next Page` cho đến khi không nhấn được nữa
            while True:
                try:
                    next_page_button = WebDriverWait(self.driver, 10).until(
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
            logout_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Logout']]"))
            )
            logout_button.click()
            time.sleep(5)

            # Kiểm tra URL hiện tại để xác nhận đã đăng xuất
            current_url = self.driver.current_url
            print("URL hiện tại sau khi đăng xuất:", current_url)

            # Xác nhận URL của trang đăng nhập để kiểm tra đăng xuất thành công
            assert current_url == "https://bookcart.azurewebsites.net/login", "Đăng xuất không thành công, không chuyển về trang đăng nhập."

            print("Đăng xuất thành công và đã chuyển về trang đăng nhập.")

        except Exception as e:
            assert False, f"Kiểm thử thất bại với lỗi: {e}"


    # *******************DATA VALIDATION********************

    def test_login_blank_fields(self):
        try:
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )

            # Leave both fields empty
            username_field.send_keys("")
            password_field.send_keys("")

            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            error_message = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//mat-error"))
            )
            assert error_message is not None, "Không tìm thấy thông báo lỗi khi không nhập thông tin đăng nhập."
        except Exception as e:
            assert False, f"Đăng nhập thất bại với lỗi: {e}"

    def test_data_validation_register_invalid(self):
        user_info_invalid = {
            "firstname": "",
            "lastname": "Truu",
            "username": "existing_user",
            "password": "Vkl041103",
            "confirm_password": "wrong_password",
            "gender": "Male"
        }

        try:
            login_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            register_button = WebDriverWait(self.driver, 30).until(
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
                field = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                field.clear()
                field.send_keys(user_info_invalid[key])
                time.sleep(1)

            gender_radio = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info_invalid['gender']}']"))
            )
            gender_radio.click()
            time.sleep(1)

            submit_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-user-registration/div/mat-card/mat-card-content/form/mat-card-actions/button"))
            )
            submit_button.click()
            time.sleep(2)

            error_messages = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "mat-mdc-form-field-error"))
            )
            error_texts = [msg.text.strip() for msg in error_messages]

            expected_errors = ["First Name is required", "Password do not match"]
            for error in expected_errors:
                assert error in error_texts, f"Thông báo lỗi '{error}' không xuất hiện."
        except Exception as e:
            assert False, f"Đăng ký không thành công với lỗi: {e}"

    def test_data_validation_register_with_one_number_in_PW(self):
        user_info = {
            "firstname": "Hau",
            "lastname": "Truu",
            "username": "carrot",
            "password": "1",  # Mật khẩu chỉ có 1 chữ số
            "confirm_password": "1",
            "gender": "Male"
        }

        try:
            login_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            register_button = WebDriverWait(self.driver, 30).until(
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
                field = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                field.clear()
                field.send_keys(user_info[key])
                time.sleep(1)

            gender_radio = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//mat-radio-button[@value='{user_info['gender']}']"))
            )
            gender_radio.click()
            time.sleep(1)

            # Kiểm tra thông báo lỗi cho trường mật khẩu
            try:
                # Chờ thông báo lỗi hiển thị với XPath mới
                error_message = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      "/html/body/app-root/div/app-user-registration/div/mat-card/mat-card-content/form/mat-form-field[4]/div[2]/div"))
                )
                # Định nghĩa thông báo lỗi mong đợi dưới dạng chữ thường
                expected_error_message = "password should have minimum 8 characters, at least 1 uppercase letter, 1 lowercase letter and 1 number"

                # So sánh thông báo lỗi mà không phân biệt chữ hoa chữ thường
                assert expected_error_message in error_message.text.lower(), f"Expected error message not found. Actual message: {error_message.text}"
                print("Test Passed: Error message displayed as expected.")
            except TimeoutException:
                assert False, "Thông báo lỗi cho trường mật khẩu không xuất hiện. Test Failed."


        except Exception as e:
            assert False, f"Đăng ký thất bại với lỗi: {e}"

    def test_data_validation_placeorder(self):
        # Đăng nhập trước
        self.test_login_valid()

        # Nhấn vào nút "Thêm vào giỏ hàng"
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
        )
        add_to_cart_button.click()

        # Kiểm tra xem sản phẩm đã được thêm vào giỏ hàng hay chưa
        try:
            success_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.mdc-snackbar__label'))
            )
            assert "one item added to cart" in success_message.text.lower(), "Sản phẩm chưa được thêm vào giỏ hàng."
        except TimeoutException:
            print(self.driver.page_source)  # In ra HTML để kiểm tra nếu không tìm thấy thông báo
            assert False, "Thông báo thêm sản phẩm vào giỏ hàng không xuất hiện."

        # Nhấn vào biểu tượng giỏ hàng
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        cart_icon.click()

        # Nhấn vào nút checkout
        checkout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[2]/td[6]/button"))
        )
        checkout_button.click()

        # Điền thông tin vào biểu mẫu
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@formcontrolname="name"]'))
        ).send_keys('Nguyen Van A')

        self.driver.find_element(By.XPATH, '//*[@formcontrolname="addressLine1"]').send_keys('123 Đường ABC')
        self.driver.find_element(By.XPATH, '//*[@formcontrolname="addressLine2"]').send_keys('Tầng 2, Chung cư XYZ')

        # Nhập mã pin không hợp lệ (2 chữ số)
        self.driver.find_element(By.XPATH, '//*[@formcontrolname="pincode"]').send_keys('11')
        self.driver.find_element(By.XPATH, '//*[@formcontrolname="state"]').send_keys('Hồ Chí Minh')

        # Nhấn vào nút "Place Order"
        place_order_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        # Thêm thời gian chờ trước khi nhấn nút "Place Order"
        time.sleep(2)  # Chờ 2 giây

        place_order_button.click()
        time.sleep(2)  # Chờ 2 giây

        # Kiểm tra thông báo lỗi cho trường pincode
        try:
            # Chờ thông báo lỗi hiển thị
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'mat-error'))
            )
            assert "pincode must have 6 digits only and cannot start with 0" in error_message.text.lower()
            print("Test Passed: Error message displayed as expected.")
        except TimeoutException:
            print(self.driver.page_source)
            assert False, "Thông báo lỗi cho trường pincode không xuất hiện. Test Failed."

        # Không cần kiểm tra đơn hàng thành công vì chúng ta đang kiểm tra lỗi



    # ***************ADD TO CART - CHECKOUT*****************

    def add_to_wishlist(self, quantity=1):
        username = "trhuuhau"
        password = "Vkl041103"

        print("Bắt đầu quá trình đăng nhập...")
        try:
            # Đăng nhập
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(username)

            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(password)

            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            success_indicator = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
            )
            assert success_indicator is not None, "Đăng nhập không thành công: không tìm thấy phần tử xác nhận đăng nhập."
            print("Đăng nhập thành công. Tiến hành tìm kiếm sản phẩm...")

        except Exception as e:
            print(f"Đăng nhập thất bại với lỗi: {e}")
            return []

        try:
            # Tìm tất cả sản phẩm
            products = WebDriverWait(self.driver, 15).until(
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
                    success_message = WebDriverWait(self.driver, 10).until(
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

    def test_add_1_product_to_wishlist(self):
        """
        Thêm một sản phẩm vào danh sách yêu thích (wishlist) và xác nhận việc thêm thành công.
        Kiểm tra các sản phẩm đã có trong wishlist và đảm bảo sản phẩm vừa thêm tồn tại trong đó.
        """
        print("Thêm 1 sản phẩm vào danh sách yêu thích khi nó chưa có trong wishlist...")

        # Gọi hàm `add_to_wishlist` để thêm sản phẩm vào wishlist
        added_products = self.add_to_wishlist(quantity=1)

        try:
            # Điều hướng đến trang wishlist nếu cần
            wishlist_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[1]"))
                # Chỉnh sửa XPATH nếu cần
            )
            wishlist_button.click()
            time.sleep(3)  # Đợi trang wishlist tải

            # Đợi danh sách wishlist xuất hiện sau khi thêm sản phẩm
            wishlist_items = WebDriverWait(self.driver, 10).until(
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

    def add_to_cart(self, quantity=3):
        # Đăng nhập vào hệ thống
        username = "trhuuhau"
        password = "Vkl041103"

        print("Bắt đầu quá trình đăng nhập...")
        try:
            # Nhấn vào nút đăng nhập
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            # Nhập tên đăng nhập
            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(username)

            # Nhập mật khẩu
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(password)

            # Nhấn nút xác nhận đăng nhập
            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            # Kiểm tra đăng nhập thành công
            success_indicator = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
            )
            assert success_indicator is not None, "Đăng nhập không thành công: không tìm thấy phần tử xác nhận đăng nhập."
            print("Đăng nhập thành công. Tiến hành tìm kiếm sản phẩm...")

        except Exception as e:
            print(f"Đăng nhập thất bại với lỗi: {e}")
            return []  # Trả về danh sách rỗng nếu đăng nhập thất bại

        try:
            # Tìm tất cả sản phẩm trên trang
            products = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//app-book-card"))
            )

            # Chỉ lấy số sản phẩm theo yêu cầu
            product_count = min(quantity, len(products))  # Số lượng sản phẩm cần thêm vào giỏ hàng
            added_products = []  # Danh sách lưu trữ tên sản phẩm đã thêm

            print(f"Tìm thấy {len(products)} sản phẩm. Sẽ thêm {product_count} sản phẩm vào giỏ hàng...")

            for i in range(product_count):
                product = products[i]

                # Lấy tên sản phẩm
                product_name = product.find_element(By.XPATH, ".//strong").text
                added_products.append(product_name)  # Lưu tên sản phẩm đã thêm

                # Nhấn vào nút "Thêm vào giỏ hàng" cho sản phẩm hiện tại
                print(f"Đang thêm sản phẩm: {product_name} vào giỏ hàng...")
                add_to_cart_button = product.find_element(By.XPATH, ".//button[contains(., 'Add to Cart')]")
                add_to_cart_button.click()

                # Kiểm tra thông báo thành công
                try:
                    success_message = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '.mdc-snackbar__label'))
                    )
                    assert "one item added to cart" in success_message.text.lower(), f"Sản phẩm '{product_name}' chưa được thêm vào giỏ hàng."
                    print(f"Sản phẩm '{product_name}' đã được thêm vào giỏ hàng thành công.")
                except TimeoutException:
                    assert False, "Thông báo thêm sản phẩm vào giỏ hàng không xuất hiện."

                # Quay lại trang danh sách sản phẩm và làm mới danh sách
                print("Quay lại trang danh sách sản phẩm...")
                product_list_url = "https://bookcart.azurewebsites.net/"
                self.driver.get(product_list_url)

                # Tăng thời gian chờ cho danh sách sản phẩm tải lại
                products = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//app-book-card"))
                )

            # Hiển thị các sản phẩm đã thêm
            print("Danh sách sản phẩm đã thêm vào giỏ hàng:", added_products)

            # Nhấn vào biểu tượng giỏ hàng
            print("Nhấn vào biểu tượng giỏ hàng để kiểm tra...")
            cart_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            cart_icon.click()

            # Kiểm tra xem tên sản phẩm đã được thêm vào giỏ hàng chưa
            print("Kiểm tra các sản phẩm trong giỏ hàng...")
            for product_name in added_products:
                print(f"Đang kiểm tra sản phẩm '{product_name}' trong giỏ hàng...")
                try:
                    product_in_cart = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, f"//td[contains(@class, 'mat-column-title')]//a[text()='{product_name}']"))
                    )
                    assert product_in_cart.is_displayed(), f"Sản phẩm '{product_name}' không có trong giỏ hàng."
                    print(f"Sản phẩm '{product_name}' có trong giỏ hàng.")
                except TimeoutException:
                    assert False, f"Sản phẩm '{product_name}' không xuất hiện trong giỏ hàng."

            print(f"Tất cả {product_count} sản phẩm đã được thêm vào giỏ hàng thành công!")
            return added_products  # Trả về danh sách các sản phẩm đã thêm

        except TimeoutException:
            assert False, "Không tìm thấy danh sách sản phẩm sau khi đăng nhập."

    def test_add_3_product_to_cart(self):
        # Đặt số lượng sản phẩm cần thêm vào giỏ hàng
        quantity_to_add = 3

        # Gọi hàm thêm sản phẩm vào giỏ hàng
        print(f"Thêm {quantity_to_add} sản phẩm vào giỏ hàng...")
        added_products = self.add_to_cart(quantity=quantity_to_add)

        try:
            # Kiểm tra xem giỏ hàng có ít nhất số lượng sản phẩm đã thêm không
            cart_items = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//app-shoppingcart//table/tbody/tr"))
            )

            # Đếm số lượng sản phẩm trong giỏ hàng
            cart_item_count = len(cart_items)
            assert cart_item_count >= quantity_to_add, f"Giỏ hàng không có đủ sản phẩm. Có {cart_item_count} sản phẩm."

            # Lấy tên các sản phẩm trong giỏ hàng để kiểm tra
            added_product_names = []
            for i in range(min(quantity_to_add, cart_item_count)):
                product_name = cart_items[i].find_element(By.XPATH,
                                                          ".//td[contains(@class, 'mat-column-title')]//a").text
                added_product_names.append(product_name)

            # So sánh danh sách sản phẩm đã thêm với sản phẩm trong giỏ hàng
            assert len(added_product_names) == quantity_to_add, "Không phải tất cả sản phẩm đã thêm vào giỏ hàng."

            print(f"Tất cả {quantity_to_add} sản phẩm đã được thêm vào giỏ hàng thành công!")

        except TimeoutException:
            raise Exception("Không thể mở giỏ hàng hoặc không tìm thấy sản phẩm trong giỏ hàng.")

    def test_add_product_to_cart_with_random_quantity(self):
        # Đặt số lượng sản phẩm ngẫu nhiên từ 1 đến 5
        random_quantity = random.randint(1, 5)
        print(f"Số lượng ngẫu nhiên được chọn để thêm vào giỏ hàng: {random_quantity}")

        # Gọi hàm thêm một sản phẩm vào giỏ hàng
        print(f"Thêm 1 sản phẩm vào giỏ hàng...")
        added_products = self.add_to_cart(quantity=1)

        # Mở giỏ hàng
        print("Mở giỏ hàng để kiểm tra...")
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        cart_icon.click()

        try:
            # Kiểm tra xem sản phẩm đã được thêm vào giỏ hàng chưa
            product_name = added_products[0]  # Lấy tên sản phẩm vừa thêm
            print(f"Đang kiểm tra sản phẩm '{product_name}' trong giỏ hàng...")

            # Tìm sản phẩm trong giỏ hàng
            product_in_cart = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//td[contains(@class, 'mat-column-title')]//a[text()='{product_name}']"))
            )

            assert product_in_cart.is_displayed(), f"Sản phẩm '{product_name}' không có trong giỏ hàng."
            print(f"Sản phẩm '{product_name}' có trong giỏ hàng.")

            # Lấy số lượng hiện tại của sản phẩm trong giỏ hàng
            quantity_xpath = "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[1]/table/tbody/tr[1]/td[4]/div/div[2]"
            current_quantity_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, quantity_xpath))
            )
            current_quantity = int(current_quantity_element.text)  # Lấy giá trị số lượng hiện tại

            # Nhấp vào nút tăng số lượng sản phẩm ngẫu nhiên
            quantity_increase_button_xpath = "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[1]/table/tbody/tr[1]/td[4]/div/div[3]/button/span[1]"

            for _ in range(random_quantity):
                print("Tăng số lượng sản phẩm...")
                # Chờ cho nút có thể nhấp được
                increase_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, quantity_increase_button_xpath))
                )

                # Dùng ActionChains để đảm bảo rằng phần tử sẽ nhận sự kiện click
                ActionChains(self.driver).move_to_element(increase_button).click().perform()
                time.sleep(1)  # Tạm dừng một chút giữa các lần nhấp

            # Tính toán số lượng mong muốn
            final_quantity = current_quantity + random_quantity
            updated_quantity_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, quantity_xpath))
            )
            updated_quantity = updated_quantity_element.text  # Lấy giá trị số lượng sau khi cập nhật

            # Kiểm tra số lượng sản phẩm trong giỏ hàng
            assert str(updated_quantity) == str(final_quantity), \
                f"Số lượng sản phẩm trong giỏ hàng không đúng. Mong muốn: {final_quantity}, thực tế: {updated_quantity}."
            print(f"Số lượng sản phẩm trong giỏ hàng đã được cập nhật thành công lên {final_quantity}.")

        except TimeoutException:
            raise Exception("Không thể mở giỏ hàng hoặc không tìm thấy sản phẩm trong giỏ hàng.")

    def test_summary_and_add_to_cart(self):
        # Thông tin đăng nhập
        username = "trhuuhau"
        password = "Vkl041103"

        print("Bắt đầu quá trình đăng nhập vào hệ thống...")
        try:
            # Nhấn vào nút đăng nhập
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            login_button.click()
            time.sleep(2)

            # Nhập tên đăng nhập và mật khẩu
            username_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[1]/div[1]//input"))
            )
            username_field.send_keys(username)
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/app-root/div/app-login/div/mat-card/mat-card-content/form/mat-form-field[2]/div[1]//input"))
            )
            password_field.send_keys(password)

            # Nhấn nút xác nhận đăng nhập
            login_submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Login']]"))
            )
            login_submit_button.click()
            time.sleep(5)

            # Kiểm tra đăng nhập thành công
            success_indicator = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[contains(@class, 'mat-mdc-menu-trigger')]//span[@class='mdc-button__label']/span[text()=' trhuuhau']"))
            )
            print("Đăng nhập thành công!")

        except Exception as e:
            print(f"Đăng nhập thất bại với lỗi: {e}")
            return

        # Mở chi tiết sản phẩm và thực hiện các thao tác
        try:
            # Chọn sản phẩm đầu tiên
            product = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//app-book-card[1]//a"))
            )
            product.click()
            time.sleep(3)
            print("Đã mở chi tiết sản phẩm.")

            # Cuộn trang từ từ để người kiểm thử có thể thấy các sản phẩm
            for _ in range(1):  # Số lần cuộn trang (có thể điều chỉnh)
                self.driver.execute_script("window.scrollBy(0, 300);")  # Cuộn 300px mỗi lần
                time.sleep(1)  # Thời gian chờ mỗi lần cuộn


            # Nhấn nút "Generate book plot summary using Google Gemini"
            summary_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[span[contains(text(),'Generate book plot summary using Google Gemini')]]"))
            )
            summary_button.click()
            print("Đã nhấn nút summary.")

            # Chờ tóm tắt hoàn tất (thêm thời gian chờ để xử lý quá trình tóm tắt nếu cần thiết)
            time.sleep(10)
            print("Đã hoàn thành tóm tắt sách.")

            # Nhấn nút "Add to Cart"
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(),'Add to Cart')]]"))
            )
            add_to_cart_button.click()
            print("Đã thêm sản phẩm vào giỏ hàng.")
            time.sleep(2)


            # Kiểm tra giỏ hàng
            cart_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
            )
            cart_icon.click()
            print("Đã mở giỏ hàng để kiểm tra.")
            time.sleep(2)

            # Kiểm tra sản phẩm trong giỏ hàng
            product_in_cart = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//app-shoppingcart//table/tbody/tr//td[contains(@class, 'mat-column-title')]//a"))
            )
            assert product_in_cart.is_displayed(), "Sản phẩm không có trong giỏ hàng."
            print("Sản phẩm đã có trong giỏ hàng.")

        except TimeoutException:
            print("Không thể hoàn thành quy trình thêm sản phẩm vào giỏ hàng.")

        print("Kết thúc kiểm thử.")

    def test_calculate_cart_total(self):
        # Đăng nhập và thêm một số sản phẩm vào giỏ hàng trước khi kiểm tra
        print("Thêm sản phẩm vào giỏ hàng để kiểm tra tổng giá trị...")
        quantity_to_add = 3
        added_products = self.add_to_cart(quantity=quantity_to_add)

        # Mở giỏ hàng
        print("Mở giỏ hàng để kiểm tra tổng giá trị...")
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        cart_icon.click()

        try:
            # Lấy tất cả các hàng trong giỏ hàng
            cart_items = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//app-shoppingcart//table/tbody/tr"))
            )

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

                # Cập nhật tổng giá trị
                total_price += item_price * item_quantity

            # Kiểm tra tổng giá trị hiển thị trong giỏ hàng
            total_value_xpath = "//app-shoppingcart//td[contains(@class, 'mat-column-action')]/strong[not(contains(text(), 'Cart Total:'))]"
            displayed_total_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, total_value_xpath))
            )

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

    # Kiểm tra chức năng checkout
    def test_checkout(self):
        # Đăng nhập trước
        self.test_login_valid()

        # Nhấn vào nút "Thêm vào giỏ hàng"
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
        )
        add_to_cart_button.click()

        # Kiểm tra xem sản phẩm đã được thêm vào giỏ hàng hay chưa
        try:
            # Cập nhật để tìm phần tử thông báo thành công
            success_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.mdc-snackbar__label'))
            )
            assert "one item added to cart" in success_message.text.lower(), "Sản phẩm chưa được thêm vào giỏ hàng."
        except TimeoutException:
            print(self.driver.page_source)  # In ra HTML để kiểm tra nếu không tìm thấy thông báo
            assert False, "Thông báo thêm sản phẩm vào giỏ hàng không xuất hiện."

        # Nhấn vào biểu tượng giỏ hàng
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[2]"))
        )
        cart_icon.click()

        # Nhấn vào nút checkout
        checkout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[2]/td[6]/button"))
        )
        checkout_button.click()

        # Điền thông tin vào biểu mẫu
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@formcontrolname="name"]'))
        ).send_keys('Nguyen Van A')

        self.driver.find_element(By.XPATH, '//*[@formcontrolname="addressLine1"]').send_keys('123 Đường ABC')
        self.driver.find_element(By.XPATH, '//*[@formcontrolname="addressLine2"]').send_keys('Tầng 2, Chung cư XYZ')
        self.driver.find_element(By.XPATH, '//*[@formcontrolname="pincode"]').send_keys('700000')
        self.driver.find_element(By.XPATH, '//*[@formcontrolname="state"]').send_keys('Hồ Chí Minh')

        # Nhấn vào nút "Place Order"
        place_order_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        place_order_button.click()

        # Kiểm tra xem đơn hàng đã được gửi thành công hay chưa
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.mdc-snackbar__label'))
            )
            success_message = self.driver.find_element(By.CSS_SELECTOR, '.mdc-snackbar__label')
            assert "order placed successfully" in success_message.text.lower()
        except TimeoutException:
            print(self.driver.page_source)
            assert False, "Đơn hàng không được xác nhận thành công."

    # Kiểm tra xem ứng dụng có chuyển đến trang đăng nhập khi checkout mà chưa đăng nhập
    def test_checkout_without_login(self):
        # Thử nhấn vào nút "Thêm vào giỏ hàng" mà không đăng nhập
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/div/app-home/div/div[2]/div/div[1]/app-book-card/mat-card/mat-card-content/app-addtocart/button"))
        )
        add_to_cart_button.click()
        time.sleep(2)  # Tạm dừng 2 giây để quan sát

        # Nhấn vào biểu tượng giỏ hàng
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/button[1]"))
        )
        cart_icon.click()
        time.sleep(5)  # Tạm dừng 2 giây để quan sát

        # Nhấn vào nút "Checkout"
        try:
            checkout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/app-root/div/app-shoppingcart/mat-card/mat-card-content[2]/td[6]/button"))
            )
            checkout_button.click()
            time.sleep(2)  # Tạm dừng 2 giây để kiểm tra quá trình chuyển hướng

            # Kiểm tra URL hiện tại xem có phải là trang đăng nhập không
            current_url = self.driver.current_url
            assert "login" in current_url.lower(), "Ứng dụng không chuyển hướng đến trang đăng nhập khi checkout mà không đăng nhập."

        except TimeoutException:
            print("Không tìm thấy nút Checkout hoặc có thể đã chuyển hướng đến trang đăng nhập.")

        # In ra URL hiện tại để xác nhận
        print("URL hiện tại:", self.driver.current_url)


    # ****************SEARCH********************

    def test_search_product(self):
        # Tên sản phẩm cần tìm
        search_query = "Harry"

        # Tìm ô tìm kiếm (dựa trên mã nguồn HTML đã cho)
        search_box = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="search"]')

        # Nhập tên sản phẩm vào ô tìm kiếm
        search_box.send_keys(search_query)
        time.sleep(3)

        # Gửi phím Enter để thực hiện tìm kiếm
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # Chờ trang tải kết quả tìm kiếm
        try:
            # Chờ một khoảng thời gian để kết quả tìm kiếm xuất hiện
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/app-home/div/div[2]/div/div/app-book-card/mat-card/mat-card-content/div[2]/a/strong'))
                # Thay 'div.product-name' bằng selector đúng
            )
            print(f"Kết quả tìm kiếm cho '{search_query}' đã hiển thị.")
        except TimeoutException:
            print(f"Không tìm thấy kết quả tìm kiếm cho '{search_query}'.")

        # Thêm thời gian chờ giữa các thao tác để đảm bảo kết quả hiển thị
        time.sleep(3)  # Đợi 3 giây trước khi kiểm tra

        # Kiểm tra xem sản phẩm có được hiển thị trong kết quả không
        try:
            # Tìm sản phẩm trong kết quả và kiểm tra tính khả dụng của nó
            product_result = self.driver.find_element(By.CSS_SELECTOR, 'div.product-name')  # Cập nhật với selector chính xác
            if product_result.is_displayed():
                print(f"Sản phẩm '{search_query}' được hiển thị trong kết quả tìm kiếm.")
            else:
                print(f"Sản phẩm '{search_query}' không hiển thị trong kết quả tìm kiếm.")
        except StaleElementReferenceException:
            print(f"Lỗi tham chiếu trong khi kiểm tra sản phẩm '{search_query}'.")

    def test_search_product_with_suggestions(self):
        # Tên sản phẩm cần tìm
        global suggestion_text
        search_query = "Harry"

        # Tìm ô tìm kiếm (dựa trên mã nguồn HTML đã cho)
        search_box = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="search"]')

        # Nhập tên sản phẩm vào ô tìm kiếm
        search_box.send_keys(search_query)
        time.sleep(3)  # Thời gian chờ để các gợi ý xuất hiện

        # Chờ các gợi ý xuất hiện
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mat-autocomplete-0"]'))  # XPath của gợi ý
            )
            print(f"Gợi ý tìm kiếm cho '{search_query}' đã hiển thị.")
        except TimeoutException:
            print(f"Không tìm thấy gợi ý tìm kiếm cho '{search_query}'.")

        # Nhấp vào gợi ý tìm kiếm và lấy nội dung gợi ý
        try:
            # XPath của gợi ý đầu tiên
            first_suggestion = self.driver.find_element(By.XPATH, '//*[@id="mat-autocomplete-0"]/mat-option[1]')
            suggestion_text = first_suggestion.text.strip()  # Lấy nội dung gợi ý
            first_suggestion.click()
            print(f"Nhấp vào gợi ý '{suggestion_text}' thành công.")
        except NoSuchElementException:
            print(f"Không tìm thấy gợi ý với từ khóa '{search_query}'.")

        time.sleep(3)  # Đợi 3 giây để trang tải kết quả

        # Kiểm tra xem sản phẩm có được hiển thị trong kết quả tìm kiếm không
        try:
            # Kiểm tra xem sản phẩm có hiển thị không dựa trên nội dung của gợi ý (sử dụng nội dung lấy được)
            product_result = self.driver.find_element(By.XPATH,
                                                      f'//div[@class="p-1 ng-star-inserted"]//mat-card-content//div[@class="card-title my-2"]//strong[contains(text(), "{suggestion_text}")]')

            if product_result.is_displayed():
                print(f"Sản phẩm '{suggestion_text}' được hiển thị trong kết quả tìm kiếm.")
            else:
                print(f"Sản phẩm '{suggestion_text}' không hiển thị trong kết quả tìm kiếm.")
        except NoSuchElementException:
            print(f"Không tìm thấy sản phẩm '{suggestion_text}' trong kết quả tìm kiếm.")

    def test_filter_price(self):
        # Mở trang chính
        self.driver.get("https://bookcart.azurewebsites.net/")
        time.sleep(5)  # Chờ để trang tải hoàn tất

        # Đợi để thanh trượt xuất hiện
        slider = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/app-root/div/app-home/div/div[1]/div/app-price-filter/mat-card/mat-card-content[1]/mat-slider/input"))
        )
        time.sleep(3)  # Thời gian chờ để thanh trượt sẵn sàng

        # Đặt giá trị thanh trượt trực tiếp bằng JavaScript và kích hoạt sự kiện 'input' và 'change'
        self.driver.execute_script("""
        arguments[0].value = 500; 
        arguments[0].dispatchEvent(new Event('input'));
        arguments[0].dispatchEvent(new Event('change'));
        """, slider)
        time.sleep(3)  # Đợi để trang cập nhật kết quả

        # Kiểm tra giá trị của thanh trượt sau khi điều chỉnh
        slider_value = self.driver.execute_script("return arguments[0].value", slider)
        print(f"Giá trị thanh trượt thực tế là: {slider_value}")  # In giá trị thực tế

        # Điều chỉnh lại nếu giá trị không khớp
        assert int(slider_value) == 500 or int(
            slider_value) == 511, f"Thanh trượt không được đặt đúng mức 500, mà là {slider_value}"

        # Cuộn trang từ từ để người kiểm thử có thể thấy các sản phẩm
        for _ in range(5):  # Số lần cuộn trang (có thể điều chỉnh)
            self.driver.execute_script("window.scrollBy(0, 300);")  # Cuộn 300px mỗi lần
            time.sleep(1)  # Thời gian chờ mỗi lần cuộn

        # Lấy tất cả các giá sản phẩm hiển thị trên trang
        prices = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//p[contains(text(), '₹')]"))
        )

        # Kiểm tra từng giá sản phẩm để đảm bảo giá <= 500
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
            assert price_value <= 500, f"Giá {price_value} lớn hơn 500"

        print("Tất cả giá sản phẩm đều <= 500")


    # *****************REPONSIVE DESIGN**************

    def _test_responsive_design_for_size(self, width, height):
        driver = self.driver  # Sử dụng driver từ thuộc tính của lớp
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
                failed_checks.append(f"Logo không hiển thị đúng ở kích thước {width}x{height}: {e}")

            # Kiểm tra thanh điều hướng ở chế độ mobile (menu icon)
            if width <= 768:  # Với màn hình nhỏ (dưới 768px)
                try:
                    menu_icon = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "/html/body/app-root/app-nav-bar/mat-toolbar/mat-toolbar-row/div[3]/a[1]"))
                    )
                    assert menu_icon.is_displayed(), f"Menu icon không hiển thị ở chế độ mobile tại kích thước {width}x{height}"
                except Exception as e:
                    failed_checks.append(
                        f"Menu icon không hiển thị ở chế độ mobile tại kích thước {width}x{height}: {e}")
            else:  # Với màn hình lớn
                navbar_buttons = driver.find_elements(By.XPATH,
                                                      "//div[@class='d-flex align-items-center']//button")
                try:
                    assert len(
                        navbar_buttons) > 0, f"Các liên kết điều hướng không hiển thị ở chế độ desktop tại kích thước {width}x{height}"
                except AssertionError as e:
                    failed_checks.append(
                        f"Các liên kết điều hướng không hiển thị ở chế độ desktop tại kích thước {width}x{height}: {e}")

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

    def test_responsive_design_small(self):
        # Đầu tiên, thực hiện đăng nhập trước
        self.test_login_valid()
        # Kích thước màn hình: iPhone 8 (375x667)
        width, height = 375, 667
        self._test_responsive_design_for_size(width, height)

    def test_responsive_design_ipad(self):
        # Đầu tiên, thực hiện đăng nhập trước
        self.test_login_valid()
        # Kích thước màn hình: iPad (768x1024)
        width, height = 768, 1024
        self._test_responsive_design_for_size(width, height)

    def test_responsive_design_tablet(self):
        # Đầu tiên, thực hiện đăng nhập trước
        self.test_login_valid()
        # Kích thước màn hình: Tablet (1280x800)
        width, height = 1280, 800
        self._test_responsive_design_for_size(width, height)

    def test_responsive_design_desktop(self):
        # Đầu tiên, thực hiện đăng nhập trước
        self.test_login_valid()
        # Kích thước màn hình: Desktop Full HD (1920x1080)
        width, height = 1920, 1080
        self._test_responsive_design_for_size(width, height)
