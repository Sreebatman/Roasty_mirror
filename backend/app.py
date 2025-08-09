from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from deepface import DeepFace
import cv2
import numpy as np
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Environment setup
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enhanced roast messages
ROASTS = {
    'age': [
        "Are you a museum piece? Because you look ancient!",
        "You're so old, your birth certificate is in Roman numerals!",
        "Is that your face or did you walk into a wall?",
        "You look like you've been through a time machine set to 'wrinkle'"
    ],
    'emotion': {
        'angry': ["Who hurt you? Oh wait, it was genetics!", "Did you wake up like this or is it permanent?"],
        'sad': ["Cheer up! At least you're not as ugly as you think.", "Smile! It makes people wonder what you're up to."],
        'neutral': ["Did your face freeze like that or is it a choice?", "More expression please! Oh wait, you can't."],
        'fear': ["I'd be scared too if I looked like that!", "Saw a ghost? Oh wait, that's just your reflection!"],
        'happy': ["Your smile looks like a crime scene!", "That grin could scare crows from a cornfield."],
        'surprise': ["Did you see a ghost? Oh wait, that's just your reflection!", "Pikachu face? More like Pikashock face!"],
        'disgust': ["You look like you smelled your own cooking!", "Did something die? Oh it's just your expression."]
    },
    'gender': {
        'Man': ["Did you lose a fight with a lawnmower?", "That beard looks like a bird's nest!"],
        'Woman': ["That face could stop a clock!", "Did you do your makeup in the dark?"]
    },
    'race': {
        'white': ["You're so pale, I can see your insecurities!", "Need some sun? Or maybe just less screen time."],
        'black': ["Looking like a shadow with bad intentions!", "Shine so bright I need shades!"],
        'asian': ["Your face is wider than my future!", "Eyes so small, I thought you were squinting."],
        'indian': ["You shine brighter than my future!", "That skin tone deserves better facial expressions."],
        'middle eastern': ["Your beard looks like a bird's nest!", "Looking like a desert mirage."],
        'latino hispanic': ["Hotter than Satan's oven!", "Passion in your eyes... or maybe just indigestion?"]
    }
}

def generate_roast(analysis):
    roasts = []
    
    # Age roasts
    if analysis['age'] > 40:
        roasts.append(random.choice(ROASTS['age']))
    
    # Emotion roasts
    emotion = analysis['dominant_emotion']
    roasts.append(random.choice(ROASTS['emotion'][emotion]))
    
    # Gender roasts
    gender = analysis['dominant_gender']
    roasts.append(random.choice(ROASTS['gender'][gender]))
    
    # Race roasts
    race = analysis['dominant_race']
    roasts.append(random.choice(ROASTS['race'].get(race, ["Your face broke my algorithm!"])))
    
    return " ".join(roasts)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        img = cv2.imread(filepath)
        if img is None:
            return jsonify({'error': 'Invalid image file'}), 400
            
        results = DeepFace.analyze(img, actions=['emotion', 'age', 'gender', 'race'])
        primary = results[0]
        
        response = {
            'emotion': primary['dominant_emotion'],
            'age': primary['age'],
            'gender': primary['dominant_gender'],
            'race': primary['dominant_race'],
            'roast': generate_roast(primary)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)