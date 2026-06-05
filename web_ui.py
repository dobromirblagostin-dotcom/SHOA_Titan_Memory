from flask import Flask, request, jsonify, render_template_string
from core import BabyTitan
import webbrowser
import json
import os
from datetime import datetime

app = Flask(__name__)
titan = BabyTitan()
HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Малыш Титан SHOA</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #0a0a2a; color: #eee; }
        textarea { width: 100%; background: #1a1a3a; color: #eee; border: 1px solid #4a4a8a; }
        button { background: #2a6a8a; color: white; padding: 10px 20px; border: none; cursor: pointer; margin: 5px; }
        button:hover { background: #3a8aaa; }
        #answer { border: 1px solid #4a4a8a; padding: 15px; margin-top: 15px; min-height: 100px; background: #0f0f2f; }
        #history { border: 1px solid #4a4a8a; padding: 15px; margin-top: 20px; max-height: 300px; overflow-y: auto; background: #0f0f2f; }
        .message { margin: 10px 0; padding: 8px; border-bottom: 1px solid #2a2a5a; }
        .user { color: #8af; }
        .bot { color: #af8; }
        pre { white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>🤖 Маленький Титан SHOA</h1>
    <div id="code"></div>
    <textarea id="question" rows="4" placeholder="Задайте вопрос..."></textarea><br>
    <button onclick="ask()">Спросить</button>
    <button onclick="clearHistory()">Очистить историю</button>
    <div id="answer"></div>
    <div id="history"><h3>📜 История диалога:</h3></div>
    <script>
        async function ask() {
            let q = document.getElementById('question').value;
            let resp = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: q})
            });
            let data = await resp.json();
            document.getElementById('answer').innerHTML = '<strong>Ответ:</strong><br>' + data.answer;
            document.getElementById('question').value = '';
            loadHistory();
        }
        
        async function clearHistory() {
            await fetch('/clear_history', {method: 'POST'});
            loadHistory();
        }
        
        async function loadHistory() {
            let resp = await fetch('/get_history');
            let data = await resp.json();
            let historyDiv = document.getElementById('history');
            historyDiv.innerHTML = '<h3>📜 История диалога:</h3>';
            for (let msg of data.history) {
                historyDiv.innerHTML += '<div class="message"><span class="user">👤 ' + msg.user + '</span><br><span class="bot">🤖 ' + msg.bot + '</span></div>';
            }
        }
        
        // Загружаем историю при старте
        loadHistory();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt', '')
    answer = titan.think(prompt)
    
    # Сохраняем в историю
    history = load_history()
    history.append({
        "user": prompt,
        "bot": answer,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_history(history)
    
    return jsonify({'answer': answer})

@app.route('/get_history', methods=['GET'])
def get_history():
    history = load_history()
    return jsonify({'history': history})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    save_history([])
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(host='127.0.0.1', port=5000, debug=False)