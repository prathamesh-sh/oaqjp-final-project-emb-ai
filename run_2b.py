import sys, json
from emotion_detection import emotion_detector

if __name__ == "__main__":
    result = emotion_detector("I love this new technology.")
    # If the function returns raw text (string), just print it; otherwise print JSON dump
    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, indent=2))
