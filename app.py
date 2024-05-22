from flask import Flask, render_template, request, session, jsonify
from query_processor import process_query
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'jay'  # Set a secret key for session management

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('files')
    file_paths = []
    
    for file in uploaded_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        file_paths.append(file_path)
    
    session['file_paths'] = file_paths
    return jsonify({'file_paths': file_paths})

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    file_paths = session.get('file_paths', [])  # Retrieve file paths from session
    if request.method == 'POST':
        query_text = request.get_json(force=True)['query']
        response = process_query(file_paths, query_text)
        return jsonify({'response': response})
    return render_template('chat.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
