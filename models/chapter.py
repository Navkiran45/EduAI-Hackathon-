from app import db

class Chapter(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    objective_text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)  # To maintain the order of objectives

    def __repr__(self):
        return f'<ChapterObjective {self.id}>' 