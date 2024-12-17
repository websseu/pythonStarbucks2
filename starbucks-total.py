import os
import json
from datetime import datetime

# 기본 경로 설정
base_path = "total"  # "total" 폴더 경로
output_file = "starbucks_total.json"  # 출력 파일 경로

# 통합 데이터 구조 초기화
combined_data = {
    "style": "스타벅스",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "count": 0,
    "items": []
}

# 디버깅: base_path 확인
if not os.path.exists(base_path):
    print(f"Error: '{base_path}' 경로가 존재하지 않습니다.")
    exit()

# JSON 파일 가져오기
json_files = [f for f in os.listdir(base_path) if f.endswith(".json")]

if not json_files:
    print("Error: JSON 파일이 'total' 폴더에 없습니다.")
    exit()

# 디버깅: JSON 파일 목록 확인
print(f"Found JSON files in '{base_path}': {json_files}")

# 모든 JSON 파일 처리
for json_file in json_files:
    file_path = os.path.join(base_path, json_file)
    
    # 디버깅: 처리 중인 파일 확인
    print(f"Processing file: {file_path}")
    
    try:
        # JSON 파일 읽기
        with open(file_path, "r", encoding="utf-8") as f:
            file_data = json.load(f)
        
        # 데이터를 combined_data에 추가
        if "item" in file_data and isinstance(file_data["item"], list):
            combined_data["items"].extend(file_data["item"])
        else:
            print(f"Warning: 'item' 키가 없거나 잘못된 형식입니다. ({file_path})")
    except json.JSONDecodeError as e:
        print(f"Error: JSON 파일을 읽을 수 없습니다. ({file_path})")
        print(f"Details: {e}")

# 총 개수 추가
combined_data["count"] = len(combined_data["items"])

# 결과를 출력 파일로 저장
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=4)

print(f"통합된 데이터가 '{output_file}'에 저장되었습니다.")
