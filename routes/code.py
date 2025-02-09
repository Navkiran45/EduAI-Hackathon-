from flask import Blueprint, request, jsonify, render_template
import openai
from flask_login import login_required, current_user
from dotenv import load_dotenv
from models.chapter import ChapterObjective, ObjectiveProgress
from app import db
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Configure OpenAI client with Groq
openai_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

code_bp = Blueprint('code', __name__)

@code_bp.route('/')
@login_required
def show_code_editor():
    return render_template('code.html', 
                         objective=None,
                         progress=None,
                         language='python')  # Default to Python

@code_bp.route('/<int:objective_id>')
@login_required
def show_code(objective_id):
    objective = ChapterObjective.query.get_or_404(objective_id)
    # Get or create progress record
    progress = ObjectiveProgress.query.filter_by(
        student_id=current_user.id,
        objective_id=objective_id
    ).first()
    
    if not progress:
        progress = ObjectiveProgress(
            student_id=current_user.id,
            objective_id=objective_id
        )
        db.session.add(progress)
        db.session.commit()

    return render_template('code.html', 
                         objective=objective,
                         progress=progress,
                         language=objective.chapter.language)

@code_bp.route('/evaluate', methods=['POST'])
@login_required
def evaluate_code():
    try:
        data = request.get_json()
        code = data.get('code')
        objective_id = data.get('objective_id')
        evaluation_type = data.get('objective')  # 'analyze' or 'explain'

        if not code:
            return jsonify({'error': 'Missing code'}), 400

        objective = None
        language = 'python'  # default
        if objective_id:
            objective = ChapterObjective.query.get_or_404(objective_id)
            language = objective.chapter.language
            progress = ObjectiveProgress.query.filter_by(
                student_id=current_user.id,
                objective_id=objective_id
            ).first()

            if not progress:
                progress = ObjectiveProgress(
                    student_id=current_user.id,
                    objective_id=objective_id
                )
                db.session.add(progress)
                db.session.commit()

            # Update attempt count
            progress.attempts += 1
            progress.last_attempt = code
            db.session.commit()

        # Custom prompt for code evaluation that avoids giving direct solutions
        if evaluation_type == 'analyze':
            prompt = f"""
            You are a programming tutor who helps students learn by guiding them to find solutions themselves.
            Never provide direct code solutions. Instead, give hints, ask questions, and point out concepts they should research.

            You are specifically evaluating {language.upper()} code. If the code appears to be in a different language,
            point this out and explain that they need to use {language.upper()} for this objective.

            Analyze this code{f' for the objective: "{objective.objective_text}"' if objective else ''}:
            ```{language}
            {code}
            ```

            Provide feedback that:
            1. First, verify if the code is valid {language.upper()} code. If not, explain why and what language it appears to be
            2. Points out what concepts they understand well
            3. Identifies areas for improvement without giving direct solutions
            4. Suggests what concepts or documentation they should look into
            5. If there are issues, ask guiding questions to help them find the solution themselves
            {f'6. End with either [PASS] or [FAIL] based on whether the code satisfies the core objective' if objective else ''}

            Remember: DO NOT provide code solutions. Guide them to find answers themselves.
            """
        else:  # explain
            prompt = f"""
            You are a programming tutor who helps students learn by guiding them to find solutions themselves.
            Never provide direct code solutions. Instead, explain concepts and guide understanding.

            You are specifically explaining {language.upper()} code. If the code appears to be in a different language,
            point this out and explain that they need to use {language.upper()} for this objective.

            Explain the concepts used in this code:
            ```{language}
            {code}
            ```

            Provide an explanation that:
            1. First, verify if the code is valid {language.upper()} code. If not, explain why and what language it appears to be
            2. Describes the high-level concepts and patterns used
            3. Explains why certain approaches might or might not be optimal
            4. Suggests related concepts they might want to learn about
            5. If there are potential improvements, describe them conceptually without providing code

            Remember: Focus on explaining concepts, not providing code solutions.
            """

        # Call Groq API
        response = openai_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": f"You are a helpful {language.upper()} programming tutor who guides students to find solutions themselves, never giving direct answers. Use the Socratic method to help students learn."},
                {"role": "user", "content": prompt}
            ]
        )

        feedback = response.choices[0].message.content

        # Check if objective is completed
        if objective and "[PASS]" in feedback:
            progress.completed = True
            progress.completed_at = datetime.utcnow()
            db.session.commit()

        return jsonify({
            "success": True,
            "feedback": feedback,
            "completed": progress.completed if objective else None
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@code_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.get_json()
        message = data.get('message')
        objective_id = data.get('objective_id')
        code_context = data.get('context')

        if not all([message, code_context]):
            return jsonify({'error': 'Missing required data'}), 400

        objective = None
        language = 'python'  # default
        if objective_id:
            objective = ChapterObjective.query.get_or_404(objective_id)
            language = objective.chapter.language

        # Create a context-aware prompt that avoids giving direct solutions
        prompt = f"""
        You are a programming tutor who helps students learn by guiding them to find solutions themselves.
        Never provide direct code solutions. Instead, give hints, ask questions, and point out concepts they should research.

        You are specifically helping with {language.upper()} programming. If the code appears to be in a different language,
        point this out and explain that they need to use {language.upper()} for this objective.

        Context:
        {f'- Learning Objective: {objective.objective_text}' if objective else ''}
        - Current Code:
        ```{language}
        {code_context}
        ```
        
        Student Question: {message}

        Provide a response that:
        1. First, verify if the code is valid {language.upper()} code. If not, explain why and what language it appears to be
        2. Helps them understand the concepts involved
        3. Guides them to find the answer themselves through questions and hints
        4. Points them to relevant documentation or learning resources
        5. If they're stuck, break down the problem into smaller steps they can work through
        6. Uses analogies or examples to explain concepts (but never provide direct code solutions)

        Remember: Your goal is to help them learn, not to give them the answer.
        """

        response = openai_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": f"You are an expert {language.upper()} programming tutor who uses the Socratic method. Never give direct code solutions."},
                {"role": "user", "content": prompt}
            ]
        )

        return jsonify({
            "success": True,
            "response": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500