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
    uploaded_file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(file_path)
    session['file_path'] = file_path
    return render_template('chat.html', file_path=file_path)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    file_path = session.get('file_path')  # Retrieve file path from session
    if request.method == 'POST':
        query_text = request.get_json(force=True)['query']
        # query_text = request.form['query']
        response = process_query(file_path, query_text)
        return jsonify({'file_path': file_path, 'response': response})
    return render_template('chat.html', file_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)