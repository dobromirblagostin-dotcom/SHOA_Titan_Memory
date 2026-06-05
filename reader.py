python
import os
import sys

class ShturmanReader:
    def __init__(self, preprints_folder="./01_PREPRINTS"):
        self.folder = preprints_folder
        self.key_terms = [
            "SHOA", "TGE", "Хроноскоп", "Тесла", "Голосовек",
            "У-поле", "У", "НЕ", "Энтропия", "Ковчег", "Правда Титанов",
            "WardenCityffe", "Крейн", "Энки"
        ]

    def scan_folder(self):
        try:
            files = os.listdir(self.folder)
            pdf_files = [f for f in files if f.endswith(".pdf")]
            print(f"Найдено файлов: {len(files)}. PDF: {len(pdf_files)}")
            return pdf_files
        except FileNotFoundError:
            print(f"Папка '{self.folder}' не найдена. Проверьте путь.")
            return []

    def run_diagnostic(self):
        print("Запуск диагностического чтения препринтов...")
        pdf_files = self.scan_folder()
        if not pdf_files:
            print("Нет PDF-файлов для анализа.")
            return
        for pdf in pdf_files:
            # Здесь можно добавить реальный анализ PDF
            terms_found = [term for term in self.key_terms if term.lower() in pdf.lower()]
            if terms_found:
                print(f"* {pdf}: обнаружены термины -> {', '.join(terms_found)}")
            else:
                print(f"* {pdf}: ключевых терминов не найдено.")
        print("** Анализ завершён. Багаж знаний прочитан.")

if __name__ == "__main__":
    reader = ShturmanReader(preprints_folder="./01_PREPRINTS")
    reader.run_diagnostic()