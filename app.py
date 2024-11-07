# app.py
from flask import Flask, render_template, request
from flask_cors import CORS
from backend.main import get_data, clean_data

app = Flask(__name__, template_folder="templates")
CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""  
    if request.method == "POST":
        userinput = request.form["userInput"]   
        print(userinput)
        try:
            rawData = get_data("laptop",userinput)
            print(rawData)
            print("break")
            output = clean_data(rawData)
            print(output)
        except:
            output = userinput
    return render_template("index.html", data=output, working=userinput)

@app.route("/test")
def test():
    return "flask is running"

if __name__ == "__main__":
    app.run(debug=True)
