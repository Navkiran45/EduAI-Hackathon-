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
from flask_login import login_required, current_user
from app import db
import os
import openai
import json
import logging

# Set up logging for better error reporting
logging.basicConfig(level=logging.ERROR)

quiz_bp = Blueprint("quiz", __name__)
openai_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key=os.environ.get("GROQ_API_KEY")
)

GENERATE_PROMPT = """
Generate a quiz consisting of 20 questions about programming, around the topic of {lang}.
The quiz is intended to serve as an evaluation for finding out the level of knowledge of the student,
and as such it should be challenging but not impossible and include questions of varying difficulty,
from easy to hard. Keep the main focus on overall programming concepts instead of being language-specific,
but still include some language-specific questions as well.

The questions should be in MCQ format, with 4 options each, and the correct answer should be one of the options.
Each question should be unique and not repeated in the quiz.
Each question should be clear and concise, and should not be ambiguous.
Each question should be relevant to the programming language {lang}.
Each question should have some amount of points assigned to it, with the total points of the quiz being 100.

IMPORTANT: Your response must be a valid JSON object with no markdown formatting, code blocks, or escaped characters.
Do not use escaped underscores or newlines in the response. Keep all text in a single line if it contains code.
The response should follow this exact schema:
{{
    "quiz": [
        {{
            "question": "What is x in this code: int x = 5;",
            "options": ["5", "undefined", "null", "error"],
            "correct_option": 0,
            "points": 5
        }},
        ... 19 more questions
    ]
}}

Do not include any explanations, notes, or additional text. Return only the JSON object."""

@quiz_bp.route("/generate-quiz/<lang>")
@login_required
def generate_quiz(lang):
    try:
        # Validate language
        valid_languages = ['python', 'javascript', 'java', 'cpp']
        if lang.lower() not in valid_languages:
            flash("Invalid programming language selected.", "error")
            return redirect(url_for('base.home'))

        # Generate prompt
        prompt = GENERATE_PROMPT.format(lang=lang)

        # Send request to OpenAI
        response = openai_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a quiz generator. Generate quiz questions in valid JSON format without any escaped characters or markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=20000  # Increased to ensure we get complete response
        )

        # Get the response content and parse it
        quiz_content = response.choices[0].message.content.strip()
        
        # Clean up the response if needed
        if quiz_content.startswith('```json'):
            quiz_content = quiz_content[7:-3]  # Remove ```json and ``` markers
        elif quiz_content.startswith('```'):
            quiz_content = quiz_content[3:-3]  # Remove ``` markers
            
        # Remove any leading/trailing whitespace and newlines
        quiz_content = quiz_content.strip()
        
        # Clean up escaped characters and fix common issues
        quiz_content = quiz_content.replace('\\_', '_')  # Fix escaped underscores
        quiz_content = quiz_content.replace('\\n', '\\n')  # Fix escaped newlines
        quiz_content = quiz_content.replace('\\"', '"')  # Fix escaped quotes
        
        # Handle incomplete JSON (in case response was truncated)
        if quiz_content.endswith('...') or 'Continue to next page' in quiz_content:
            logging.error("Received incomplete JSON response")
            flash("Error: Received incomplete quiz data. Please try again.", "error")
            return redirect(url_for('base.level', language=lang))
        
        try:
            quiz_data = json.loads(quiz_content)
        except json.JSONDecodeError as e:
            logging.error(f"JSON Parse Error - Content: {quiz_content[:500]}...")  # Log first 500 chars
            logging.error(f"JSON Parse Error - Details: {str(e)}")
            flash("Error generating quiz: Invalid response format.", "error")
            return redirect(url_for('base.level', language=lang))

        # Validate the quiz data structure
        if not isinstance(quiz_data, dict) or 'quiz' not in quiz_data:
            logging.error(f"Invalid quiz structure: {quiz_data}")
            flash("Error generating quiz. Please try again.", "error")
            return redirect(url_for('base.level', language=lang))

        # Validate quiz questions
        if not quiz_data['quiz'] or not isinstance(quiz_data['quiz'], list):
            logging.error("Quiz data does not contain any questions")
            flash("Error generating quiz: No questions generated.", "error")
            return redirect(url_for('base.level', language=lang))

        # Store quiz in session
        session['quiz_data'] = quiz_data
        return redirect(url_for('quiz.render_quiz', lang=lang))

    except Exception as e:
        logging.error(f"An error occurred while generating the quiz: {str(e)}")
        flash("An error occurred while generating the quiz. Please try again.", "error")
        return redirect(url_for('base.level', language=lang))

@quiz_bp.route("/submit-quiz", methods=['POST'])
@login_required
def submit_quiz():
    try:
        # Get the pre-calculated scores from the form
        score_percentage = float(request.form.get("score_percentage", 0))
        total_points = int(request.form.get("total_points", 0))
        max_points = int(request.form.get("max_points", 0))
        language = request.form.get("language")

        if not language:
            flash("Language not specified", "error")
            return redirect(url_for('base.home'))

        # Determine level based on score
        if score_percentage <= 40:
            level = "beginner"
        elif score_percentage <= 80:
            level = "intermediate"
        else:
            level = "advanced"

        # Clear quiz data from session
        session.pop('quiz_data', None)

        # Show result message
        flash(f"Quiz completed! You scored {total_points} out of {max_points} points ({score_percentage:.1f}%)", "success")
        flash(f"Based on your score, we recommend starting at {level.title()} level", "info")

        # Redirect to the roadmap for the determined level
        return redirect(url_for('chapters.show_roadmap', language=language, level=level))
    
    except (ValueError, TypeError) as e:
        logging.error(f"Invalid quiz submission data: {str(e)}")
        flash("Invalid quiz submission data", "error")
        return redirect(url_for('base.home'))
    except Exception as e:
        logging.error(f"An error occurred while submitting the quiz: {str(e)}")
        flash(f"An error occurred while submitting the quiz: {str(e)}", "error")
        return redirect(url_for('base.home'))

@quiz_bp.route("/<lang>")
@login_required
def render_quiz(lang):
    try:
        # Validate language
        valid_languages = ['python', 'javascript', 'java', 'cpp']
        if lang.lower() not in valid_languages:
            flash("Invalid programming language selected.", "error")
            return redirect(url_for('base.home'))

        # Get quiz data from session
        quiz_data = session.get('quiz_data')
        if not quiz_data:
            return redirect(url_for('quiz.generate_quiz', lang=lang))

        # Add the language to the quiz data for the template
        quiz_data["language"] = lang

        return render_template("quiz.html", quiz=quiz_data)
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        flash(f"An unexpected error occurred: {str(e)}", "error")
        return redirect(url_for('base.level', language=lang))
