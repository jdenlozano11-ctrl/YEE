from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ[Gemini_API_key])

@app.route("/send_to_gemini", methods=["POST"])
def send_to_gemini():
   try: 
    ingredients = request.data.decode("utf-8").strip()

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Create a simple recipe using these ingredients: {ingredients}"

    response = model.generate_content(prompt)
    return jsonify({"recipe": response.text})

@app.route('/')
def home():
    return "✅ Gemini Recipe Server is running successfully!"

if__name__ == "__main__":
app.run(host="0.0.0.0" , port=5000)
