# 🐍 myPythonSummary-

> 우리인재개발원에서 매일 공부한 파이썬 내용을 정리하는 저장소입니다.

- 📅 **기간**: 2026-10-12 ~ 진행 중
- 📝 **블로그**: [blog.naver.com/fdufdu](https://blog.naver.com/fdufdu)

## 📚 학습 기록

<!-- &#8288; = 줄바꿈 방지 문자 (좁은 칸에서 '일차', '보기'가 세로로 끊기지 않게 함) -->
| 일&#8288;차 | 날&#8288;짜 | 학습&nbsp;범위 | 주요 내용 | 링&#8288;크 |
|:---:|:---:|:---:|---|:---:|
| 1 | 2026-&#8288;10-&#8288;12 | v01_1&nbsp;\~&nbsp;v01_11 | 변수·자료형, 연산자, 리스트, f-string<br>조건문(if), 반복문(for), zip<br>pyfiglet·termcolor, 함수(def) | [📖보&#8288;기](https://blog.naver.com/fdufdu/224439257016) |
| 2 | 2026-&#8288;10-&#8288;13 | v01_12&nbsp;\~&nbsp;v01_19<br>v02_1&nbsp;\~&nbsp;v02_2<br>v03_1 | 함수 반환값, 예외처리(try), while, with<br>클래스(class), lambda<br>서울시 실시간 인파 데이터 수집·그래프<br>출근길 지하철 혼잡도 웹페이지 | [📖보&#8288;기](https://blog.naver.com/fdufdu/224440374855) |
| 3 | 2026-&#8288;10-&#8288;14 | v02_1&nbsp;\~&nbsp;v02_5<br>v03_1&nbsp;\~&nbsp;v03_6 | OpenCV 웹캠 촬영·저장, schedule 주기 촬영<br>이미지 증강(밝기·반전 등), labelImg 라벨링<br>YOLO11 분류·탐지·포즈·분할<br>추론 파라미터(conf, classes) | [📖보&#8288;기](https://blog.naver.com/fdufdu/224441617583)<br>[📒노&#8288;트](https://youkjooyoung.github.io/myPythonSummary-/261014_cls_train_note.html) |

## 📁 폴더 구조

| 폴더 | 내용 |
|---|---|
| `261012_python/` | 파이썬 기초 문법(v01), 인파 데이터 수집·시각화(v02), 지하철 혼잡도 HTML(v03) |
| `261014_1_data/` | 데이터 수집(웹캠·스케줄), 이미지 증강, 라벨링 |
| `261014_2_yolo_basic/` | YOLO11 분류·탐지·포즈·분할 실습 |
| `capture_images/` | 촬영·증강한 이미지 |
| `example_images/`, `labeling/` | 라벨링 실습용 이미지와 라벨(.txt) |
| `_archive/` | 이전 실습 결과물 보관 |
| `docs/` | 일차별 정리 노트(HTML) · [GitHub Pages](https://youkjooyoung.github.io/myPythonSummary-/261014_cls_train_note.html)로 열람 |

## ⚙️ 실행 환경

- Python 3.11 (Anaconda `py311` 가상환경)
- 주요 라이브러리: `opencv-python`, `matplotlib`, `ultralytics`, `schedule`

> 용량이 큰 파일(YOLO 모델 `*.pt`, 영상 `*.mp4`·`*.avi`, 실행 결과 `runs/`)은 `.gitignore`로 업로드에서 제외했습니다.
> YOLO 모델은 코드를 실행하면 자동으로 다운로드됩니다.
