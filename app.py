from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ[Gemini_key])

@app.route("/send_to_gemini", methods=["POST"])
def send_to_gemini():
    ingredients = request.data.decode("utf-8")

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Create a simple recipe using these ingredients: {ingredients}"

    response = model.generate_content(prompt)
    return jsonify({"recipe": response.text})
    
# =====================================================
# 🔹 Optional home route (to check if Flask is running)
# =====================================================
@app.route('/')
def home():
    return "✅ Gemini Recipe Server is running successfully!"
