# pylint: skip-file
"""Flask server for IBM Watson Emotion Detection.

Provides a simple web interface exposing the ``emotion_detector`` function
from the :pymod:`EmotionDetection.emotion_detection` module.
"""

from flask import Flask, request

# Import the packaged function
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """Render a simple index page."""
    return "Emotion Detection Service"

@app.route('/emotionDetector')
def detect_emotion():
    """Endpoint that returns formatted emotion scores and dominant emotion.
    Expects a query parameter ``textToAnalyze``.
    Returns an error message when the input is missing or invalid.
    """
    text = request.args.get('textToAnalyze')
    if not text:
        return "Invalid text! Please try again!"
    result = emotion_detector(text)
    if result.get('dominant_emotion') is None:
        return "Invalid text! Please try again!"
    formatted = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return formatted

if __name__ == '__main__':
    # Run on all interfaces so the UI can reach it
    app.run(host='0.0.0.0', port=5000)
