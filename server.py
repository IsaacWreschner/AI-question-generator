from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import docx
import PyPDF2

from questions_generator import generate_questions

app = Flask(__name__)

# Define the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded file based on its type
        if filename.endswith('.pdf'):
            text_content = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            text_content = extract_text_from_docx(file_path)
        else:
            text_content = "Unsupported file format."

        text_content = generate_questions(text_content)
        return render_template('result.html', text_content=text_content)

    return redirect(request.url)

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text_content = ''
        for page_num in range(len(reader.pages)):
            text_content += reader.pages[page_num].extract_text()
    return text_content

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text_content = ''
    for paragraph in doc.paragraphs:
        text_content += paragraph.text + '\n'
    return text_content

if __name__ == '__main__':
    app.run(debug=True)
