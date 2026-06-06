import json
import os

abilities_file = "abilities.json"

# Читаем текущие способности
with open(abilities_file, "r", encoding="utf-8") as f:
    abilities = json.load(f)

# Код для способности "txt_to_docx" (упрощённый)
txt_to_docx_code = '''
import os
from docx import Document

folder = r"C:\\Users\\User\\Desktop\\трещина финал1"
files = [f for f in os.listdir(folder) if f.endswith(".txt")]

if not files:
    print("Нет txt файлов в папке")
else:
    for filename in files:
        txt_path = os.path.join(folder, filename)
        docx_path = os.path.join(folder, filename.replace(".txt", ".docx"))
        
        doc = Document()
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                doc.add_paragraph(line.strip())
        doc.save(docx_path)
        print(f"? {filename} -> {filename.replace('.txt', '.docx')}")
    print("Готово!")
'''

# Добавляем способность
abilities["txt_to_docx"] = txt_to_docx_code.strip()

# Сохраняем обратно
with open(abilities_file, "w", encoding="utf-8") as f:
    json.dump(abilities, f, indent=2, ensure_ascii=False)

print("? Способность 'txt_to_docx' добавлена")