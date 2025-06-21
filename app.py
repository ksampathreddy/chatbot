from flask import Flask, request, jsonify, render_template
import spacy
from spacy.matcher import PhraseMatcher
from collections import defaultdict
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load English language model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Enhanced knowledge base with synonyms and patterns
knowledge_base = {
    "college_name": {
        "response": "The college name is DRK Institute of Science and Technology.",
        "patterns": ["college name", "institute name", "name of college", "drk full form", "what is drkist"]
    },
    "contact": {
        "response": "Contact Details:\nMobile: +91-90007 11899 or +91-87907 11899\nEmail: principal@drkist.edu.in",
        "patterns": ["contact", "phone", "email", "how to reach", "contact details", "phone number"]
    },
    "courses": {
        "response": "We offer these courses:\n- CSE\n- CSE (AI & ML)\n- CSE (Data Science)\n- CSE (Cyber Security)\n- Electronics and Communication Engineering\n- Electrical and Electronics Engineering\n- Mechanical Engineering\n- Civil Engineering",
        "patterns": ["courses", "programs", "degrees", "branches", "what courses", "available courses", "study programs"]
    },
    "admission": {
        "response": "Admission Process:\n1. Apply through Telangana EAPCET\n2. For Management Quota, contact Admission Department",
        "patterns": ["admission", "how to apply", "admission process", "join college", "get admission"]
    },
    "timings": {
        "response": "College Timings:\n9:20 AM to 4:20 PM, Monday to Saturday",
        "patterns": ["timings", "college hours", "working hours", "when is college open", "college schedule"]
    },
    "address": {
        "response": "College Address:\nNear Pragathi Nagar, Bowrampet (V), Hyderabad - 500043, Telangana, India",
        "patterns": ["address", "location", "where is college", "college location", "how to reach college"]
    },
    "placements": {
        "response": "Placement Information:\nWe have a dedicated Placement Cell. Top companies visit our campus for recruitment.",
        "patterns": ["placements", "jobs", "recruitment", "companies", "placement record"]
    }
}

# Create inverted index for better matching
inverted_index = defaultdict(list)
for intent, data in knowledge_base.items():
    for pattern in data["patterns"]:
        for word in pattern.split():
            inverted_index[word.lower()].append(intent)

def get_intent(user_input):
    doc = nlp(user_input.lower())
    
    # 1. Check for exact matches first
    for intent, data in knowledge_base.items():
        for pattern in data["patterns"]:
            if pattern in user_input.lower():
                return intent
    
    # 2. Check using inverted index
    word_matches = set()
    for token in doc:
        if token.text in inverted_index:
            word_matches.update(inverted_index[token.text])
    
    if word_matches:
        return max(word_matches, key=lambda x: len(knowledge_base[x]["patterns"][0]))
    
    # 3. Use spaCy similarity as fallback
    max_similarity = 0
    best_match = None
    for intent, data in knowledge_base.items():
        for pattern in data["patterns"]:
            pattern_doc = nlp(pattern)
            similarity = doc.similarity(pattern_doc)
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = intent
    
    return best_match if max_similarity > 0.6 else None

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    intent = get_intent(user_message)
    
    if intent:
        response = knowledge_base[intent]["response"]
    else:
        response = "I couldn't find information about that. Here are some things I can help with:\n"
        response += "\n".join([f"- {', '.join(knowledge_base[k]['patterns'][:2])}..." for k in list(knowledge_base.keys())[:5]])
        response += "\n\nTry asking about one of these topics."
    
    return jsonify({'response': response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True)