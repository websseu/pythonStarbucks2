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

# 웹드라이버 설정
# options = ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage") 
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-infobars")
# options.add_argument("--disable-notifications")
# options.add_experimental_option("prefs", {
#     "profile.default_content_setting_values.geolocation": 2,  # 위치 권한 차단
#     "profile.default_content_setting_values.notifications": 2  # 알림 차단
# })
# browser = webdriver.Chrome(options=options)
# wait = WebDriverWait(browser, 10)

# 웹드라이버 설정(로컬)
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

try:
    # Starbucks 매장 페이지 로드
    browser.get("https://www.starbucks.co.kr/store/store_map.do?disp=locale")
    print("페이지 로드 중...")
    time.sleep(10)

    # 결과를 저장할 데이터 구조
    data = {
        "날짜": current_date,
        "전체": 0,
        "서울": 0,
        "경기": 0,
        "광주": 0,
        "대구": 0,
        "대전": 0,
        "부산": 0,
        "울산": 0,
        "인천": 0,
        "강원": 0,
        "경남": 0,
        "경북": 0,
        "전남": 0,
        "전북": 0,
        "충남": 0,
        "충북": 0,
        "제주": 0,
        "세종": 0,
    }

    # 각 지역 버튼 클릭 및 데이터 수집
    for region in data.keys():
        if region in ["날짜", "전체"]:
            continue 

        try:
            # 지역 버튼 클릭
            region_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//ul[@class='sido_arae_box']/li/a[text()='{region}']")
                )
            )
            browser.execute_script("arguments[0].click();", region_button)
            print(f"{region} 버튼 클릭 완료.")
            time.sleep(10)

            # "전체" 버튼 클릭
            if region != "세종":  # 세종 지역은 전체 버튼이 없으므로 스킵
                try:
                    all_button = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//ul[@class='gugun_arae_box']/li/a[text()='전체']")
                        )
                    )
                    browser.execute_script("arguments[0].click();", all_button)
                    print("전체 버튼 클릭 완료.")
                    time.sleep(10)
                except TimeoutException:
                    print(f"{region}: '전체' 버튼이 없어 다음으로 넘어갑니다.")
                    continue

            # BeautifulSoup으로 데이터 파싱
            soup = BeautifulSoup(browser.page_source, "html.parser")
            region_count = soup.select_one(".result_num_wrap .sidoSetResult").text.strip()

            # 데이터 저장
            data[region] = int(region_count)
            data["전체"] += int(region_count)

            print(f"{region} 매장 수: {region_count}개")

            # "지역" 버튼 클릭
            location_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//header[@class='loca_search']/h3/a")
                )
            )
            browser.execute_script("arguments[0].click();", location_button)
            print("지역 검색 버튼 클릭 완료.")
            time.sleep(5)

        except TimeoutException as e:
            print(f"{region} 데이터 수집 중 에러 발생: {str(e)}")
            continue

    # count 폴더 생성
    output_dir = "count"
    os.makedirs(output_dir, exist_ok=True)

    # JSON 파일 저장
    output_filename = os.path.join(output_dir, f"starbucks-count_{current_date}.json")
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"총 매장 수: {data['전체']}개")
    print(f"JSON 파일 저장 완료: {output_filename}")

except TimeoutException as e:
    print("에러 발생:", str(e))

finally:
    browser.quit()
