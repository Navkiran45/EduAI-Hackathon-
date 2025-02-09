from flask import Blueprint, request, jsonify, render_template, flash
import os
import openai
from dotenv import load_dotenv
from flask_login import login_required

# Load environment variables
load_dotenv()

# Initialize Groq client
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")  # Ensure you set GROQ_API_KEY in your environment
)

# Create a Blueprint for the chatbot
chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat')
@login_required
def render_chat():
    return render_template('chatbot.html')

@chatbot_bp.route('/evaluate', methods=['POST'])
@login_required
def evaluate_code():
    try:
        data = request.json
        user_code = data.get('code', '')
        message = data.get('message', '')
        language = data.get('language', '')
        objective = data.get('objective', '')

        if objective == 'analyze':
            prompt = f"""
            Analyze this {language} code and provide:
            1. A brief explanation of what the code does
            2. Any potential issues or improvements
            3. Best practices that could be applied

            Code:
            ```{language}
            {user_code}
            ```
            """
        elif objective == 'explain':
            prompt = f"""
            Explain this {language} code in detail:
            1. Break down each part of the code
            2. Explain the logic and flow
            3. Highlight any important concepts used

            Code:
            ```{language}
            {user_code}
            ```
            """
        else:
            # Handle general chat messages
            prompt = f"""
            User Message: {message}

            Context:
            - Programming Language: {language if language else 'Not specified'}
            - Code (if provided):
            ```
            {user_code if user_code else 'No code provided'}
            ```

            Provide a helpful response addressing the user's question or request.
            If code is provided, reference it in your response when relevant.
            """

        # Call Groq API
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a helpful AI programming tutor. Provide clear, concise, and accurate responses."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Extract the AI's response
        feedback = response.choices[0].message.content

        return jsonify({
            "success": True,
            "response": feedback,
            "feedback": feedback  # For backward compatibility
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500