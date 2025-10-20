from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# =====================================================
# 🔹 Route to handle requests from MIT App Inventor
# =====================================================
@app.route('/send_to_gemini', methods=['POST'])
def send_to_gemini():
    try:
        # Parse incoming JSON from MIT App Inventor
        data = request.get_json()
        base64_image = data.get('image')

        if not base64_image:
            return jsonify({'error': 'No image provided'}), 400

        # Define your prompt for Gemini
        prompt = (
            "You are a helpful chef AI. Look at the image of ingredients and write a short recipe (under 80 words) "
            "and create a recipe with a title, ingredients, and brief instructions."
        )

        # Get your Gemini API key (from environment or replace temporarily)
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            # 👇 You can paste your API key here if Render env variables aren't working:
            # GEMINI_API_KEY = "AIzaSyA4-EXAMPLEKEY-12345"
            return jsonify({'error': 'Gemini API key missing'}), 500

        # Gemini API endpoint
        GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        # Set request headers
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }

        # Prepare the Gemini API request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",  # or "image/png"
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        }

        # Send the request to Gemini
        response = requests.post(GEMINI_URL, headers=headers, json=payload)

        # Handle Gemini API errors
        if response.status_code != 200:
            return jsonify({
                'error': 'Gemini API error',
                'status_code': response.status_code,
                'response': response.text
            }), response.status_code

        # Parse Gemini’s response
        gemini_data = response.json()

        recipe = (
            gemini_data.get('candidates', [{}])[0]
            .get('content', {})
            .get('parts', [{}])[0]
            .get('text', 'No recipe generated.')
        )

        # Return recipe text to MIT App Inventor
        return jsonify({'recipe': recipe})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================================================
# 🔹 Optional home route (to check if Flask is running)
# =====================================================
@app.route('/')
def home():
    return "✅ Gemini Recipe Server is running successfully!"


# =====================================================
# 🔹 Main entry point (for Render or local testing)
# =====================================================
if __name__ == '__main__':
    # Render uses PORT environment variable automatically
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
