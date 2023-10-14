from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import librosa

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CORS(app)


def process_audio(file_path):
    y, sr = librosa.load(file_path)
    tempo = librosa.beat.tempo(y=y, sr=sr)
    return tempo[0]

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        tempo = process_audio(file_path)
        os.remove(file_path)
        print(tempo)
        return jsonify({'tempo': tempo})
    return "No file uploaded"


if __name__ == '__main__':
    app.run(debug=True)