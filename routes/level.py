from flask import Blueprint, render_template
level_bp = Blueprint('level', __name__)
@level_bp.route('/level')
def level():
    return render_template('level.html')
