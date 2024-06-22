from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from llms import get_gpt_response, get_llama_response, get_claude_response

app = Flask(__name__)
CORS(app, resources={r"/get-responses": {"origins": "http://localhost:5173"}})

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        res.headers.add("Access-Control-Allow-Headers", "Content-Type, *")
        res.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        return res

@app.route('/get-responses', methods=['POST', 'OPTIONS'])
def get_responses():
    if request.method == 'OPTIONS':
        return '', 204  # No content needed for OPTIONS response

    data = request.json
    prompt = data['prompt']
    
    # Example responses
    gpt_response = "Example GPT response"
    llama_response = "Example LLaMa response"
    claude_response = "Example Claude response"
    
    responses = {
        'GPT': gpt_response,
        'LLaMa': llama_response,
        'Claude': claude_response
    }
    
    votes = {'GPT': 0, 'LLaMa': 0, 'Claude': 0}
    
    for model_name, model_response in responses.items():
        combined_prompt = f"Original prompt: {prompt}\n\nResponses:\n1. {gpt_response}\n2. {llama_response}\n3. {claude_response}\n\nWhich is the best response?"
        if model_name == 'GPT':
            vote = get_gpt_response(combined_prompt)
        elif model_name == 'LLaMa':
            vote = get_llama_response(combined_prompt)
        elif model_name == 'Claude':
            vote = get_claude_response(combined_prompt)
        
        votes[model_name] += 1
    
    winner = max(votes, key=votes.get)
    
    return jsonify({'winner': winner, 'response': responses[winner]})

if __name__ == '__main__':
    app.run(debug=True)
