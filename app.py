from flask import Flask, request, jsonify, render_template
from database import DBManager
from chatbot import ResearchChatbot

db = DBManager()
chatbot = ResearchChatbot(database=db)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    result = chatbot.collect_messages(prompt=user_input, flask=True)
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)