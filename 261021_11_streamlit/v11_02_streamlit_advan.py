import streamlit as st
from ultralytics import YOLO
import cv2
import pandas as pd             # 엑셀 같은 데이터 타입으로 만드는 도구
import time                     # 시간측정
import plotly.express as px     # 그래프 그리는 도구

# 1. 화면 구성 
# 좌/우 2개 컬럼 생성
col1, col2 = st.columns(2)

with col1:
    frame_placeholder = st.empty()  #왼쪽 컬럼 YOLO 프레임 표시용

with col2:
    chart_placeholder = st.empty()  #오른쪽 컬럼 객체 수 차트 표시용
     
# 2. 비디오 경로 설정
cap = cv2.VideoCapture("http://210.99.70.120:1935/live/cctv066.stream/playlist.m3u8")

# 3. 모델 로드
def load_model():
    return YOLO("yolo11n.pt")

model = load_model()

# 4. 비디오 프레임 처리
while cap.isOpened():
    success , frame = cap.read()
    if not success:
        st.warning("CCTV FRAME ERROR")
        break
    
    # 4-1. YOLO 모델 객체 탐지 수행
    results = model(frame)
    
    # 4-2. 탐지 결과가 그려진 프레임 이미지 생성
    annotated_frame = results[0].plot()
    
    # 4-3. 탐지된 객체의 클래스 이름 추출
    labels = [model.names[int(c)] for c in results[0].boxes.cls]
    
    # 4-4. 탐지 객체수 시각화
    if labels:
        df_count = pd.DataFrame({"Object" : labels})
        df_count = df_count.value_counts().reset_index(name="Count")
        
        # Plotly를 이용해 막대그래프 생성
        fig = px.area(  #area로 변경한것 -> 이전 bar
            df_count,
            x="Object",
            y="Count",
            title="탐지 객체 수",
            color="Object",
            text="Count"
        )
    else:
        df_count = pd.DataFrame({"Object": [], "Count": []})
        
        #빈 표 만들기
        fig = px.area(  #area로 변경한것 -> 이전 bar
            df_count,
            x="Obejct",
            y="Count",
            title="탐지 객체 수"
        )
        
        # 4-5. Streamlit에 결과 표시 
         
    frame_placeholder.image(annotated_frame, channels="BGR")
    chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"chart_{time.time()}")
        
# 5. 자원해제
cap.release()
cv2.destroyAllWindows()

