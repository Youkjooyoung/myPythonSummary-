from ultralytics import solutions

# 1. 검색 앱 생성 - CPU에서 동작(GPU면 "CUDA")
app = solutions.SearchApp(
    data = "demo_data",    # 내사진 폴더(선택)
    device="cpu"
)

# 2. 웹 서버 실행 ->     브라우저에서 http://127.0.0.1:5000 접속
app.run(debug=True)     #개발용 / 운영 시 False