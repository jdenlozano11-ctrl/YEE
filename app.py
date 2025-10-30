from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ[GEMINI_API_KEY])

@app.route("/send_to_gemini", methods=["POST"])
def send_to_gemini():
   try: 
    ingredients = request.data.decode("utf-8").strip()

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Create a simple recipe using these ingredients: {ingredients}"

    response = model.generate_content(prompt)
    return jsonify({"recipe": response.text})
   except Exception as e:
      return jsonify({"error": str(e)}), 500
@app.route('/')
def home():
    return "✅ Gemini Recipe Server is running successfully!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    ingredients = data.get("ingredients", "")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Give me a recipe using these ingredients: {ingredients}")
    return jsonify({"recipe": response.text})

if__name__ == "__main__":
app.run(debug=True)
