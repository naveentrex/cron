from flask import Flask, request, jsonify
from flask_cors import CORS
import testing
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the app

cron_status_process = []

def get_active_cron_processes():
    global cron_status_process

    while True:
        # TODO: Add logic to get information about active cron processes using psutil
        # For demonstration purposes, sleep for 5 milliseconds
        time.sleep(2)
        cron_status_process = testing.get_cron_tree()
        print(cron_status_process)

# Start the thread for monitoring active cron processes
cron_thread = threading.Thread(target=get_active_cron_processes)
cron_thread.daemon = True  # Daemonize the thread so it stops when the main program stops
cron_thread.start()

@app.route("/running-jobs/")
def home():
    data = {
        "id": 1
    }
    # data = testing.get_active_cron_tree()
    print("PRINTING DATA TO SEND")
    print(cron_status_process)
    # return jsonify(data), 200
    return jsonify(cron_status_process), 200


if __name__ == "__main__":
    app.run(debug=True)
