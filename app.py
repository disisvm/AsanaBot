from flask import Flask, request, render_template, session, redirect, url_for
from bot_functions import (
    find_closest_answer_enhanced,
    handle_multi_turn_dialogue
)

app = Flask(__name__)
app.secret_key = 'manish3308'  # Replace with a secure secret key

@app.route("/", methods=["GET", "POST"])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == "POST":
        if 'reset' in request.form:
            session.pop('chat_history', None)  # Reset the chat history completely
            return redirect(url_for('index'))  # Redirect to clear the form data

        user_query = request.form.get("query")

        # Get response from chatbot using multi-turn dialogue handling
        response = handle_multi_turn_dialogue(user_query)

        # Update the chat history
        session['chat_history'].append({"role": "You", "content": user_query})
        session['chat_history'].append({"role": "Bot", "content": response})

        # Ensure session is saved
        session.modified = True

        return render_template("index.html", chat_history=session['chat_history'])

    return render_template("index.html", chat_history=session['chat_history'])

if __name__ == "__main__":
    app.run(debug=True)
