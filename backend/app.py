from flask import Flask, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration
import fitz  # PyMuPDF
from docx import Document
import io
import os

app = Flask(__name__)

# Load model and tokenizer
model_name = "google/flan-t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = Document(io.BytesIO(file))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Determine file type and extract text
        file_type = file.content_type
        if file_type == 'application/pdf':
            text = extract_text_from_pdf(file.read())
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            text = extract_text_from_docx(file.read())
        else:
            text = file.read().decode('utf-8')  # For plain text files

        # Process the text with the model
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({'summary': summary})

    except Exception as e:
        print(e)
        return jsonify({'error': 'Error occurred while processing the file.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
