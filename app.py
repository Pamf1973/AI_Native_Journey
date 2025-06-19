# app.py

from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Basics Helper</title>
</head>
<body style="font-family:Arial; text-align:center; padding:50px; background:#f4f4f4;">
    <h1>👋 Welcome to My Python Basics Helper</h1>
    <form method="post">
        <label for="topic">Choose a concept:</label><br><br>
        <select name="topic">
            <option value="variable">What is a Variable?</option>
            <option value="script">What is a Script?</option>
            <option value="ifelse">What is IF/ELSE?</option>
            <option value="debug">What is Debug?</option>
        </select><br><br>
        <input type="submit" value="Explain">
    </form>
    <hr>
    <p>{{ explanation }}</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    explanation = ""
    if request.method == "POST":
        topic = request.form["topic"]
        if topic == "variable":
            explanation = "A variable is like a labeled box that holds data. Example: name = 'Pedro'."
        elif topic == "script":
            explanation = "A script is a file that contains Python code. When you run it, it follows the instructions line by line."
        elif topic == "ifelse":
            explanation = "IF/ELSE helps Python make decisions. Example: if hungry: eat(); else: wait()."
        elif topic == "debug":
            explanation = "Debugging is the process of finding and fixing errors in your code."

    return render_template_string(html, explanation=explanation)

if __name__ == "__main__":
    app.run(debug=True)
