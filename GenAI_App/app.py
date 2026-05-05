import os
import json
import time
from flask import Flask, request, jsonify, render_template_string
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Premium UI Template with Markdown Support
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RA100 TensorX | GenAI Suite</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --primary: #76b900;
            --primary-dark: #5a8e00;
            --bg: #0b0e14;
            --card-bg: #161b22;
            --text: #e6edf3;
            --text-dim: #8b949e;
            --border: #30363d;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Inter', sans-serif; 
            background-color: var(--bg); 
            color: var(--text);
            line-height: 1.6;
        }

        .navbar {
            padding: 1.2rem 2rem;
            background: rgba(11, 14, 20, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo { font-weight: 700; font-size: 1.4rem; color: var(--primary); display: flex; align-items: center; gap: 10px; }

        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 1fr 1.5fr;
            gap: 2rem;
        }

        @media (max-width: 950px) { .container { grid-template-columns: 1fr; } }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            display: flex;
            flex-direction: column;
        }

        h2 { margin-bottom: 1.2rem; font-weight: 600; color: var(--primary); font-size: 1.2rem; }

        .input-group { margin-bottom: 1.2rem; }
        label { display: block; margin-bottom: 0.5rem; color: var(--text-dim); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
        
        input[type="text"], select {
            width: 100%;
            background: #0d1117;
            border: 1px solid var(--border);
            color: var(--text);
            padding: 0.9rem;
            border-radius: 8px;
            font-family: inherit;
            font-size: 1rem;
            transition: all 0.2s;
        }
        input[type="text"]:focus { border-color: var(--primary); outline: none; background: #1c2128; }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 0.9rem 1.5rem;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            border: none;
            width: 100%;
            font-size: 1rem;
            text-transform: uppercase;
        }

        .btn-primary { background: var(--primary); color: #000; }
        .btn-primary:hover { background: var(--primary-dark); transform: translateY(-1px); }
        .btn-secondary { background: #30363d; color: var(--text); margin-top: 1rem; }

        .result-box {
            margin-top: 1.2rem;
            background: #0d1117;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            min-height: 120px;
            border-left: 4px solid var(--primary);
            overflow-x: auto;
        }

        .chat-section { height: 700px; }
        .chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
            background: #0d1117;
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 1rem;
        }

        .message {
            max-width: 90%;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            font-size: 0.95rem;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .user-msg { align-self: flex-end; background: var(--primary); color: #000; font-weight: 500; }
        .ai-msg { align-self: flex-start; background: #21262d; color: var(--text); border: 1px solid var(--border); }

        /* Markdown Styles */
        .ai-msg h1, .ai-msg h2, .ai-msg h3 { color: var(--primary); margin: 1rem 0 0.5rem 0; }
        .ai-msg ul, .ai-msg ol { margin-left: 1.5rem; margin-bottom: 1rem; }
        .ai-msg p { margin-bottom: 0.8rem; }
        .ai-msg code { background: #000; padding: 2px 5px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; }

        .chat-input-area { display: flex; gap: 10px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="var(--primary)"><path d="M12 2L1 21h22L12 2zm0 3.45l8.27 14.3H3.73L12 5.45zM11 16h2v2h-2v-2zm0-7h2v5h-2V9z"/></svg>
            RA100 <span style="color: var(--text-dim); font-weight: 300;">| TensorX Suite</span>
        </div>
        <div style="font-size: 0.75rem; color: var(--primary); border: 1px solid var(--primary); padding: 4px 10px; border-radius: 4px; font-weight: bold;">v2.0 LIVE</div>
    </nav>

    <div class="container">
        <!-- Controller -->
        <div class="card">
            <h2>⚡ Inference Engine</h2>
            <div class="input-group">
                <label>System Domain</label>
                <select id="task-type">
                    <option value="medical">Health & Medical Diagnostics</option>
                    <option value="vision">Security & Vision Systems</option>
                    <option value="sensor">Industrial Sensor Fusion</option>
                </select>
            </div>

            <div class="input-group">
                <label>Input Description</label>
                <input type="text" id="raw-input" placeholder="e.g. Patient reports fatigue and dry cough...">
            </div>

            <button class="btn btn-primary" onclick="runInference()" id="infer-btn">🚀 Run TensorRT Prediction</button>
            <div class="result-box" id="trt-output">Awaiting input...</div>
            <button class="btn btn-secondary" onclick="explainResult()" id="explain-btn" style="display: none;">✨ Explain Findings</button>
        </div>

        <!-- Chat -->
        <div class="card chat-section">
            <h2>🧠 Explainable AI (XAI)</h2>
            <div class="chat-messages" id="chat-messages">
                <div class="message ai-msg">Welcome, researcher. Describe a situation on the left to begin the XAI analysis.</div>
            </div>
            <div class="chat-input-area">
                <input type="text" id="user-input" placeholder="Ask a follow-up question..." onkeypress="if(event.key === 'Enter') sendMessage()">
                <button class="btn btn-primary" style="width: auto;" onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        let lastResult = null;
        let history = [];

        async function runInference() {
            const btn = document.getElementById('infer-btn');
            const output = document.getElementById('trt-output');
            const input = document.getElementById('raw-input').value;
            
            if (!input) return alert("Please describe the input first!");

            btn.disabled = true;
            output.textContent = "Optimizing Graph... Running FP16 Inference...";

            try {
                const res = await fetch('/api/infer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task: document.getElementById('task-type').value, text: input })
                });
                lastResult = await res.json();
                output.textContent = JSON.stringify(lastResult, null, 2);
                document.getElementById('explain-btn').style.display = 'block';
            } catch (e) {
                output.textContent = "Error: " + e.message;
            } finally {
                btn.disabled = false;
            }
        }

        function explainResult() {
            const prompt = `Provide a detailed, formatted explanation of these results. Use headers and bullet points: \\n\\n` + JSON.stringify(lastResult);
            sendMessage(prompt);
        }

        async function sendMessage(overrideText = null) {
            const input = document.getElementById('user-input');
            const text = overrideText || input.value.trim();
            if (!text) return;

            if (!overrideText) input.value = '';
            addMessage(text, 'user');
            history.push({role: 'user', content: text});

            const tid = addMessage("Generating Insight... ⏳", 'ai');

            try {
                const res = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ messages: history })
                });
                
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                
                updateMessage(tid, data.response);
                history.push({role: 'assistant', content: data.response});
            } catch (err) {
                updateMessage(tid, "❌ **Error**: " + err.message);
            }
        }

        function addMessage(t, s) {
            const c = document.getElementById('chat-messages');
            const d = document.createElement('div');
            const id = 'm' + Date.now();
            d.id = id;
            d.className = `message ${s}-msg`;
            if (s === 'ai') {
                d.innerHTML = marked.parse(t);
            } else {
                d.textContent = t;
            }
            c.appendChild(d);
            c.scrollTop = c.scrollHeight;
            return id;
        }

        function updateMessage(id, t) {
            const e = document.getElementById(id);
            if (e) e.innerHTML = marked.parse(t);
            document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/infer', methods=['POST'])
def infer():
    data = request.json
    task = data.get('task', 'medical')
    text = data.get('text', '')
    
    time.sleep(0.8) # Simulate GPU latency
    
    # Simple logic to vary response based on text
    confidence = 0.94 if "cough" in text.lower() else 0.85
    label = "Symptom Detected" if len(text) > 5 else "Normal"
    
    return jsonify({
        "engine": "TensorRT-v8.6 (optimized)",
        "precision": "FP16 (Half-Precision)",
        "input_summary": text[:50] + "...",
        "predictions": [{"label": label, "confidence": confidence}],
        "latency_ms": 0.95
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        messages = data.get('messages', [])
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are RA100 TensorX. Always use Markdown (headers, bolding, lists) to make your answers beautiful and easy to read. You explain TensorRT results for healthcare and engineering."}] + messages,
            model="llama-3.3-70b-versatile",
            temperature=0.6,
            max_tokens=1000,
        )
        return jsonify({"response": chat_completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
