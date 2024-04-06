from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/home")
def test():
    return render_template("temp.html")

@app.route("/setb")
def test1():
    return render_template("new.html")

@app.route("/expense")
def test2():
    return render_template("addexp.html")

@app.route("/profile")
def test3():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
