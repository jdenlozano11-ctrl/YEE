from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

@app.route('/send_to_gemini', methods=['POST'])
def send_to_gemini():
    base64_image = request.data.decode('utf-8')

    headers = {
        "Authorization": f"Bearer {os.environ.get('GEMINI_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ]
    }

   response = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
    headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
        json=payload
    )

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
