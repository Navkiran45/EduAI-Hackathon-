import sys
import os

# Add your project directory to the sys.path
project_home = '/home/your_pythonanywhere_username/your_project_name'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-production-secret-key'  # Change this to a secure value
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_home, 'instance', 'eduai.db')

# Import your Flask app
from app import app as application 