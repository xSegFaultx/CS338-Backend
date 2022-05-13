from flask import request, jsonify, send_file, make_response
from modules import app
from . import image_search
from . import text_to_speech
from . import custom_animations
import os
import json

@app.route("/")
def home():
    resp = make_response("This is the backend!", 200)
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

# input = [
#         { "birth": { "date": "Augest 10, 1970", "location": "Bangkok, Thailand" }},
#         { "school": { "name": "Harvard University", "start_date": "2015", "end_date": "2019", "location": "Massachusetts, Boston" }},
#     ]


@app.route("/video", methods=['GET', 'POST'])
def images():
    data = json.loads(request.get_data())
    print(request)
    print(data)
    
    if "input" not in data:
        resp = make_response("Please make sure the key is 'input'", 400)
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp

    if "name" not in data["input"][0]:
        resp = make_response("'name' must be the first event in input list.", 400)
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp

    input = data["input"]
    image_paths = image_search.image_search(input)
    audio_paths = text_to_speech.text_to_speech(input)
    video_name = "new_video.mp4"
    video_path = custom_animations.make_movie(image_paths, audio_paths, video_name=video_name)

    resp = make_response(send_file(video_path, as_attachment=True), 200)
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp
    