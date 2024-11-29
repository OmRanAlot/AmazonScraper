from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from backend.scraper import get_data, clean_data
import random
import asyncio
from flask_socketio import SocketIO
import settings

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = settings.SECRET_KEY

socketio = SocketIO(app)

scraped_data = None

# https://www.geeksforgeeks.org/post-redirect-get-prg-design-pattern/#



@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    # Show loading animation
    item_input = request.form.get('itemInput')
    page_input = request.form.get('pageInput')

    print(item_input, page_input)

    # Perform your scraping or processing logic here
    socketio.start_background_task(scraping_task, item_input, page_input)
        
    # Pass data back to the template
    return render_template("loading.html")
    
@app.route("/results", methods=["GET"])
def results():
    global scraped_data
    return render_template("landing.html", data=scraped_data)

def scraping_task(item, pages):
    global scraped_data
    scraped_data = get_data(item, pages)

    # Notify the client that scraping is complete
    socketio.emit("scraping_complete")

@app.route("/test")
def test():
    return "flask is running"

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001)