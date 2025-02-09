from app import db
from datetime import datetime

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), nullable=False)  # e.g., 'python', 'cpp'
    level = db.Column(db.String(20), nullable=False)     # e.g., 'beginner'
    chapter_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    objectives = db.relationship('ChapterObjective', backref='chapter', lazy=True)

    def __repr__(self):
        return f'<Chapter {self.language}-{self.level}-{self.chapter_number}>'

class ChapterObjective(db.Model):
    __tablename__ = 'chapter_objective'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    objective_text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)  # To maintain the order of objectives
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.relationship('ObjectiveProgress', backref='chapter_objective', lazy=True)

    def __repr__(self):
        return f'<ChapterObjective {self.id}>'

class ObjectiveProgress(db.Model):
    __tablename__ = 'objective_progress'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    objective_id = db.Column(db.Integer, db.ForeignKey('chapter_objective.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    last_attempt = db.Column(db.Text)  # Store the last code attempt
    completed_at = db.Column(db.DateTime)
    attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'objective_id', name='unique_student_objective'),
    )

    def __repr__(self):
        return f'<ObjectiveProgress student={self.student_id} objective={self.objective_id}>' 