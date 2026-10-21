from transformers   import  pipeline

# 1. 감정 분석 파이프라인 생성
clssfier = pipeline("sentiment-analysis")

# 2. 분석할 문장 입력 --> 추론 실행
# # (1)
# text = "I'm feeling really great today"  POSITIVE

# # (2)
# text = "he is die"      # NEGATIVE

# # (3)
# text = "No"
# # 감정 분석 결과 : NEGATIVE
# # 감정 분석 점수 : 0.9964

# # (4)
# text = "angel"
# # 감정 분석 결과 : POSITIVE
# # 감정 분석 점수 : 0.9971

#================ 한국어 기준 ================#
# 1. NEGATIVE
# text = "죽여라."
# 감정 분석 결과 : POSITIVE
# 감정 분석 점수 : 0.5691  ===> 부정적인 뜻이지만 긍정적으로 추론

# 2.POSITIVE
# text = "사랑해요."
# 감정 분석 결과 : POSITIVE
# 감정 분석 점수 : 0.9000

# text = "좋아함"
# 감정 분석 결과 : NEGATIVE
# 감정 분석 점수 : 0.6971  ===> 긍정적인 뜻이지만 부정적으로 추론
#================ 한국어 기준 끝 ================#

# (2)의 결과
# 감정 분석 결과 : NEGATIVE
# 감정 분석 점수 : 0.9984

results = clssfier(text)

# 3. 결과 확인(1번, 2번결과는 위에. . .)
# POSITIVE OR NEGATIVE --> ??
print(f"감정 분석 결과 : {results[0]['label']}")    
# 감정 분석 결과 : POSITIVE

# 0 ~ 1 확률 : 4f로 소수 4자리 포맷 --> 1에 가까울수록 확신도 높음
print(f"감정 분석 점수 : {results[0]['score']:.4f}")
# 감정 분석 점수 : 0.9999
