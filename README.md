# Chatbot


A smart chatbot that answers common queries using natural language processing.

## Features

- 💬 Natural language understanding with spaCy
- 🌐 Web-based interface accessible from any device

## Technology Stack

- **Backend**: Python Flask
- **NLP Engine**: spaCy
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Local server 

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatbot.git
   cd chatbot
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
5. Start the development server:
   ```bash
   python app.py
  The application will be available at:
  http://localhost:5000
   
