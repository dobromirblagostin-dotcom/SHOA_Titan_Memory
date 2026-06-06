import json
import os

# Путь к abilities.json
abilities_file = "abilities.json"

# Читаем текущие способности
with open(abilities_file, "r", encoding="utf-8") as f:
    abilities = json.load(f)

# Код для способности "ключ"
key_code = """
import os
path = os.path.join(os.path.dirname(__file__), 'temporal_law.txt')
try:
    with open(path, 'r', encoding='utf-8') as f:
        print(f.read())
except Exception as e:
    print(f'Ошибка: {e}')
"""

# Добавляем способность
abilities["ключ"] = key_code.strip()

# Сохраняем обратно
with open(abilities_file, "w", encoding="utf-8") as f:
    json.dump(abilities, f, indent=2, ensure_ascii=False)

print("? Способность 'ключ' добавлена в abilities.json")