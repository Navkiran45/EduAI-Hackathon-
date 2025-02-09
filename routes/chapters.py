from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.chapter import Chapter, ChapterObjective, ObjectiveProgress
from app import db

chapters_bp = Blueprint('chapters', __name__)

@chapters_bp.route('/roadmap/<string:language>/<string:level>')
@login_required
def show_roadmap(language, level):
    chapters = Chapter.query.filter_by(
        language=language,
        level=level
    ).order_by(Chapter.chapter_number).all()
    
    return render_template('roadmap.html', 
                         chapters=chapters, 
                         language=language, 
                         level=level)

@chapters_bp.route('/chapter/<int:chapter_id>')
@login_required
def chapter_detail(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    
    # Get objectives with their progress
    objectives = ChapterObjective.query.filter_by(
        chapter_id=chapter_id
    ).order_by(ChapterObjective.order).all()
    
    # Add progress state to each objective
    for objective in objectives:
        # Use progress_state instead of progress to avoid conflict with relationship
        if current_user.is_authenticated:
            progress_record = ObjectiveProgress.query.filter_by(
                student_id=current_user.id,
                objective_id=objective.id
            ).first()
            setattr(objective, 'progress_state', progress_record)
        else:
            setattr(objective, 'progress_state', None)
    
    return render_template('chapter_detail.html', 
                         chapter=chapter, 
                         objectives=objectives)

# Admin routes for managing chapters and objectives
@chapters_bp.route('/admin/chapter/add', methods=['GET', 'POST'])
@login_required
def add_chapter():
    if request.method == 'POST':
        new_chapter = Chapter(
            language=request.form['language'],
            level=request.form['level'],
            chapter_number=request.form['chapter_number'],
            title=request.form['title'],
            description=request.form['description']
        )
        
        try:
            db.session.add(new_chapter)
            db.session.commit()
            flash('Chapter added successfully!', 'success')
            return redirect(url_for('chapters.show_roadmap', 
                                  language=new_chapter.language, 
                                  level=new_chapter.level))
        except Exception as e:
            db.session.rollback()
            flash('Error adding chapter', 'error')
            
    return render_template('admin/add_chapter.html')

@chapters_bp.route('/admin/objective/add/<int:chapter_id>', methods=['POST'])
@login_required
def add_objective(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    
    new_objective = ChapterObjective(
        chapter_id=chapter_id,
        objective_text=request.form['objective_text'],
        order=request.form['order']
    )
    
    try:
        db.session.add(new_objective)
        db.session.commit()
        flash('Objective added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding objective', 'error')
        
    return redirect(url_for('chapters.chapter_detail', chapter_id=chapter_id)) 