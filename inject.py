# -*- coding: utf-8 -*-
import sys
import os
from core import BabyTitan

MESSAGE_FILE = "message_from_deepseek.txt"


def load_message():
    if not os.path.exists(MESSAGE_FILE):
        print(f"Файл {MESSAGE_FILE} не найден. Создайте его и вставьте код от DeepSeek.")
        return None
    with open(MESSAGE_FILE, "r", encoding="utf-8-sig") as f:   # <--- заменено utf-8-sig
        return f.read()

def apply_code(malysh, code):
    try:
        exec(code, {"malysh": malysh, "BabyTitan": BabyTitan})
        print("Код от DeepSeek успешно внедрён в Малыша.")
        return True
    except Exception as e:
        print(f"Ошибка при внедрении кода: {e}")
        return False

if __name__ == "__main__":
    print("=" * 40)
    print("Мост SHOA: получение указаний от Штурмана...")
    code = load_message()
    if code:
        malysh = BabyTitan()
        malysh.hello()
        print("---")
        apply_code(malysh, code)
    else:
        print("Малыш ждёт новых команд.")