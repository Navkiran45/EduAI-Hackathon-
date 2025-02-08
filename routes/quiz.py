from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    session,
)
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
import os
import openai
import json

quiz_bp = Blueprint("quiz", __name__)
openai_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=os.environ.get("GROQ_API_KEY")
)

GENERATE_PROMPT = """
Generate a quiz consisting of 20 questions about programming, around the topic of {lang}.
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
@quiz_bp.get("/generate-quiz/<lang>")
def generate_quiz(lang):
    if lang is None:
        return {"error": "You need to provide a language parameter"}, 400

    # Generate prompt
    prompt = GENERATE_PROMPT.format(lang=lang)

    # Send request to OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        quiz = response.choices[0].message.content
        return quiz, 200

    except Exception as e:
        return {"error": f"An error occurred while generating the quiz: {str(e)}"}, 500


@quiz_bp.post("/submit-quiz")
def submit_quiz():
    # Get the pre-calculated scores from the form
    score_percentage = float(request.form.get("score_percentage", 0))
    total_points = int(request.form.get("total_points", 0))
    max_points = int(request.form.get("max_points", 0))
    language = request.form.get("language")

    # Store results in flash message
    flash(
        f"Quiz completed! You scored {total_points} out of {max_points} points ({score_percentage:.1f}%)",
        "success",
    )

    if score_percentage <= 40:
        return redirect("/beginner")
    elif score_percentage <= 80:
        return redirect("/intermediate")
    else:
        return redirect("/advanced")


@quiz_bp.get("/<lang>")
def render_quiz(lang):
    quiz_data, status = generate_quiz(lang)
    if status != 200:
        return quiz_data, status

    # Parse the JSON string into a Python dict if it's a string
    if isinstance(quiz_data, str):
        quiz_data = json.loads(quiz_data)

    # Store the quiz data in session
    session["quiz_data"] = quiz_data

    # Add the language to the quiz data for the template
    quiz_data["language"] = lang

    return render_template("quiz.html", quiz=quiz_data)
