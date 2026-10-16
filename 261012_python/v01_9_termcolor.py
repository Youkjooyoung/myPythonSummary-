from termcolor import colored

# color(문자열, 글자색, 배경색, attrs = [스타일])
color_setence = colored("Hello, World!", "red", "on_blue", ["bold"])
print(color_setence)
