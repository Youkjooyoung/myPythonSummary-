from transformers   import pipeline

## 번역 함수 정의 및 모델 설정 (Hugging Face NLLB - 로컬 실행, 요청 제한 없음)
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M",
                      src_lang="eng_Latn", tgt_lang="kor_Hang")

def trans_en_to_kor(sentence):
    """
    영어문장 --> 한국어로 번역하는 함수

    """
    translate_sen = translator(sentence)[0]['translation_text']
    return translate_sen

# 1. 요약 파이프라인 생성
summarizer = pipeline("summarization", model="t5-small")

# 2. 요약할 원문
text = """#1 NEW YORK TIMES BESTSELLER - From the indie rock sensation known as Japanese Breakfast,
        an unforgettable memoir about family, food, grief,
        love, and growing up Korean American--
        "in losing her mother and cooking to bring her back to life,
        Zauner became herself" (NPR).
        - CELEBRATING OVER ONE YEAR ON THE NEW YORK TIMES BESTSELLER LIST
        In this exquisite story of family, food, 
        grief, and endurance, Michelle Zauner proves herself far more than a dazzling singer, 
        songwriter, and guitarist. With humor and heart, 
        she tells of growing up one of the few Asian American kids at her school in Eugene, Oregon; 
        of struggling with her mother's particular, high expectations of her; of a painful adolescence; 
        of treasured months spent in her grandmother's tiny apartment in Seoul, 
        where she and her mother would bond, late at night, over heaping plates of food."""

# 3. 요약문 생성
summary = summarizer(text)

# 4. 결과 텍스트로 추출 --> 출력
sum_text = summary[0]['summary_text']
print(f"======요약된 문장 : {sum_text}======")
# ======요약된 문장 : "in losing her mother and cooking to bring her back to life,
# Zauner became herself," she tells nPR .
# her memoir is a memoir about family, food, grief, love,
# and growing up Korean American .
# the author tells of growing up one of the few Asian American kids at her school .======

# 5. 요약문
kr_sum_text = trans_en_to_kor(sum_text)

# 6. 한국어 번역문 출력
print(f"======한국어 번역 문장 : {kr_sum_text}======")
# ======한국어 번역 문장 : "엄마를 잃고 다시 살리기 위해 요리하면서, 자너는 자신을 되었다"고 
# 그녀는 nPR에 말한다. 그녀의 회고록은 가족, 음식, 슬픔, 사랑,
# 그리고 한국계 미국인 성장에 대한 회고록이다. 
# 저자는 그녀의 학교에서 몇 안 되는 아시아계 미국인 아이들 중 한 명 중 
# 한 명 중 한 명 중 한 명 중 한 명 중 한 명 중 
# 한 명으로 성장했다는이야기를 한다.======


