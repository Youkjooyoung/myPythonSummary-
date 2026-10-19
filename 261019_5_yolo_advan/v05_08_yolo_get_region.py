import cv2

# 1. 비디오 경로 설정
cap = cv2.VideoCapture("https://cctvsec.ktict.co.kr/6571/f0XwBug391mTlh0/btmMDU2sVR4LgiEVl4E3UpO1SIpsVSS9D1dyOeaLvh/JxY63")

ponits = []

# 2. 마우스 이벤트 처리 콜백 함수 정의
def mouse_callback(event, x, y, flags, param):
    """
    마우스 이벤트 콜백 함수
    - 좌 클릭 시 좌표를 points 리스트에 추가
    - 좌표 출력
    """
    if event == cv2.EVENT_LBUTTONDOWN: # 좌 클릭 이벤트 감지
        ponits.append((x,y))
        print(f"클릭된 좌표는 {x, y}입니다.")
        
# 3. 윈도우 창 설정 및 콜백 함수 등록
cv2.namedWindow("GET_X_Y", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("GET_X_Y", mouse_callback)

# 4. 비디오 프레임 처리
while cap.isOpened():
    success , frame = cap.read()
    if not success:
        print("프레임확인 바람")
        break
    
    # 4-1. 프레임 크기 조정(640 * 480)
    re_frame = cv2.resize(frame,(640, 480))
    
    # 4-2. 프레임 시각화
    cv2.imshow("GET_X_Y", re_frame)
    
    # 4-3. q키를 눌러서 종료
    if cv2.waitKey(20) & 0xFF == ord('q'):
        print("q키를 눌러 종료")
        break
    
# 5. 자원 해제
cap.release()
cv2.destroyAllWindows()

# 6. 좌표 사용안내
