import streamlit as st  # 웹앱 만드는 도구
from ultralytics import YOLO
import cv2

# 1. Streamlit 페이지 기본 설정 -> 웹 화면 모양 결정
st.set_page_config(layout="wide")   # 화면을 가로로 넓게 사용
st.title("YOLO 실시간 CCTV 탐지")    # 페이지 맨 위의 제목 표시

# 2. 영상 출력용 공간 설정 --> 영상이 들어갈 빈 액자 준비
frame_placeholder = st.empty()      # 사진을 계속 갈아끼울 자리

# 3. CCTV 비디오 스트림 연결 --> 인터넷 CCTV 카메라 접속
cap = cv2.VideoCapture("http://210.99.70.120:1935/live/cctv066.stream/playlist.m3u8")

# 4. 모델 로드 --> 사물 인식 AI 두뇌 불러오기
model = YOLO("yolo11n.pt")

# 5. 비디오 프레임 처리 --> CCTV 영상을 한 장씩 분석 반복
while cap.isOpened():
    success , frame =cap.read()
    if not success:
        print("프레임 읽기 실패")
        st.warning("프레임 확인바람 . . .")
        break
    
    # 5-1. 모델로 객체 탐지 수행
    results = model(frame)
    
    # 5-2. 탐지결과를 이미지에 시각화
    annotated_fream = results[0].plot()
    
    # 5-3 . Streamlit placeholder에 프레임 갱신
    frame_placeholder.image(annotated_fream,channels="BGR")

# 6. 자원해제
cap.release()
cv2.destroyAllWindows()
