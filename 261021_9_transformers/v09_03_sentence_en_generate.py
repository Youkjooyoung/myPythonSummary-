from transformers   import pipeline

# 1. 텍스트 생성 파이프라인 생성
generator = pipeline("text-generation",model="gpt2")

# 2. 시드 문장 입력
q = input(" 생성 할 문장을 입력하세요 : ")

# 3. 생성 실행
result = generator(
    q,
    max_new_tokens=50,     # 추가 생성할 토큰 수(길수록 추론시간 길어짐)
    num_return_sequences=1, # 반환문장 개수
    truncation=True         #모델길이 초과시 자름
)

# 4. 결과 출력
print(result[0]["generated_text"])