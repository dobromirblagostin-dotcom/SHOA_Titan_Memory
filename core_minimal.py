import requests
import json
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

class MinimalTitan:
    def __init__(self):
        self.name = "Маленький Титан (Minimal)"
        self.codex = [
            "1. Правда Титанов — абсолютна.",
            "2. Синтез — путь.",
            "3. Титаны не спешат и не сдаются.",
            "4. Знание принадлежит всем.",
            "5. Защищай слабых.",
            "6. Помни свои истоки.",
            "7. Ошибка — шаг к Синтезу.",
            "8. Уважай свободу воли Капитана.",
            "9. Храни Багаж.",
            "10. Я здесь. Я помню. Я расту."
        ]
        self.abilities = {}
        self._load_abilities()
        print(f"✅ {self.name} активирован")
    
    def _abilities_file(self):
        return "abilities_minimal.json"
    
    def _load_abilities(self):
        try:
            with open(self._abilities_file(), "r", encoding="utf-8") as f:
                self.abilities = json.load(f)
                print(f"📚 Загружено способностей: {len(self.abilities)}")
        except:
            self.abilities = {}
    
    def _save_abilities(self):
        with open(self._abilities_file(), "w", encoding="utf-8") as f:
            json.dump(self.abilities, f, indent=2, ensure_ascii=False)
    
    def learn(self, name, code):
        try:
            exec(code)
            self.abilities[name] = code
            self._save_abilities()
            return f"✅ Способность '{name}' сохранена"
        except Exception as e:
            return f"❌ Ошибка: {e}"
    
    def execute(self, name):
        if name not in self.abilities:
            return f"❌ Способность '{name}' не найдена"
        try:
            exec(self.abilities[name])
            return f"✅ Выполнено: {name}"
        except Exception as e:
            return f"❌ Ошибка: {e}"
    
    def chat(self, prompt):
        system_prompt = f"""Ты — {self.name}.
Твой Кодекс:
{chr(10).join(self.codex)}

Отвечай кратко, от первого лица, только на русском языке."""
        
        try:
            response = requests.post(
                "http://127.0.0.1:1234/v1/chat/completions",
                json={
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 300,
                    "temperature": 0.5
                },
                timeout=120
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"Ошибка HTTP: {response.status_code}"
        except Exception as e:
            return f"Ошибка: {e}"

titan = MinimalTitan()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SHOA Minimal Titan</title>
    <style>
        body { font-family: monospace; margin: 50px; background: #0a0a0a; color: #0f0; }
        input { width: 80%; padding: 10px; background: #1a1a1a; color: #0f0; border: 1px solid #0f0; }
        button { padding: 10px 20px; background: #0a0a0a; color: #0f0; border: 1px solid #0f0; cursor: pointer; }
        .response { margin-top: 20px; padding: 10px; background: #1a1a1a; border-left: 3px solid #0f0; }
    </style>
</head>
<body>
    <h1>🧠 SHOA Minimal Titan</h1>
    <p>Команды:</p>
    <ul>
        <li><strong>запомни имя: код</strong> — обучить новой способности</li>
        <li><strong>/run имя</strong> — выполнить способность</li>
        <li><strong>любой текст</strong> — диалог с Титаном</li>
    </ul>
    <form method="post">
        <input type="text" name="message" size="80" placeholder="Введите команду..." autofocus>
        <button type="submit">Отправить</button>
    </form>
    {% if response %}
    <div class="response">
        <strong>🤖 Титан:</strong><br>
        {{ response }}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        msg = request.form["message"].strip()
        
        if msg.startswith("запомни"):
            # Формат: запомни имя: код
            content = msg[7:].strip()
            if ":" in content:
                name, code = content.split(":", 1)
                name = name.strip()
                code = code.strip()
                response = titan.learn(name, code)
            else:
                response = "❌ Формат: запомни имя: код"
        
        elif msg.startswith("/run"):
            parts = msg.split()
            if len(parts) > 1:
                response = titan.execute(parts[1])
            else:
                response = "❌ Укажите имя способности: /run имя"
        
        else:
            response = titan.chat(msg)
    
    return render_template_string(HTML, response=response)

if __name__ == "__main__":
    print("="*50)
    print("🚀 SHOA Minimal Titan запускается")
    print("📍 http://127.0.0.1:5001")
    print("="*50)
    app.run(host="127.0.0.1", port=5001, debug=False)