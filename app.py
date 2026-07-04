import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')

# API Key load karo
api_key = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        description = data.get('description', '')
        platform = data.get('platform', 'Instagram')
        tone = data.get('tone', 'Casual')

        user_prompt = f"Platform: {platform}\nTone: {tone}\nDescription: {description}"

        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant", # Tumhari key ke liye best
            messages=[
                {"role": "system", "content": "You are a helpful social media assistant."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        ai_response = completion.choices[0].message.content
        return jsonify({"success": True, "result": ai_response})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)