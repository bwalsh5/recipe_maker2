from quart import Quart, render_template, request
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI()

# this is a long comment.


# Create the Quart app
app = Quart(__name__)

@app.route('/', methods=['GET'])
async def index():
    return await render_template('index.html', assistant_reply="")

@app.route('/chat', methods=['POST'])
async def chat():
    try:
        # Get ingredients from form
        form_data = await request.form
        ingredients = form_data['user_input']

        # Prompt GPT with a recipe assistant system message
        messages = [
            {
                "role": "system",
                "content": "You are a helpful recipe assistant. When given a list of ingredients, suggest one or two possible dishes someone could cook. If possible, provide simple instructions too."
            },
            {
                "role": "user",
                "content": ingredients
            }
        ]

        # Call OpenAI
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        # Extract the assistant's reply
        assistant_response = response.choices[0].message.content

        # Return the rendered page
        return await render_template('index.html', assistant_reply=assistant_response)

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return await render_template("index.html", assistant_reply="Something went wrong, please try again.")

if __name__ == "__main__":
    app.run(debug=True)
