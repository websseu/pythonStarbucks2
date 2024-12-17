# 파이썬을 이용한 스타벅스 데이터 수집하기

파이썬을 이용하여 스타벅스 홈페이지에서 스타벅스 매장 정보를 수집하겠습니다.

## 지역

```

```

## 폴더명

```
https://websseu.github.io/pythonStarbucks/location/seoul/seoul_2024-11-13.json
```

```
https://websseu.github.io/pythonStarbucks/location/[지역명]/[지역명]_2024-11-13.json
```

```
└── location [지역명, 지역 매장 갯수, 위도, 경도]
    ├── 01 seoul
    ├── 02 gyeonggi
    ├── 03 busan
    ├── 04 daegu
    ├── 05 incheon
    ├── 06 gwangju
    ├── 07 daejeon
    ├── 08 ulsan
    ├── 09 gangwon
    ├── 10 chungbuk
    ├── 11 chungnam
    ├── 12 jeolbuk
    ├── 13 jeolnam
    ├── 14 gyeongbuk
    ├── 15 gyeongnam
    ├── 16 jeju
    └── 17 sejong
```

## 지역명

지역명은 다음과 같이 정리합니다.

```
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
    "제주": "jeju",
    "세종": "sejong"
}
```
