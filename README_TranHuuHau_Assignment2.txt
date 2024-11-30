
# **Tự động hóa kiểm thử với Selenium và Python**

Kho lưu trữ này chứa các script kiểm thử tự động cho các ứng dụng web sử dụng Selenium và Python. Các bài kiểm thử được thiết kế để kiểm tra khả năng phản hồi và chức năng của một trang web.

## **Yêu cầu trước khi sử dụng**

Trước khi chạy các script, đảm bảo rằng bạn đã cài đặt các công cụ sau:

- **Python 3.6 hoặc phiên bản mới hơn**  
- **Google Chrome** (dùng cho Chrome WebDriver)
- **ChromeDriver** (phù hợp với phiên bản Chrome của bạn)
- **Selenium WebDriver**
- **pip** (công cụ cài đặt gói Python)

## **Cài đặt Môi Trường**

Thực hiện các bước sau để thiết lập môi trường:

### 1. **Cài đặt Python**

Nếu bạn chưa cài đặt Python, tải và cài đặt từ trang web chính thức của Python:

- [Tải Python](https://www.python.org/downloads/)

Sau khi cài đặt xong, kiểm tra phiên bản Python đã cài bằng lệnh:

```bash
python --version
```

### 2. **Cài đặt Các Gói Python Cần Thiết**

Bạn cần cài đặt các gói Python sau:

- **Selenium** để tự động hóa web
- **WebDriverManager** để quản lý các driver (tùy chọn nhưng khuyến khích)

Để cài đặt các gói cần thiết, tạo một môi trường ảo (khuyến khích) và cài đặt các phụ thuộc qua `pip`:

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scriptsctivate
# Mac/Linux:
source venv/bin/activate

# Cài đặt các gói cần thiết
pip install selenium webdriver-manager
```

Ngoài ra, bạn có thể cài đặt các gói toàn cục, nhưng việc sử dụng môi trường ảo được khuyến khích để tránh xung đột với các dự án khác.

### 3. **Tải ChromeDriver**

Để chạy các bài kiểm thử với Chrome, bạn cần tải **ChromeDriver**. ChromeDriver cần phải phù hợp với phiên bản trình duyệt Chrome của bạn. Bạn có thể kiểm tra phiên bản Chrome từ:

- **Trợ giúp → Giới thiệu về Google Chrome**

Sau đó, tải ChromeDriver phù hợp từ liên kết sau:

- [Tải ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

Sau khi tải xong, hãy chắc chắn rằng `chromedriver` đã được thêm vào PATH của hệ thống hoặc cung cấp đường dẫn trực tiếp trong script của bạn.

### 4. **Cài đặt WebDriver Manager (Tùy chọn)**

Thay vì quản lý ChromeDriver thủ công, bạn có thể sử dụng gói **WebDriverManager** để tự động xử lý phiên bản driver. Điều này đặc biệt hữu ích để tránh xung đột phiên bản.

```bash
pip install webdriver-manager
```

### 5. **Clone Kho Lưu Trữ**

Clone kho lưu trữ này về máy tính của bạn.

```bash
git clone https://github.com/tranhuuhau2003/N8_TranHuuHau_Assigment2.git
cd N8_TranHuuHau_Assigment2
```

---

## **Chạy Các Script Kiểm Thử**

### 1. **Tạo một Script Kiểm Thử**

Tạo một file Python (ví dụ: `test_script.py`) nơi bạn sẽ viết hoặc gọi các bài kiểm thử của mình.

### 2. **Ví Dụ Mã Kiểm Thử**

Dưới đây là một ví dụ về script kiểm thử để bắt đầu với Selenium WebDriver và chạy một bài kiểm thử cơ bản.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Thiết lập WebDriver
options = Options()
options.add_argument('--headless')  # Chạy ở chế độ không giao diện (headless)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Điều hướng đến một trang web
driver.get("https://www.example.com")
time.sleep(2)

# Tìm kiếm một phần tử
element = driver.find_element(By.TAG_NAME, "h1")
print(f"Tiêu đề trang là: {element.text}")

# Đóng trình duyệt
driver.quit()
```

### 3. **Chạy Script Kiểm Thử**

Để chạy bài kiểm thử, chỉ cần thực thi script Python:

```bash
python test_script.py
```

Nếu mọi thứ được thiết lập chính xác, bài kiểm thử sẽ chạy trong trình duyệt (hoặc ở chế độ headless nếu đã cấu hình).

---

## **Chạy Tất Cả Các Bài Kiểm Thử**

Nếu bạn có nhiều script kiểm thử, bạn có thể chạy tất cả chúng bằng một công cụ quản lý kiểm thử như **unittest** hoặc **pytest**.

### Ví Dụ với `unittest`:

```bash
python -m unittest discover -s tests
```

### Ví Dụ với `pytest`:

```bash
pytest
```

Hãy đảm bảo tổ chức các script kiểm thử của bạn trong một thư mục `tests` hoặc tương tự để dễ dàng phát hiện bởi công cụ quản lý kiểm thử.

---

## **Khắc Phục Lỗi**

- **Lỗi không tương thích phiên bản driver:** Nếu bạn gặp lỗi về sự không tương thích giữa phiên bản Chrome và ChromeDriver, hãy chắc chắn rằng cả hai đều được cập nhật lên phiên bản mới nhất. Bạn có thể cập nhật ChromeDriver bằng cách chạy:

```bash
pip install --upgrade webdriver-manager
```

- **Lỗi Selenium WebDriver:** Đảm bảo rằng Selenium và WebDriverManager đã được cài đặt đúng bằng cách chạy `pip show selenium webdriver-manager`.

- **Vấn đề với môi trường:** Nếu bạn gặp vấn đề với các biến môi trường hoặc môi trường ảo, hãy đảm bảo rằng `chromedriver` đã có trong PATH của hệ thống hoặc cung cấp đường dẫn chính xác trong script kiểm thử của bạn.

---

## **Kết Luận**

README này cung cấp tổng quan về cách thiết lập môi trường và chạy các script kiểm thử sử dụng Selenium và Python. Đối với các cấu hình nâng cao, bạn có thể tích hợp nó vào các pipeline CI/CD như Jenkins, GitHub Actions, hoặc các công cụ khác.

Chúc bạn kiểm thử vui vẻ! 🎉
