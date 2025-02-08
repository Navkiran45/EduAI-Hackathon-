from flask import Blueprint, request, jsonify
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")  # Ensure you set GROQ_API_KEY in your environment
)

# Create a Blueprint for the chatbot
chatbot_bp = Blueprint('chatbot', __name__)

# Route to evaluate code
@chatbot_bp.route('/evaluate', methods=['POST'])
def evaluate_code():
    user_code = request.json.get('code')  # Get the code from the frontend
    objective = request.json.get('objective')  # Get the objective (if any)

    # Custom prompt to evaluate the code
    prompt = f"""
    You are an AI tutor. A user has submitted the following code for the objective: {objective}.
    Code:
    {user_code}

    Your task is to:
    1. Check if the code is correct.
    2. If the code is incorrect, provide suggestions to fix it without giving the complete solution.
    3. If the code is correct, acknowledge it and provide feedback.

    Respond in a concise and helpful manner.
    """

    # Call Groq API
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # Use the appropriate Groq model
        messages=[
            {"role": "system", "content": "You are a helpful AI tutor."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the AI's response
    feedback = response.choices[0].message.content

    return jsonify({"feedback": feedback})