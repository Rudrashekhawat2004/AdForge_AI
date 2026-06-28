from flask import Flask, render_template, request
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def index():
    ad_copy = ""
    if request.method == 'POST':
        product = request.form['product']
        # Groq se AI copy generate karwana
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Write a catchy ad copy for: {product}"}],
            model="llama-3.1-8b-instant"
        )
        ad_copy = chat_completion.choices[0].message.content
    return render_template('index.html', ad_copy=ad_copy)
if __name__=='__main__':
 app.run(debug=True)