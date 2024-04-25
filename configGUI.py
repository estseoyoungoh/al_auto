import tkinter as tk
from tkinter import simpledialog
import configparser
import os

def save_config(username, password, model_name, script_kor):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    config['ACCOUNT']['EMAIL'] = username
    config['ACCOUNT']['PW'] = password
    config['MODEL']['NAME'] = model_name
    config['SCRIPT']['kor'] = script_kor
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config['ACCOUNT']['EMAIL'], config['ACCOUNT']['PW'], config['MODEL']['NAME'], config['SCRIPT']['kor']

def on_submit(user_entry, pass_entry, model_entry,script_entry, root):
    username = user_entry.get()
    password = pass_entry.get()
    model_name = model_entry.get()
    script_kor = script_entry.get()
    save_config(username, password, model_name, script_kor )
    root.destroy()

def run_gui():
    root = tk.Tk()
    root.title("설정")

    # 창 크기/위치 설정
    root.geometry("500x300+500+500")

    tk.Label(root, text="로그인할 이메일:").grid(row=0)
    tk.Label(root, text="비밀번호:").grid(row=1)
    tk.Label(root, text="모델 이름:").grid(row=2)
    tk.Label(root, text="스크립트 (한글):").grid(row=3)

    user_entry = tk.Entry(root)
    pass_entry = tk.Entry(root, show="*")
    model_entry = tk.Entry(root)
    script_entry = tk.Entry(root)

    user_entry.grid(row=0, column=1)
    pass_entry.grid(row=1, column=1)
    model_entry.grid(row=2, column=1)
    script_entry.grid(row=3, column=1)

    current_user, current_pass, current_model, current_script = load_config()
    user_entry.insert(0, current_user)
    pass_entry.insert(0, current_pass)
    model_entry.insert(0, current_model)
    script_entry.insert(0, current_script)

    submit_btn = tk.Button(root, text="시작", command=lambda: on_submit(user_entry, pass_entry, model_entry,script_entry, root))
    submit_btn.grid(row=3, columnspan=2)

    root.mainloop()

if __name__ == '__main__':
    run_gui()