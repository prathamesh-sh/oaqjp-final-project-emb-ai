import json
from emotion_detection import emotion_detector

if __name__ == "__main__":
    result = emotion_detector("I love this new technology.")
    print(json.dumps(result, indent=2) if isinstance(result, dict) else result)
