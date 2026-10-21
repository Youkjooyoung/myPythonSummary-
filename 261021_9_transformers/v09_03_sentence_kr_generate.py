from transformers   import pipeline

# 1. 텍스트 생성 파이프라인 생성( 모델 변경 )
generator = pipeline("text-generation", model="skt/kogpt2-base-v2")

# 2. 시드 문장 입력
q = input(" 생성 할 문장을 입력하세요 : ")

# 3. 생성 실행
result = generator(
    q,
    max_new_tokens=50,
    do_sample=True,          # 샘플링 사용 (매번 다른 문장)
    top_p=0.9,
    temperature=0.8,
    repetition_penalty=1.2,  # 같은 말 반복 억제 (작은 모델에 중요)
    truncation=True
)

# 4. 결과 출력
print(result[0]["generated_text"])

# 생성 할 문장을 입력하세요 : 안녕하세요 나는 대한민국 사람입니다.

# 생성 된 문장 :
# 안녕하세요 나는 대한민국 사람입니다. 내겐 대한민국이 있습니다. 내가 오늘 이 자리에 나왔기 때문에 정말 감사합니다.
# 그리고 제가 너무 자랑스럽고 행복해요.
# 제게 주어진 사명감이 얼마나 중요한지 깨달았어요! 저는 국민여러분께 대통령님께서 말씀해주신 대로