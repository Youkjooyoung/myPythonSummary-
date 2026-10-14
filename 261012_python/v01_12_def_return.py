import pyfiglet
from termcolor import colored

def make_highlight(text: str) -> None:
    
    """
    입력된 문자열을 pyfiglet, termcolor를 이용하여 꾸며준다.
    
        매개변수 : text (str) : 꾸며줄 문자열
    """
    py_text = pyfiglet.figlet_format(text)
    color_py_text = colored(py_text,"red")
    return color_py_text

result = make_highlight("Hello World")

print(result)


    #make_highlight 함수를 터미널에서 출력되게 해주세요.