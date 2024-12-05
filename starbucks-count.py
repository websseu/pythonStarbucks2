from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import os
import json
from datetime import datetime

# 현재 날짜
current_date = datetime.now().strftime("%Y-%m-%d")

# 폴더 생성
base_folder = "location"
count_folder = os.path.join(base_folder, "count")
os.makedirs(count_folder, exist_ok=True) 

# 웹드라이버 설정
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 문제 방지
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")  # 알림 비활성화
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 2,  # 위치 권한 차단
    "profile.default_content_setting_values.notifications": 2  # 알림 차단
})
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)


# 웹드라이버 설정(로컬)
# browser = webdriver.Chrome()
# wait = WebDriverWait(browser, 10)

try:
    browser.get("https://www.starbucks.co.kr/store/store_map.do?disp=locale")

    # 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "store_map_layer_cont"))
    )
    print("페이지가 완전히 로드되었습니다.")
    time.sleep(5)

    # 서울 버튼 클릭
    sido_button = browser.find_element(By.CSS_SELECTOR, ".sido_arae_box li:nth-child(1) a")
    browser.execute_script("arguments[0].click();", sido_button)
    print("서울 버튼을 클릭했습니다.")
    time.sleep(3)

    # 전체 버튼 클릭
    all_button = browser.find_element(By.CSS_SELECTOR, ".gugun_arae_box li:nth-child(1) a")
    browser.execute_script("arguments[0].click();", all_button)
    print("전체 버튼을 클릭했습니다.")
    time.sleep(3)

    # 페이지 소스를 BeautifulSoup을 사용하여 저장
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # 전체 매장 수 추출
    total_count_element = soup.select_one(".result_num_wrap .sidoSetResult")
    total_count = int(total_count_element.text.strip()) if total_count_element else 0
    print(f"전체 매장 수: {total_count}")

    # json 파일 생성
    count_data = {
        "date": current_date,
        "total": total_count,
        "seoul": total_count  # 현재 페이지에서 서울 매장만 조회했다고 가정
    }
    count_file_path = os.path.join(count_folder, f"starbucks-count_{current_date}.json")
    with open(count_file_path, "w", encoding="utf-8") as json_file:
        json.dump(count_data, json_file, ensure_ascii=False, indent=4)
    print(f"데이터가 JSON 파일로 저장되었습니다: {count_file_path}")
   
except TimeoutException as e:
    print("에러 발생:", str(e))

finally:
    browser.quit()
