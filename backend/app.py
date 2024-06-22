from flask import Flask, request, jsonify
from gpt import get_gpt_response
from llama import get_llama_response
from gemini import get_gemini_response

app = Flask(__name__)

@app.route('/get-responses', methods=['POST'])
def get_responses():
    data = request.json
    prompt = data['prompt']
    
    # Get initial responses
    gpt_response = get_gpt_response(prompt)
    llama_response = get_llama_response(prompt)
    gemini_response = get_gemini_response(prompt)
    
    responses = {
        'GPT': gpt_response,
        'LLaMa': llama_response,
        'Gemini': gemini_response
    }
    
    # Collect votes
    votes = {'GPT': 0, 'LLaMa': 0, 'Gemini': 0}
    
    for model_name, model_response in responses.items():
        combined_prompt = f"Original prompt: {prompt}\n\nResponses:\n1. {gpt_response}\n2. {llama_response}\n3. {gemini_response}\n\nWhich is the best response?"
        if model_name == 'GPT':
            vote = get_gpt_response(combined_prompt)
        elif model_name == 'LLaMa':
            vote = get_llama_response(combined_prompt)
        elif model_name == 'Gemini':
            vote = get_gemini_response(combined_prompt)
        
        votes[vote] += 1
    
    # Determine the winner
    winner = max(votes, key=votes.get)
    
    return jsonify({'winner': winner, 'response': responses[winner]})

if __name__ == '__main__':
    app.run(debug=True)
