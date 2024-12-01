from gevent import monkey
monkey.patch_all() #patches the standard library modules before they are imported

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from backend.scraper import get_data
from flask_socketio import SocketIO
import settings

#create flask app
app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = settings.SECRET_KEY

#create socketio app so python can communicate with the frontend
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

    # starts scraping in bkgd
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
    print("scraping complete")
    socketio.emit("scraping_complete")

@app.route("/test")
def test():
    return "flask is running"

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    socketio.run(app, debug=True, port=5001)


#url is 
# http://127.0.0.1:5001/