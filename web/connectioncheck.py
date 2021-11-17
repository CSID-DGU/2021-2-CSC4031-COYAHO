from flask import Flask
from flask import request
import requests
import threading

app = Flask(__name__)

url = "http://20.200.236.230"


@app.route('/')
def connect_check():

    try:
        res = requests.get(url)
        print(str(res.status_code))

    except requests.Timeout:
        print("timeout")
        pass
    except requests.ConnectionError:
        print("connectionerror")
        pass
    finally:
        threading.Timer(20, connect_check).start()
    return "OK"


if __name__ == "__main__":
    app.run()
