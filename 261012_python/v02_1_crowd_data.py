# 서울시 실시간 인구데이터(인파밀집) 수집
# 출처: 서울 열린데이터광장(서울특별시) - 서울시 실시간 인구데이터 (OA-21778)
#
# 인증키 발급: https://data.seoul.go.kr → 로그인 → 마이페이지 → 인증키 신청
# 발급받은 키를 아래 API_KEY에 넣거나, 환경변수 SEOUL_API_KEY 로 설정하세요.
# 키가 없으면 "sample" 키로 동작하며, 이때는 '광화문·덕수궁' 1곳만 조회됩니다.

import csv
import os
import time
from datetime import datetime

import requests

API_KEY = os.environ.get("SEOUL_API_KEY", "sample")
BASE_URL = "http://openapi.seoul.go.kr:8088/{key}/json/citydata_ppltn/1/5/{area}"

# 장소코드는 POI001 부터 시작 (중간에 비어있는 번호가 있어 넉넉하게 130까지 시도)
if API_KEY == "sample":
    AREA_CODES = ["POI009"]  # 샘플키는 광화문·덕수궁만 가능
else:
    AREA_CODES = [f"POI{i:03d}" for i in range(1, 131)]


# 1. 장소 하나의 데이터를 가져오는 함수
def fetch_area(area):
    url = BASE_URL.format(key=API_KEY, area=area)
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
    except Exception as e:
        print(f"[{area}] 요청 실패: {e}")
        return None

    items = data.get("SeoulRtd.citydata_ppltn")
    if not items:
        msg = data.get("RESULT", {}).get("RESULT.MESSAGE", "데이터 없음")
        print(f"[{area}] 건너뜀: {msg}")
        return None
    return items[0]


# 2. 수집
now_rows = []       # 현재 인구 현황
forecast_rows = []  # 12시간 예측

for area in AREA_CODES:
    item = fetch_area(area)
    if item is None:
        continue

    forecasts = item.pop("FCST_PPLTN", None) or []
    now_rows.append(item)
    for fc in forecasts:
        forecast_rows.append({"AREA_CD": item["AREA_CD"], "AREA_NM": item["AREA_NM"], **fc})

    print(f"[{item['AREA_CD']}] {item['AREA_NM']}: {item['AREA_CONGEST_LVL']} "
          f"({item['AREA_PPLTN_MIN']}~{item['AREA_PPLTN_MAX']}명)")
    time.sleep(0.1)  # 서버 부담 줄이기


# 3. CSV 저장 (엑셀에서 한글 안 깨지게 utf-8-sig)
def save_csv(filename, rows):
    if not rows:
        return
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"저장 완료: {filename} ({len(rows)}행)")


os.makedirs("data", exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M")
save_csv(f"data/crowd_now_{stamp}.csv", now_rows)
save_csv(f"data/crowd_forecast_{stamp}.csv", forecast_rows)


# 4. 혼잡한 곳 요약
LEVELS = {"여유": 1, "보통": 2, "약간 붐빔": 3, "붐빔": 4}
busy = sorted(now_rows, key=lambda r: LEVELS.get(r["AREA_CONGEST_LVL"], 0), reverse=True)

print(f"\n=== 수집 장소 {len(now_rows)}곳 / 혼잡도 높은 순 TOP 10 ===")
for r in busy[:10]:
    print(f"{r['AREA_NM']:<20} {r['AREA_CONGEST_LVL']:<6} {r['AREA_PPLTN_MIN']}~{r['AREA_PPLTN_MAX']}명")
