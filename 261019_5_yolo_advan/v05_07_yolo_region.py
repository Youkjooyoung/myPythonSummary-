from ultralytics import solutions
import cv2
import math

# 1.비디오 경로 설정(CCTV 스트림)
cap = cv2.VideoCapture("https://cctvsec.ktict.co.kr/6571/f0XwBug391mTlh0/btmMDU2sVR4LgiEVl4E3UpO1SIpsVSS9D1dyOeaLvh/JxY63")

# 2. 구역 좌표 설정 (dist 형식 = 키로 영역 구분)
    #클릭된 좌표는 (269, 179)입니다.
    #클릭된 좌표는 (6, 422)입니다.
    #클릭된 좌표는 (204, 473)입니다.
    #클릭된 좌표는 (333, 191)입니다

# 2-1. 원(타원) 좌표 생성 함수 : 중심(cx, cy), 가로 반지름 rx, 세로 반지름 ry, 점 개수 n
def make_circle(cx, cy, rx, ry=None, n=36):
    ry = rx if ry is None else ry          # ry 생략 시 정원
    return [
        (int(cx + rx * math.cos(2 * math.pi * i / n)),
         int(cy + ry * math.sin(2 * math.pi * i / n)))
        for i in range(n)
    ]

region_points = {
    "region1" : [(269, 179), (6, 422),(204, 473), (333, 191)],
    # region1 을 화면 중앙(x=320) 기준 좌우 반전 : x' = 640 - x
    "region2" : [(371, 179), (634, 422), (436, 473), (307, 191)],
    # 원 모양 구역 : 중심 (330, 120), 반지름 40 (점 12개 → 간격 약 21px라 점이 겹치지 않음)
"region3" : make_circle(330, 120, 40, n=12),
}

# 3. 모델 로드 및 구역 객체 생성
yolo_region =solutions.RegionCounter(
    model ="yolo11n.pt",
    show = False,
    region = region_points,
)

# 4. 프레임 처리
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print(" 프레임 확인")
        break
    # 4-1. 프렝미 크기 조정(좌표계 통일)
    re_frame =  cv2.resize(frame, (640, 480))
    
    # 4-2. 구역 내 객체 수 계산
    results = yolo_region(re_frame)
    
    # 4-3. 처리된 프레임 표시(show = False -> 우리가 창을 직접띄움)
    cv2.imshow("RESION", results.plot_im)
    
    # 4-4. 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("q 를 눌러 종료")
        break
    
# 5. 자원 해제
cap.release()
cv2.destroyAllWindows()