from flask import Flask, request, jsonify
import spacy
from spacy.matcher import PhraseMatcher
from string import punctuation
import re

app = Flask(__name__)

# Load English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# Knowledge base for the chatbot
knowledge_base = {
    "college_name": "The college name is DRK Institute of Science and Technology.",
    "contact": "Mobile: +91-90007 11899 or +91-87907 11899, Mail: principal@drkist.edu.in",
    "courses": "We offer:\n- CSE\n- CSE (AI & ML)\n- CSE (Data Science)\n- CSE (Cyber Security)\n- Electronics and Communication Engineering\n- Electrical and Electronics Engineering\n- Mechanical Engineering\n- Civil Engineering",
    "admission": "Apply through Telangana EAPCET or contact Admission Department for Management Quota.",
    "timings": "9:20 AM to 4:20 PM, Monday to Saturday.",
    "about": "DRKIST is a premier educational institution dedicated to helping students learn and grow.",
    "address": "Near Pragathi Nagar, Bowrampet (V), Hyderabad - 500043, Telangana, India",
    "placement_officer": "Syed Irfan Ali is the Placement Officer of DRK Institute of Science & Technology. We have a dedicated Placement Cell.",
    "placements": "We have a dedicated Placement Cell and top companies visit our college.",
    "hostel": "Not currently available.",
    "transport": "We provide bus facilities across Hyderabad.",
    "results": "Check on JNTUH website or DRKIST Results Portal.",
    "eligibility": "Eligibility varies. For B.Tech: Intermediate (10+2) or Diploma. For MBA: Bachelor's degree in any field.",
    "library": "Yes, the college has a well-stocked library with a wide range of books.",
    "syllabus": "Available on JNTUH website.",
    "duration": "B.Tech is 4 years (8 semesters).",
    "cse_hod": "Dr. K. Kanaka Vardhini is the Head of CSE",
    "csm_hod": "Dr. Durga Prasad Kavadi is the Head of CSE (AI & ML).",
    "csd_hod": "Mr. Jacob Jayaraj G is the Head of CSE (Data Science).",
    "csc_hod": "Dr. Durga Prasad Kavadi is the Head of CSE (Cyber Security).",
    "eee_hod": "Mrs. Y. Sai Jyotirmayi is the Head of EEE.",
    "mechanical_hod": "Dr. Pavan Bagali is the Head of Mechanical Engineering.",
    "ece_hod": "Ms. M. Sravanthi is the Head of ECE.",
    "hr_hod": "Mr. K.T. Thomas is the Head of HR.",
    "mba_hod": "Dr. P. Prasanthi is the Head of MBA Department.",
    "join_club": "Club events and sessions are conducted on Saturdays. You can join by contacting head of club",
    "clubs": "We have technical and cultural clubs. Sessions usually take place on Saturdays.",
    "labs": "We have specialized labs for each stream.",
    "fees": "Please contact the Admission Department for the latest fee structure.",
    "tc": "Visit the Admission Department for your Transfer Certificate (TC).",
    "bonafide": "Request your Bonafide Certificate at the Admission Department.",
    "professor": "Yes, contact details (email & mobile) are available on the official website.",
    "timetable": "Please refer to the DRKIST attendance portal for your class timetable.",
    "attendance_requirement": "75% attendance is mandatory.",
    "attendance": "Check your attendance on the DRKIST Attendance Portal using your Roll Number.",
    "sports": "Yes, we offer a variety of sports and activities including:\n- Cricket\n- Basketball\n- Volleyball\n- Kho-Kho\n- Throw Ball\n- Badminton",
    "chairman": "Sri D.B Chandra Sekhara Rao is the Chairman of DRK",
    "secretary": "Sri D. Santosh",
    "treasurer": "Sri D. Sriram",
    "principal": "Dr. Gnaneswara Rao Nitta is the Principal of DRK Institute of Science & Technology"
}

# Create phrase matcher for better intent recognition
matcher = PhraseMatcher(nlp.vocab)
phrases = list(knowledge_base.keys())
patterns = [nlp(text) for text in phrases]
matcher.add("KNOWLEDGE", patterns)

# Preprocess text - remove punctuation, lowercase, etc.
def preprocess(text):
    text = text.lower()
    text = re.sub(f'[{punctuation}]', '', text)
    return text

# Find the most relevant intent
def get_intent(user_input):
    doc = nlp(preprocess(user_input))
    
    # Check for matches with the phrase matcher
    matches = matcher(doc)
    if matches:
        match_id, start, end = matches[0]
        return nlp.vocab.strings[match_id]
    
    # If no direct match, use similarity
    max_similarity = 0
    best_match = None
    
    for intent in knowledge_base.keys():
        intent_doc = nlp(intent)
        similarity = doc.similarity(intent_doc)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = intent
    
    return best_match if max_similarity > 0.5 else None

# Chatbot response function
def get_response(user_input):
    intent = get_intent(user_input)
    
    if intent and intent in knowledge_base:
        return knowledge_base[intent]
    else:
        return "I'm sorry, I don't understand that question. Please try asking something else."

# API endpoint for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    response = get_response(user_message)
    return jsonify({'response': response})

# Serve the frontend
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)