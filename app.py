from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
from backend.main import get_data, clean_data

app = Flask(__name__, template_folder="templates")
CORS(app)

# https://www.geeksforgeeks.org/post-redirect-get-prg-design-pattern/#

@app.route("/", methods=["GET"])
def index():
    output = ""  
    testing = "lololol"
    if request.method == "GET":
        userinput = request.args.get("userInput")   
        print(userinput)
        try:
            rawData = get_data("laptop",userinput)
            print(rawData)
            print("break")
            output = clean_data(rawData)
            print(output)
        except:
            output = []

    return render_template("index.html", data=output, working=testing)

@app.route("/test")
def test():
    return "flask is running"

if __name__ == "__main__":
    app.run(debug=True)
