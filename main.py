from flask import Flask
from flask import redirect, send_file, send_from_directory, request
import requests
import lxml
import re

app = Flask(__name__)

def parseURL(ph_key):
    dom = requests.get("https://www.pornhub.com/view_video.php?viewkey=" + ph_key).content

    result = re.search('"quality":"720","videoUrl":"(.*?)"},', dom.decode("utf-8"))

    return str(result.group(1).replace('\\', ''))

@app.route("/video")
def fromurl():
    try:
        ph_video = request.args.get("url")
    except Exception:
        try:
            ph_video = request.args.get("key")
        except Exception as e:
            return str(e)
        else:
            return redirect(parseURL(ph_video))    
    else:
        return redirect(parseURL(ph_video.split("=")[1]))

app.run(host="127.0.0.1", port=5000, debug=False)