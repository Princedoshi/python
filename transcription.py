from flask import Flask, request, jsonify
from pydub import AudioSegment
import io
from pocketsphinx import AudioFile
import requests
from transformers import pipeline
import cv2

app = Flask(__name__)
summarizer = pipeline('summarization')

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large"
headers = {"Authorization": "Bearer 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"}

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        audio_data = request.files['audio'].read()
        audio_text = recognize_audio(audio_data)
        text=summarize_text(audio_text)
        
        return jsonify({'text': text,'ogtext':audio_text,"keywords":query({"inputs": text,})})
    except Exception as e:
        return jsonify({'error': str(e)})
    
def recognize_audio(audio_data):
    response = requests.post(API_URL, headers=headers, data=audio_data)
    # print(response.json()['text'])
    return (response.json()['text'])

# app = Flask(_name_)

API2_URL = "https://api-inference.huggingface.co/models/transformer3/H1-keywordextractor"
headers2 = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API2_URL, headers=headers2, json=payload)
	return [item.strip() for item in response.json()[0].get('summary_text', '').split(',')]

# @app.route('/summarize', methods=['POST'])
def summarize_text(article):
    try:
        # if not request.is_json:
        #     return jsonify({'error': 'Invalid request. Please provide a JSON payload.'})
        # data = request.get_json()
        # article = data['text']
        summary = summarizer(article, max_length=300,
                             min_length=100, do_sample=False)
        return summary[0]['summary_text']

    except Exception as e:
        print("hi")
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
