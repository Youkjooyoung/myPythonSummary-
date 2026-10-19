import os                #환경변수(API 키)를 읽는 도구
import urllib.request   #인터넷 주소로 자료 요청하는 도구
import json             # 글자로 된 자료를 사전(dict) 모양으로 바꾸는 도구
import pandas as pd     #자료를 엑셀 같은 표로 다루는 도구


# 1. 인증기 -> 정부사이트에서 받은 비밀번호
key = os.getenv("ITS_API_KEY")
# 과금 우려있는 API KEY는 코드 노출 그리고 깃허브에 업로드 하지않음
# .env 환경변수로 관리

# 2. 도로 유형 -> 어느 도로의 CCTV 를 가져올지
# its = 일반도로 ,  ex = 고속도로
road_type = "its"

# 3. 관심 영역(경도 · 위도 범위)
minX, maxX = 120.95, 127.02
minY, maxY = 30.55, 37.69
getType = "json"

# 4. API URL 조립
url_cctv = (
    f"https://openapi.its.go.kr:9443/cctvInfo"
    f"?apiKey={key}&type={road_type}&cctvType=1"
    f"&minX={minX}&maxX={maxX}"
    f"&minY={minY}&maxY={maxY}&getType={getType}"
)

# 5. 요청
response = urllib.request.urlopen(url_cctv)

# 6. bytes -> str -> dict ; 봉투뜯기 (왜 두변 변환??)
#   (왜 디코딩??) 서버는 인터넷 전송용 bytes(0 , 1 묶음)로 보냄
#                     -> 사람 ,파이썬이 읽으려는 한글 str(글자)로 풀어야함
#   (왜 JSON 파싱??) str은 글자 덩어리일뿐 -> 값 꺼내려면
#                      dict(파이썬 사전) 형태여야 ["키"]로 접근 가능
json_str = response.read().decode("utf-8")  #bytes -> str(사람글자)
# print(json_str)

json_object = json.loads(json_str)          #str -> dict (사전모양)
# print(json_object)

# 7. 데이터 프레임 변환
cctv_play = pd.json_normalize(
    json_object["response"]["data"], sep=''
)
# print(cctv_play)
#      roadsectionid      coordx  ...             cctvname                                            cctvurl
# 0                   126.261960  ...    [국도38] 태안 두야교회교차로  http://cctvsec.ktict.co.kr/4027/GS9cuqRaCq9cmh...
# 1                   126.612830  ...  [국도 21호선] 보령 봉황터널시점  http://cctvsec.ktict.co.kr/4107/YVJDetuWhH2gGu...
# 2                   126.595440  ...  [국도 21호선] 보령 봉황터널종점  http://cctvsec.ktict.co.kr/4108/uEw2V7VUiudn1P...
# 3                   126.617068  ...  [국도 21호선] 홍성 단아래사거리  http://cctvsec.ktict.co.kr/4109/XIgVIAd5Mc+EOX...
# 4                   126.463910  ...   [국도 29호선] 서산 석림사거리  http://cctvsec.ktict.co.kr/4120/bUjLufPLscQPC/...
# ...            ...         ...  ...                  ...                                                ...
# 1131                126.431750  ...      [국도77] 보령 원산교차로  http://cctvsec.ktict.co.kr/79943/AIoboCF598a09...
# 1132                126.426860  ...      [국도77] 보령 원의교차로  http://cctvsec.ktict.co.kr/79944/Cq4IS6LXWRVtz...
# 1133                126.427360  ...      [국도77] 보령 선촌교차로  http://cctvsec.ktict.co.kr/79945/M3e6nxxBpjsL2...
# 1134                126.422390  ...      [국도77] 태안 영목교차로  http://cctvsec.ktict.co.kr/79946/zEbVeHDV9LXKv...
# 1135                126.683466  ...  [국도38] 가곡지하차도(대산방향)  http://cctvsec.ktict.co.kr/79964/Bo6Q2k4U1wfpx...

# 8. CCTV URL 출력
test_url = cctv_play["cctvurl"][999]
print(f"선택된 CCTV URL : {test_url}")