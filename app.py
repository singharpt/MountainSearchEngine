from flask import Flask, render_template

#__name__ references this file (app.py)
app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
