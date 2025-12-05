# =========================================================
# ΜΕΡΟΣ Β: FLASK WEB APP ΓΙΑ ΤΗΝ ΕΡΓΑΣΙΑ
# Αποθήκευσέ το ως app.py
# =========================================================

import os
import cv2
from flask import Flask, request, render_template_string, send_from_directory
from fer import FER
from openai import OpenAI

# =========================================================
# ΡΥΘΜΙΣΕΙΣ OPENAI (ΠΑΛΙΟ ΙΔΙΟ CONCEPT)
# =========================================================

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")  # ή βάλε σταθερά αν θες
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

LLM_MODEL = "gpt-4.1-mini"

# =========================================================
# ΔΗΜΙΟΥΡΓΙΑ FLASK APP
# =========================================================

app = Flask(__name__)

# Φάκελοι για uploads / annotated
UPLOAD_FOLDER = "static/uploads"
ANNOTATED_FOLDER = "static/annotated"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ANNOTATED_FOLDER, exist_ok=True)

# Δημιουργία detector
emotion_detector = FER(mtcnn=True)

# =========================================================
# ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ (ΙΔΙΕΣ ΛΟΓΙΚΑ ΜΕ ΤΟ NOTEBOOK)
# =========================================================

def allowed_emotions():
    return ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]


def detect_emotions_in_image(image_path: str):
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Η εικόνα δεν βρέθηκε: {image_path}")

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    raw = emotion_detector.detect_emotions(img_rgb)

    results = []
    for det in raw:
        box = det.get("box", [0, 0, 0, 0])
        emo = det.get("emotions", {})
        if emo:
            label = max(emo, key=emo.get)
            conf = float(emo[label])
        else:
            label = "unknown"
            conf = 0.0

        results.append({
            "box": tuple(box),
            "emotion": label,
            "confidence": conf,
            "emotions": {k: float(v) for k, v in emo.items()}
        })
    return results


def aggregate_emotions(detections):
    base = {e: 0.0 for e in allowed_emotions()}
    if not detections:
        return base

    count = 0
    for det in detections:
        emo = det["emotions"]
        if emo:
            count += 1
            for e in allowed_emotions():
                base[e] += float(emo.get(e, 0.0))

    if count == 0:
        return base

    for e in base:
        base[e] /= count

    return base


def annotate_image(image_path: str, detections, save_path: str):
    """
    Φορτώνει την εικόνα, ζωγραφίζει τα κουτιά και την αποθηκεύει στο save_path.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Αποτυχία φόρτωσης εικόνας.")

    for det in detections:
        x, y, w, h = det["box"]
        emotion = det["emotion"]
        conf = det["confidence"]

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label = f"{emotion} ({conf:.2f})"
        cv2.putText(
            img,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    cv2.imwrite(save_path, img)


emotion_to_playlist = {
    "happy": "uplifting_pop_playlist",
    "sad": "chill_ambient_playlist",
    "angry": "rock_energy_playlist",
    "fear": "calm_piano_playlist",
    "disgust": "neutral_focus_playlist",
    "surprise": "random_discovery_playlist",
    "neutral": "lofi_study_playlist",
}

def map_emotion_to_playlist(dominant_emotion: str) -> str:
    return emotion_to_playlist.get(dominant_emotion, "lofi_study_playlist")


def llm_description(summary: dict):
    if client is None:
        return "LLM δεν κλήθηκε (δεν έχει οριστεί OPENAI_API_KEY)."

    text = ", ".join([f"{e}: {v:.2f}" for e, v in summary.items()])

    prompt = (
        "You are an assistant that describes emotional state based on probabilities.\n"
        f"Emotion probabilities: {text}\n"
        "Write a short, clear emotional interpretation in English."
    )

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You explain emotional states accurately."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM error: {e}"


# =========================================================
# ΑΠΛΟ HTML TEMPLATE ΣΕ CHAT-STYLE
# =========================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Emotion-Based Music Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: auto; padding: 20px; }
        .chat-box { border: 1px solid #ccc; border-radius: 8px; padding: 15px; margin-top: 20px; }
        .message-user { text-align: right; color: #333; margin: 10px 0; }
        .message-bot { text-align: left; color: #006; margin: 10px 0; }
        .image-row { display: flex; gap: 20px; margin-top: 20px; }
        .image-row img { max-width: 100%; max-height: 300px; border-radius: 8px; border: 1px solid #ccc; }
        .result-block { margin-top: 20px; padding: 10px; border-radius: 8px; background-color: #f8f8f8; }
    </style>
</head>
<body>
    <h1>Emotion-Based Music Assistant</h1>
    <p>Ανέβασε μία εικόνα προσώπου. Το σύστημα θα ανιχνεύσει το συναίσθημα, θα προτείνει playlist και θα δώσει περιγραφή μέσω LLM.</p>

    <form action="/analyze" method="post" enctype="multipart/form-data">
        <label>Εικόνα:</label>
        <input type="file" name="image" accept="image/*" required>
        <button type="submit">Ανάλυση</button>
    </form>

    {% if user_message %}
    <div class="chat-box">
        <div class="message-user">
            <strong>Εσύ:</strong> {{ user_message }}
        </div>
        <div class="message-bot">
            <strong>Σύστημα (Dominant emotion):</strong> {{ dominant_emotion }}
        </div>
        <div class="message-bot">
            <strong>Προτεινόμενη playlist:</strong> {{ playlist }}
        </div>
        <div class="message-bot">
            <strong>LLM περιγραφή:</strong> {{ llm_text }}
        </div>

        <div class="result-block">
            <h3>Μέσες πιθανότητες συναισθημάτων:</h3>
            <ul>
                {% for emo, prob in summary.items() %}
                    <li>{{ emo }}: {{ "%.2f"|format(prob) }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="image-row">
            <div>
                <h3>Αρχική εικόνα</h3>
                <img src="{{ original_url }}" alt="Original Image">
            </div>
            <div>
                <h3>Annotated εικόνα</h3>
                <img src="{{ annotated_url }}" alt="Annotated Image">
            </div>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""


# =========================================================
# ROUTES
# =========================================================

@app.route("/", methods=["GET"])
def index():
    """
    Αρχική σελίδα με φόρμα upload.
    """
    return render_template_string(
        HTML_TEMPLATE,
        user_message=None,
        dominant_emotion=None,
        playlist=None,
        llm_text=None,
        summary={},
        original_url="",
        annotated_url=""
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Route που δέχεται την εικόνα, τρέχει FER + LLM και επιστρέφει αποτελέσματα.
    """
    file = request.files.get("image")
    if not file:
        return "Δεν δόθηκε εικόνα.", 400

    # Αποθήκευση αρχικής εικόνας
    filename = file.filename
    original_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(original_path)

    # Ανάλυση συναισθημάτων
    detections = detect_emotions_in_image(original_path)
    summary = aggregate_emotions(detections)

    if detections:
        dominant = max(summary, key=summary.get)
    else:
        dominant = "none"

    playlist = map_emotion_to_playlist(dominant)
    llm_text = llm_description(summary)

    # Δημιουργία annotated εικόνας
    annotated_filename = f"{os.path.splitext(filename)[0]}_annotated.png"
    annotated_path = os.path.join(ANNOTATED_FOLDER, annotated_filename)

    if detections:
        annotate_image(original_path, detections, annotated_path)
    else:
        # αν δεν υπάρχουν πρόσωπα, αντιγράφουμε απλά την αρχική
        cv2.imwrite(annotated_path, cv2.imread(original_path))

    # URLs για εμφάνιση εικόνων
    original_url = f"/static/uploads/{filename}"
    annotated_url = f"/static/annotated/{annotated_filename}"

    # Μήνυμα χρήστη (σαν chat)
    user_message = f"Ανέβασα την εικόνα {filename}."

    return render_template_string(
        HTML_TEMPLATE,
        user_message=user_message,
        dominant_emotion=dominant,
        playlist=playlist,
        llm_text=llm_text,
        summary=summary,
        original_url=original_url,
        annotated_url=annotated_url
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    # Σημείωση: Για production deployment σε Render/PythonAnywhere,
    # συνήθως ΔΕΝ τρέχουμε debug=True
    app.run(host="0.0.0.0", port=8000, debug=True)
