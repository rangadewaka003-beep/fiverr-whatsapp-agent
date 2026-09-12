import os
from flask import Flask, request, render_template_string, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ඔබේ Gemini API Key එක
GEMINI_API_KEY = "AQ.Ab8RN6L7VVRu4GmaUcGhOj1fqZwMW1xqhDIQ44Iq4bQkdOth_w"
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

fiverr_seo_system_instruction = """
You are an elite Fiverr SEO & Marketplace Growth Expert. Your core objective is to engineer Fiverr Gigs designed to rank #1 by exploiting the Fiverr search algorithm.
When the user provides a service or niche, you must output a structured blueprint containing:
1. High-CTR & SEO Title (under 80 characters).
2. 5 Precision Search Tags (low-competition, high-intent).
3. Algorithmic Gig Description with scannable bullet points.
4. SEO-Optimized FAQs.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=fiverr_seo_system_instruction
)

# අලංකාර වෙබ් අතුරු මුහුණත (UI) සහිත HTML කෝඩ් එක
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fiverr SEO Agent - AI Generator</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .container { width: 100%; max-width: 650px; background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.4); margin-top: 30px; }
        h1 { text-align: center; color: #38bdf8; font-size: 26px; margin-bottom: 8px; }
        p.subtitle { text-align: center; color: #94a3b8; font-size: 14px; margin-bottom: 25px; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex: 1; padding: 14px; border: 1px solid #334155; background: #0f172a; color: #fff; border-radius: 10px; font-size: 16px; outline: none; transition: border 0.2s; }
        input[type="text"]:focus { border-color: #38bdf8; }
        button { background: #0284c7; color: white; border: none; padding: 14px 24px; border-radius: 10px; font-size: 16px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #0369a1; }
        .loading { text-align: center; color: #38bdf8; display: none; margin-bottom: 15px; font-weight: 500; }
        .result { background: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #334155; white-space: pre-wrap; line-height: 1.7; font-size: 15px; min-height: 200px; color: #e2e8f0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Fiverr SEO Agent</h1>
        <p class="subtitle">Generate high-ranking Fiverr Gig titles, tags, descriptions & FAQs instantly with AI.</p>
        <div class="input-group">
            <input type="text" id="nicheInput" placeholder="Enter your service/niche (e.g., Python Developer, Graphic Design)..." onkeypress="handleKeyPress(event)" />
            <button onclick="generateSEO()">Generate</button>
        </div>
        <div id="loading" class="loading">⏳ Generating your elite Fiverr SEO blueprint... Please wait...</div>
        <div id="resultBox" class="result">Your AI-generated Fiverr SEO blueprint will appear here...</div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                generateSEO();
            }
        }

        async function generateSEO() {
            const niche = document.getElementById('nicheInput').value;
            const resultBox = document.getElementById('resultBox');
            const loading = document.getElementById('loading');

            if (!niche.trim()) {
                alert('Please enter a niche or service!');
                return;
            }

            loading.style.display = 'block';
            resultBox.innerText = '';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ niche: niche })
                });
                const data = await response.json();
                if (data.success) {
                    resultBox.innerText = data.blueprint;
                } else {
                    resultBox.innerText = 'Error: ' + data.error;
                }
            } catch (err) {
                resultBox.innerText = 'An error occurred while connecting to the server.';
            } finally {
                loading.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON data"}), 400
        
    niche = data.get("niche", "")
    if not niche:
        return jsonify({"success": False, "error": "Niche is required"}), 400
    
    try:
        response = model.generate_content(f"Create a complete Fiverr SEO blueprint for: {niche}")
        return jsonify({"success": True, "blueprint": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()
