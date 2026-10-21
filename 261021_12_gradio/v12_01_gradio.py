import gradio as gr

# 1. 간단하 함수 정의
def say_hello(name):
    return "HELLO" + name

# 2. Gradio 인터페이스 생성
gr_web = gr.Interface(
    fn=say_hello,   # 실행할 함수
    inputs="text",  # 텍스트 입력창
    outputs="text"  # 텍스트 출력창
)

# 3. 웹앱 실행 ( share = True -->공개 URL)
gr_web.launch(share=True)
