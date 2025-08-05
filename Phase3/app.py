from flask import Flask , render_template ,request , jsonify
from flask_pymongo import PyMongo



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/chatgpt"
mongo = PyMongo(app)

@app.route("/")
def home():
    questions_collection = mongo.db.questions
    all_qs = list(questions_collection.find({}, {"answer": 0}))
    return render_template("index.html",all_qs=all_qs)

@app.route("/api", methods=["GET","POST"])
def API():
    question = request.json
    if request.method == "POST":
        chat = mongo.db.questions.insert_one({
            "question" : question,
            "answer" : f"This is answer of {question}"
        })
        return jsonify({
            'question' : question,
            'result' : f"This is answer of {question}"
        })
    return jsonify({
            'question' : question,
            'result' : "This is result"
        })
    

if(__name__ == "__main__"):
    app.run(debug=True)