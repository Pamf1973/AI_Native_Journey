# app.py

from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template with styles and emojis
html = """
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Python Basics Helper</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #e8f4fc;
            color: #2c3e50;
            padding: 50px;
            text-align: center;
        }
        h1 {
            font-size: 48px;
            margin-bottom: 20px;
        }
        form {
            margin: 30px auto;
        }
        select, input[type="submit"] {
            font-size: 20px;
            padding: 10px;
            margin-top: 10px;
        }
        p {
            font-size: 24px;
            margin-top: 40px;
            padding: 15px;
            background: #ffffffcc;
            display: inline-block;
            border-radius: 10px;
            max-width: 700px;
        }
        .emojis {
            font-size: 40px;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <h1>🐍 Python Basics Helper 📚</h1>
    <form method="post">
        <label for="topic"><strong>Select a concept to learn:</strong></label><br><br>
        <select name="topic">
            <option value="variable">🔡 What is a Variable?</option>
            <option value="script">📜 What is a Script?</option>
            <option value="ifelse">🔀 What is IF/ELSE?</option>
            <option value="debug">🐞 What is Debug?</option>
        </select><br><br>
        <input type="submit" value="🧠 Teach Me!">
    </form>

    {% if explanation %}
    <p>{{ explanation }}</p>
    {% endif %}

    <div class="emojis">
        💻 ⚙️ 🤖
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    explanation = ""
    if request.method == "POST":
        topic = request.form["topic"]
        if topic == "variable":
            explanation = "🔡 A variable is like a labeled box where you store information. Example: name = 'Pedro'"
        elif topic == "script":
            explanation = "📜 A script is a file filled with Python code — instructions your computer follows from top to bottom."
        elif topic == "ifelse":
            explanation = "🔀 IF/ELSE lets Python make decisions. If something is true, do this. Otherwise, do something else."
        elif topic == "debug":
            explanation = "🐞 Debugging means finding and fixing errors in your code so everything works smoothly."

    return render_template_string(html, explanation=explanation)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
