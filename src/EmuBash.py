from tkinter import *
import os
from tkinter import ttk


T_WINDOW_W = 1000
T_WINDOW_H = 800
T_WINDOW_PAD_X = 50
T_WINDOW_PAD_Y = 50
INPUT_PAD_X = 8
INPUT_PAD_Y = 8
COMMANDS = ['ls', 'cd', 'exit']

CODE_SUCCESS = 0
CODE_INVALID_COMMAND = 1
CODE_INVALID_ARGUMENT = 2
CODE_EMPTY_FIELD = 3


def t_window_init():
    """Инициализация главного окна приложения и области вывода."""
    global t_window, output_text, input_frame
    t_window = Tk()
    t_window.title("My VFS")
    t_window.geometry(
        f"{T_WINDOW_W}x{T_WINDOW_H}+{T_WINDOW_PAD_X}+{T_WINDOW_PAD_Y}"
    )
    t_window.resizable(False, False)

    output_text = Text(
        t_window,
        bg="black",
        fg="white",
        insertbackground="white",
        font=("monospace", 11),
        wrap=WORD,
    )
    output_text.pack(fill=BOTH, expand=True, padx=8, pady=(8, 0))

    input_frame = ttk.Frame(t_window)
    input_frame.pack(fill=X, side=BOTTOM, padx=8, pady=8)

    user_name = os.getlogin()
    host_name = os.uname().nodename
    symbol = '#' if os.getuid() == 0 else "$"
    user_curr_dir = "~"

    prefix = ttk.Label(
        input_frame,
        text=f"{user_name}@{host_name}:{user_curr_dir}{symbol}"
    )
    prefix.pack(side=LEFT)


def ls_process(command, arguments):
    """Обработка команды ls."""
    return f"{command} {' '.join(arguments)}"


def cd_process(command, arguments):
    """Обработка команды cd."""
    return f"{command} {' '.join(arguments)}"


def command_handle_process(command: str, args=[], code: int=CODE_EMPTY_FIELD):
    """Обработка команды и вывод результата в зависимости от кода."""
    if code == CODE_INVALID_COMMAND:
        text = f"{command}: Invalid command"
    elif code == CODE_SUCCESS:
        if command == 'ls':
            text = ls_process(command, args)
        elif command == "exit":
            t_window.quit()
        elif command == 'cd':
            text = cd_process(command, args)
    elif code == CODE_EMPTY_FIELD:
        return
    output_write(text)


def enter_handle_process(event):
    """Обработка нажатия Enter в поле ввода команды."""
    text = input_line.get().split()

    command = text[0]
    arguments = text[1:]
    if command not in COMMANDS:
        if command == '':
            command_handle_process(command, arguments, CODE_EMPTY_FIELD)
        else:
            command_handle_process(command, arguments, CODE_INVALID_COMMAND)
    elif command in COMMANDS:
        command_handle_process(command, arguments, CODE_SUCCESS)



def output_write(text: str = ""):
    """Запись текста в область вывода."""
    output_text.config(state=NORMAL)
    output_text.insert(END, text + "\n")
    output_text.config(state=DISABLED)
    output_text.see(END)

if __name__ == '__main__':
    t_window_init()
    input_line = ttk.Entry(input_frame)
    input_line.pack(
        fill=X, side='left', padx=INPUT_PAD_X,
        pady=INPUT_PAD_Y, expand=True
    )
    input_line.focus()
    t_window.bind('<Return>', enter_handle_process)
    t_window.mainloop()
