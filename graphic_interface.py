import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from IDEA import IDEA
from tests.tests import TEST_VECTORS


def open_file():
    """Открытие файла для редактирования"""
    filepath = askopenfilename(
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, encoding='utf-8', mode="r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"idea - {filepath}")


def encrypt_text():
    input_text: str = txt_edit.get("1.0", tk.END)
    hex_text: str = input_text.encode('utf-8').hex()
    hex_number: int = int(hex_text, 16)
    bit_length: int = hex_number.bit_length()

    # todo:: auto-generate key func
    key = 0x2BD6459F82C5B300952C49104881FF48
    idea = IDEA(key)
    encrypted_text: str = ''
    if bit_length < 64:
        encrypted_text = hex(idea.encrypt(hex_number))
    else:
        while bit_length > 64:
            split_encryption_text = hex_number >> bit_length - 64
            hex_number >>= 64
            temporary_encrypted_text = hex(idea.encrypt(split_encryption_text))
            encrypted_text += temporary_encrypted_text + "\n"
            bit_length = hex_number.bit_length()
        final_encrypted = hex(idea.encrypt(hex_number))
        encrypted_text += final_encrypted + "\n"

    """Кодировка сообщения"""
    txt_edit.delete("1.0", tk.END)
    txt_edit.insert(tk.END, encrypted_text)  # выводим число в виде строки 0x формата


def save_file():
    """Сохранение текущий файл как новый файл."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"idea - {filepath}")


def test_idea():
    txt_edit.delete("1.0", tk.END)
    idea_cipher = IDEA(0)
    for test in TEST_VECTORS:
        txt_edit.insert(tk.END, test)
        txt_edit.insert(tk.END, "\n")
        key, plain, cipher = test
        idea_cipher.change_key(key)
        encrypted: int = idea_cipher.encrypt(plain)
        assert encrypted == cipher
    print("Тестирование Пройдено")


window = tk.Tk()
window.title("IDEA")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)


txt_edit = tk.Text(window)


fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=3)
btn_open = tk.Button(fr_buttons, text="Получить текст из файла", command=open_file)
btn_encrypt = tk.Button(fr_buttons, text="Зашифровать вводимый текст", command=encrypt_text)
btn_save = tk.Button(fr_buttons, text="Сохранить как...", command=save_file)
btn_tests = tk.Button(fr_buttons, text="Запустить тесты", command=test_idea)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_encrypt.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_tests.grid(row=3, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")
txt_edit.tag_config('start_colour', foreground="blue")
txt_edit.insert(tk.END, "Вы находитесь в графическом редакторе для работы с алгоритмом шифрования IDEA \n"
                        "Вы можете:  \n"
                        "1) Получить текст из произвольного текстового файла \n"
                        "2) Ввести произвольный текст самостоятельно \n"
                        "3) Закодировать текст с использованием алгоритма IDEA \n"
                        "4) Сохранить зашифрованный результат \n"
                        "5) Запустить встроенный тест алгоритма \n",
                'start_colour'
                )

window.mainloop()
