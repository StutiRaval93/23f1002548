from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/student_register")
def student_register():
    return render_template("student_register.html")

if __name__ == "__main__":
    app.run(debug=True)

