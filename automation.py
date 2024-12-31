from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def automate_location():
    # إعدادات المتصفح
    options = Options()
    options.add_argument("--headless")  # لتشغيل المتصفح في وضع غير مرئي
    options.add_argument("--start-maximized")  # لفتح المتصفح في وضع ملء الشاشة (يظل في الوضع غير المرئي)
    options.add_argument("--disable-extensions")  # تعطيل الإضافات

    # إنشاء كائن WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        # فتح صفحة Google Maps
        driver.get("https://www.google.com/maps")

        # انتظار ظهور حقل البحث
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )

        # تنفيذ JavaScript لتحديد الموقع الجغرافي
        driver.execute_script("""
            navigator.geolocation.getCurrentPosition(function(position) {
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
                console.log("Latitude: " + latitude + ", Longitude: " + longitude);
                window.location.href = 'http://127.0.0.1:5000/receive-location?latitude=' + latitude + '&longitude=' + longitude;
            }, function(error) {
                alert('Error getting location');
            });
        """)

        # الانتظار حتى يتم الانتقال إلى الرابط الجديد
        WebDriverWait(driver, 10).until(
            EC.url_contains("/receive-location")
        )

        # إغلاق المتصفح بعد التفاعل
        driver.quit()

    except Exception as e:
        print(f"حدث خطأ: {e}")
        driver.quit()
