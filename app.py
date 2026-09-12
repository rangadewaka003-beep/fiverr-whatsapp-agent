import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ඔබේ API Key එක කෙළින්ම කේතය තුළට ඇතුළත් කර ඇත
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

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    data = request.json
    try:
        incoming_msg = data.get("Body", "")
        if not incoming_msg:
            return jsonify({"reply": "कृपया නිෂේ එකක් එවන්න!"}), 400

        response = model.generate_content(incoming_msg)
        return jsonify({"reply": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
