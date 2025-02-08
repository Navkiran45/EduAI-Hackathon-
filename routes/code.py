from flask import Blueprint, request, jsonify, render_template
import openai
from flask_login import login_required
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure OpenAI client with Groq
openai_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

code_bp = Blueprint('code', __name__)

@code_bp.route('/code')
@login_required
def show_code():
    return render_template('code.html')

@code_bp.route('/api/code', methods=['POST'])
def process_code():
    try:
        data = request.get_json()
        content = data.get('content', '')
        selected_text = data.get('selectedText', '')

        if not content:
            return jsonify({'error': 'No code content provided'}), 400

        # Prepare the message based on whether text is selected
        if selected_text:
            prompt = f"""Please analyze this selected code and provide:
1. An explanation of what this code does
2. Any potential issues or improvements
3. Best practices that could be applied

Selected code:
```
{selected_text}
```

Full context:
```
{content}
```"""
        else:
            prompt = f"""Please analyze this code and provide:
1. A brief overview of what this code does
2. Any potential issues or improvements
3. Best practices that could be applied

Code:
```
{content}
```"""

        # Call Groq API through OpenAI client
        response = openai_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert programming assistant. Analyze code, explain it clearly, and suggest improvements while being concise and practical."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        # Extract the response
        analysis = response.choices[0].message.content

        return jsonify({
            'success': True,
            'analysis': analysis
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
