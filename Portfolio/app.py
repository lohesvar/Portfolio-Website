import os
import mysql.connector
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Database Configuration
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'lohesvar'),
            database=os.getenv('DB_NAME', 'portfolio_db')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL Database: {err}")
        return None

PROJECTS = [
    {
        'title': 'Gallery Page',
        'description': 'An interactive and visually stunning image gallery showcasing curated photography with smooth filters.',
        'thumbnail': '/projects/gallery-page/thumbnail.png',
        'live_link': '/projects/gallery-page/index.html'
    },
    {
        'title': 'To-do Project',
        'description': 'A minimal and responsive task tracking application to organize daily checklists and increase productivity.',
        'thumbnail': None,
        'live_link': '/projects/to-do-project/index.html'
    },
    {
        'title': 'To-do Project v2',
        'description': 'An upgraded and feature-rich version of the task manager with category filtering, searching, and refined animations.',
        'thumbnail': None,
        'live_link': '/projects/to-do-project-v2/index.html'
    },
    {
        'title': 'NoteFlow',
        'description': 'A collaborative note-taking application powered by Flask and SQLite database storage.',
        'thumbnail': None,
        'live_link': 'http://localhost:8000'
    },
    {
        'title': 'YouTube Like',
        'description': 'A video-sharing and custom display platform featuring upload simulations and interactive layouts.',
        'thumbnail': None,
        'live_link': 'http://localhost:5002'
    }
]

def get_latest_resume():
    assets_dir = 'D:/Projects/Assets'
    if not os.path.exists(assets_dir):
        return None
    files = [os.path.join(assets_dir, f) for f in os.listdir(assets_dir) if os.path.isfile(os.path.join(assets_dir, f))]
    resume_files = [f for f in files if any(kw in os.path.basename(f).lower() for kw in ['resume', 'cv'])]
    if not resume_files:
        resume_files = files
    if not resume_files:
        return None
    return max(resume_files, key=os.path.getmtime)

@app.route('/')
def index():
    """Render the main portfolio page."""
    return render_template('index.html', projects=PROJECTS)

@app.route('/resume')
def serve_resume():
    """Find and serve the most recently updated resume file."""
    resume_path = get_latest_resume()
    if resume_path and os.path.exists(resume_path):
        filename = os.path.basename(resume_path)
        ext = os.path.splitext(filename)[1].lower()
        as_attachment = ext not in ['.pdf', '.txt']
        return send_file(resume_path, as_attachment=as_attachment, download_name=filename)
    return "Resume not found", 404

@app.route('/projects/<path:filename>')
def serve_project_static(filename):
    """Serve static project files from the Assets/Projects folder."""
    return send_from_directory('D:/Projects/Assets/Projects', filename)


@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions via AJAX."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not all([name, email, subject, message]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection failed. Please try again later.'}), 500

        try:
            cursor = conn.cursor()
            # Insert the message into the database
            query = "INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)"
            values = (name, email, subject, message)
            cursor.execute(query, values)
            conn.commit()
            return jsonify({'success': True, 'message': 'Message sent successfully! I will get back to you soon.'})
        except mysql.connector.Error as err:
            print(f"Error executing database query: {err}")
            return jsonify({'success': False, 'message': 'Failed to save message due to database error.'}), 500
        finally:
            if conn:
                cursor.close()
                conn.close()

if __name__ == '__main__':
    # Run the application in debug mode for development
    app.run(debug=True, port=5000)
