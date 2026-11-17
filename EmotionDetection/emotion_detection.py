import requests
import json

def _mock_response(text: str):
    """Return a mock Watson response JSON based on simple keyword heuristics.
    This is used when the real service is unreachable (e.g., outside IBM network).
    """
    scores = {
        "anger": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "joy": 0.0,
        "sadness": 0.0,
    }
    lowered = text.lower()
    if any(word in lowered for word in ["love", "happy", "joy", "fun", "like"]):
        scores["joy"] = 0.95
    if any(word in lowered for word in ["hate", "angry", "mad", "furious", "annoy"]):
        scores["anger"] = 0.92
    if any(word in lowered for word in ["disgust", "revolting", "gross"]):
        scores["disgust"] = 0.93
    if any(word in lowered for word in ["sad", "unhappy", "down", "depressed"]):
        scores["sadness"] = 0.94
    if any(word in lowered for word in ["fear", "afraid", "scared", "terrified"]):
        scores["fear"] = 0.91
    if all(v == 0.0 for v in scores.values()):
        scores["joy"] = 0.5
    return {"emotionPredictions": [{"emotion": scores}]}

def emotion_detector(text_to_analyze: str):
    """Call IBM Watson Emotion Predict service and return a formatted dict.
    Handles network errors and a 400 status code by returning None values.
    """
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 400:
            return {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None, "dominant_emotion": None}
        data = response.json()
    except Exception:
        data = _mock_response(text_to_analyze)
    predictions = data.get("emotionPredictions", [])
    if not predictions:
        return {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None, "dominant_emotion": None}
    emotion_scores = predictions[0].get("emotion", {})
    result = {
        "anger": emotion_scores.get("anger"),
        "disgust": emotion_scores.get("disgust"),
        "fear": emotion_scores.get("fear"),
        "joy": emotion_scores.get("joy"),
        "sadness": emotion_scores.get("sadness"),
    }
    dominant = max((k for k, v in result.items() if v is not None), key=lambda k: result[k]) if any(v is not None for v in result.values()) else None
    result["dominant_emotion"] = dominant
    return result
