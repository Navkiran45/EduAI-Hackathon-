from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
import os
import openai

quiz_bp = Blueprint('quiz', __name__)
openai_client = openai.OpenAI(
    base_url = "https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

GENERATE_PROMPT = """
Generate a quiz consisting of 20 questions about programming in {lang}.
The quiz is intended to serve as an evaluation for findout out the level of knowledge of the student,
and as such it should be challenging but not impossible and include questions of varying difficulty,
from easy to hard. Keep the main focus on overall programming concepts instead of being language-specific,
but still include some language-specific questions as well.
The questions should be in MCQ format, with 4 options each, and the correct answer should be one of the options.
Each question should be unique and not repeated in the quiz.
Each question should be clear and concise, and should not be ambiguous.
Each question should be relevant to the programming language {lang}.
Each question should have some amout of points assigned to it, with the total points of the quiz being 100.
Your response should be a valid JSON object that follows the following schema:
{{
    "quiz": [
        {{
            "question": "question goes here",
            "options": [
                "option 1",
                "option 2",
                "option 3",
                "option 4"
            ],
            "correct_option": 1,
            "points": 5
        }},
        (... 19 more questions)
    ]
}}
You need to strictly adhere to the above schema,
and the quiz should be generated in a way that it is unique and not repeated.
"""

# Generate quiz
@quiz_bp.get('/generate-quiz')
def generate_quiz():
    language = request.args.get('lang')
    if language is None:
        return {
            "error": "You need to provide a language parameter"
        }, 400

    # Generate prompt
    prompt = GENERATE_PROMPT.format(lang=language)

    # Send request to OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"}
        )

        quiz = response.choices[0].message.content
        return jsonify(quiz), 200

    except Exception as e:
        return {
            "error": f"An error occurred while generating the quiz: {str(e)}"
        }, 500