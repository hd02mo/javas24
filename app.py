from flask import Flask, render_template

# Flaskオブジェクトの作成
app = Flask(__name__)

# '/'へアクセスがあったときの処理
@app.route('/')
def hello():
    return 'Hello World!'

# '/index'へアクセスがあったときの処理
@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)