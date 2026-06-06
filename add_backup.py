import json
import os

abilities_file = "abilities.json"

with open(abilities_file, "r", encoding="utf-8") as f:
    abilities = json.load(f)

abilities["backup_abilities"] = "import shutil, datetime; backup_name = 'abilities_backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'; shutil.copy('abilities.json', backup_name); print('Создан бэкап: ' + backup_name)"

with open(abilities_file, "w", encoding="utf-8") as f:
    json.dump(abilities, f, indent=2, ensure_ascii=False)

print("✅ backup_abilities добавлена")