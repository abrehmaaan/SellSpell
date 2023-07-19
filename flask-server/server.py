from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

app = Flask(__name__)
CORS(app)

# Initialize the ChatOpenAI instance
chat = ChatOpenAI(temperature=0.0, openai_api_key="YOUR_OPENAI_API_KEY")

# Define the template string and prompt template
template_string = """
Translate the text \
that is delimited by triple backticks \
into a style that is {style}. \
text: ```{text}```
"""
prompt_template = ChatPromptTemplate.from_template(template_string)

@app.route('/')
@cross_origin()
def root():
    return {"message":"Welcome to SellSpell"}

# Define the API endpoint to handle POST requests
@app.route('/update_description', methods=['POST'])
@cross_origin()
def update_description():
    try:
        # Get the JSON data from the request
        data = request.json
        if not data or 'title' not in data or 'description' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        # Extract the title and description from the JSON data
        title = data['title']
        description = data['description']

        # Define the style (you can customize this as per your needs)
        style = """American English \
                   in appealing tone that makes customer buy the product"""

        # Generate the messages using the template
        messages = prompt_template.format_messages(
            style=style,
            text=title + " " + description)

        # Get the updated description from the ChatOpenAI model
        response = chat(messages)
        updated_description = response.content

        # Return the updated description as a response
        return jsonify({'updated_description': updated_description}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
