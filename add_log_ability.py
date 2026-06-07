import json
import os

abilities_file = "abilities.json"

# Читаем текущие способности
with open(abilities_file, "r", encoding="utf-8") as f:
    abilities = json.load(f)

# Код для способности "анализ_лога"
log_code = '''
import os
log_file = 'kovcheg_log.txt'
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f'Всего записей в логе: {len(lines)}')
    print('Последние 5 записей:')
    for line in lines[-5:]:
        print(line.strip())
else:
    print('Лог не найден')
'''

# Добавляем способность
abilities["анализ_лога"] = log_code.strip()

# Сохраняем
with open(abilities_file, "w", encoding="utf-8") as f:
    json.dump(abilities, f, indent=2, ensure_ascii=False)

print("? Способность 'анализ_лога' добавлена")