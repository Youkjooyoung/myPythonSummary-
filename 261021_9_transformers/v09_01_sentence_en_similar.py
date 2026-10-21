# 1. 라이브러리 불러오기
from sentence_transformers  import  SentenceTransformer, util
#sentence_transformer -> 사전 학습 임베딩 모델 로더 클래스
#util -> 코사인 유사도 검색 등 보조 함수 묶음

# 2. 사전 학습 모델 로드
model = SentenceTransformer("all-MiniLM-L6-v2")
    # 모델 설명 : 영어 문장을 의미 공간에 맵핑, 빠름
    
# 3. 비교할 두 문장 정의
# (1)
# sen1 = "The cat is sleeping on the sopa"
# sen2 = "Tomorrow, I have a math exam at school"

# (2)
sen1 = "He is reading a book in the library"
sen2 = "He is at the library reading a book"

# (3)
sen1 = "mother"
sen2 = "mom"

# 4. 문장 --> 숫자 좌표로 바꾸기(인코딩)
emb1 = model.encode(sen1,convert_to_tensor=True)
emb2 = model.encode(sen2,convert_to_tensor=True)

# 5. 두 좌표가 얼마나 같은 방향인지 측정(코사인 유사도)
cos_sim = util.pytorch_cos_sim(emb1,emb2)

    # 값 범위 해석 : 
    #   -1 : 완전 반대 의미
    #   0 : 의미무관
    #   1 : 완전히 동일 의미

# 6. 결과 출력
print(f"두 문장의 유사도 : {cos_sim.item():.4f}")
#   두 문장의 유사도 : 0.0166  (1)
#   두 문장의 유사도 : 0.9723  (2)
#   두 문장의 유사도 : 0.8971  (3)