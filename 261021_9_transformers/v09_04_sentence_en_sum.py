from transformers   import pipeline
# pip install transformer==5.20.2
#다운그레이드
#pip install transformers==4.57.6

# 1. 요약 파이프라인 생성
summarizer = pipeline("summarization", model="t5-small")

# 2. 요약할 원문
text = """A special 25th anniversary edition of the extraordinary
international bestseller... Santiago's journey teaches us about
the essential wisdom of listening to our hearts..."""

# 3. 요약 실행
summary = summarizer(
    text,
    min_length=20,
    max_length=60,
    do_sample=False
)

# 4. 결과 텍스트로 추출 --> 출력
sum_text = summary[0]['summary_text']
print(f"요약된 문장 : {sum_text}")
#요약된 문장 : 25th anniversary edition of the extraordinary international bestseller.
# Santiago's journey teaches us about the essential wisdom of listening to our hearts 