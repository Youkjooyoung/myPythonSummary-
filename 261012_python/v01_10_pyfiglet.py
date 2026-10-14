import pyfiglet
from termcolor import colored

# py_text = pyfiglet.figlet_format("Hello, World!")
# color_text = colored(py_text, "red")
# print(color_text)

py_text = pyfiglet.figlet_format("PYTHON")
color_text = colored(py_text, "blue", "on_dark_grey", ["bold"])
print(color_text)
