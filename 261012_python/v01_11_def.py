import pyfiglet

# sentence = "PYTHON"
# py_senetence = pyfiglet.figlet_format(sentence)
# print(py_senetence)


def good_sentence(sentence: str):
    """
    입력된 문자를 pyfiglet를 이용하여 아스키 아트로 변환하고 출력하는 함수입니다.
    Args: sentence (str): 변환할 문자열
    반환 : None -- 출력만 수행
    """
    py_senetence = pyfiglet.figlet_format(sentence)
    print(py_senetence)


good_sentence("JUYOUNG")
