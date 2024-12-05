from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import re
import os
import json
from datetime import datetime

# 현재 날짜
current_date = datetime.now().strftime("%Y-%m-%d")

# 한글 지역명과 영문 지역명 매핑
location_name_mapping = {
    "서울": "seoul",
    "부산": "busan",
    "대구": "daegu",
    "인천": "incheon",
    "광주": "gwangju",
    "대전": "daejeon",
    "울산": "ulsan",
    "경기": "gyeonggi",
    "강원": "gangwon",
    "충북": "chungbuk",
    "충남": "chungnam",
    "전북": "jeolbuk",
    "전남": "jeolnam",
    "경북": "gyeongbuk",
    "경남": "gyeongnam",
    "제주": "jeju"
}

# 폴더 생성
base_folder = "location"
count_folder = os.path.join(base_folder, "count")
os.makedirs(count_folder, exist_ok=True) 

# 웹드라이버 설정
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage") 
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")  
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
    time.sleep(10)

    # 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "store_map_layer_cont"))
    )
    print("페이지가 완전히 로드되었습니다.")
    time.sleep(10)

    # 서울 버튼 클릭
    sido_button = browser.find_element(By.CSS_SELECTOR, ".sido_arae_box li:nth-child(1) a")
    browser.execute_script("arguments[0].click();", sido_button)
    print("서울 버튼을 클릭했습니다.")
    time.sleep(5)

    # 전체 버튼 클릭
    all_button = browser.find_element(By.CSS_SELECTOR, ".gugun_arae_box li:nth-child(1) a")
    browser.execute_script("arguments[0].click();", all_button)
    print("전체 버튼을 클릭했습니다.")
    time.sleep(10)

    # 페이지 소스를 BeautifulSoup을 사용하여 저장
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # 서울  데이터를 저장할 변수
    store_data = []

    # 서울 데이터 수집
    stores = soup.select(".quickSearchResultBoxSidoGugun li.quickResultLstCon")
    for store in stores:
        # 이름, 주소, 위도, 경도 추출
        name = store.get("data-name")
        address = store.select_one(".result_details").text.strip() if store.select_one(".result_details") else None
        
        # 주소에서 전화번호 형식을 제거
        if address:
            address = re.sub(r'\d{4}-\d{4}', '', address).strip()  # 전화번호 패턴 제거
        
        latitude = store.get("data-lat")
        longitude = store.get("data-long")

        # 수집된 정보를 딕셔너리에 저장
        store_data.append({
            "name": name,
            "address": address,
            "latitude": latitude,
            "longitude": longitude
        })
    
    # 지역 이름 정의
    location_name_kor = "서울"
    location_name_eng = location_name_mapping[location_name_kor]
    
    # 최종 JSON 구조 정의
    final_data = {
        "location": "서울",
        "count": len(store_data),
        "date": current_date,
        "item": store_data
    }

    # location 폴더에 영문 이름으로 폴더 생성
    location_folder_path = os.path.join(base_folder, location_name_eng)
    os.makedirs(location_folder_path, exist_ok=True)

    # 데이터 저장
    file_name = f"{location_folder_path}/{location_name_eng}_{current_date}.json"
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"{location_name_eng} 데이터가 '{file_name}' 파일에 저장되었습니다.")

    # 전체 매장 갯수 추출
    total_count_element = soup.select_one(".result_num_wrap .sidoSetResult")
    total_count = int(total_count_element.text.strip()) if total_count_element else 0
    print(f"전체 매장 수: {total_count}")

    # json 파일 생성
    count_data = {
        "date": current_date,
        "total": total_count,
        "seoul": total_count 
    }
    count_file_path = os.path.join(count_folder, f"starbucks-count_{current_date}.json")
    with open(count_file_path, "w", encoding="utf-8") as json_file:
        json.dump(count_data, json_file, ensure_ascii=False, indent=4)
    print(f"데이터가 JSON 파일로 저장되었습니다: {count_file_path}")
   
except TimeoutException as e:
    print("에러 발생:", str(e))

finally:
    browser.quit()
