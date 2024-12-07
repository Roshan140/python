from flask import Flask, request, jsonify, render_template
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# OpenAI client setup
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

@app.route("/")
def home():
    return render_template("index.html")  # Render the HTML template for the chatbot

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")  # Get user input from POST request
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        # Call NVIDIA API for AI completion
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=False  # Ensure streaming is turned off for simplicity
        )
        
        # Access the AI's response properly and format it with line breaks
        response = completion.choices[0].message.content
        formatted_response = response.replace('. ', '.<br><br>')  # Add line breaks between sentences or points
        return jsonify({"reply": formatted_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
